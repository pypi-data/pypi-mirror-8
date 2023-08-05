#! /usr/bin/env python2
from __future__ import division

import argparse
import thread
import logging

from os import system
from os import _exit
from os.path import join, exists
from time import sleep
from datetime import datetime

from libtorrent import add_magnet_uri, session, storage_mode_t

from touchandgo.constants import STATES
from touchandgo.helpers import is_port_free, get_free_port
from touchandgo.logger import log_set_up
from touchandgo.settings import DEBUG, TMP_DIR, DOWNLOAD_LIMIT, WAIT_FOR_IT, \
    DEFAULT_PORT
from touchandgo.strategy import DefaultStrategy
from touchandgo.stream_server import serve_file
from touchandgo.subtitles import SubtitleDownloader


log = logging.getLogger('touchandgo.download')


class DownloadManager(object):
    strategy_class = DefaultStrategy
    sub_downloader_class = SubtitleDownloader

    def __init__(self, magnet, port=None, sub_lang=None, serve=False):
        self.magnet = magnet
        if port is None:
            port = DEFAULT_PORT
        port = int(port)
        if not is_port_free(port):
            port = get_free_port()

        log.info("[Magnet]: %s [Port]: %s [Sub_lang]: %s [Serve]: %s ",
                 magnet, port, sub_lang, serve)

        self.port = port
        self.serve = serve

        # number of pieces to wait until start streaming
        # we are waiting untill all the first peices are downloaded
        # the biggest file which is supposed to be a video file
        self._video_file = None
        self.callback = serve_file
        self._served_blocks = None
        self.streaming = False

        self.stream_th = None
        self.player_th = None
        self.httpd = None

        self.init_handle()
        self.strategy = self.strategy_class(self)

        if sub_lang is not None:
            self.subtitle = self.sub_downloader_class(sub_lang)
        else:
            self.subtitle = None

    def init_handle(self):
        params = {
            "save_path": TMP_DIR,
            "allocation": storage_mode_t.storage_mode_sparse,
            }
        self.session = session()
        self.handle = add_magnet_uri(self.session, str(self.magnet), params)
        self.handle.set_upload_limit(DOWNLOAD_LIMIT)

    @property
    def status(self):
        return self.handle.status()

    def start(self):
        try:
            self.start_time = datetime.now()
            self.session.listen_on(6881, 6891)
            self.session.start_dht()
            print("Downloading metadata")
            log.info("Downloading metadata")
            while not self.handle.has_metadata():
                print("\n" * 80)
                print self.stats()
                sleep(.5)
            log.info("Starting download")
            self.strategy.initial()

            while True:
                if not self.handle.is_seed():
                    self.strategy.master()
                elif self.strategy.holding_stream:
                    self.strategy.holding_stream = False

                if not self.streaming and self.status.state == 3:
                    self.stream()

                print("\n" * 80)
                print self.stats(DEBUG)
                sleep(1)
        except KeyboardInterrupt:
            if self.httpd is not None:
                self.httpd.shutdown()
            raise KeyboardInterrupt

    @property
    def video_file(self):
        if self._video_file is None:
            self._video_file = self.get_biggest_file()
            log.info("Video File: %s", self._video_file)
        return self._video_file

    def get_biggest_file(self):
        info = self.handle.get_torrent_info()
        biggest_file = ("", 0)
        files = info.files()
        for file_ in files:
            if file_.size > biggest_file[1]:
                biggest_file = [file_.path, file_.size]

        return biggest_file

    def run_vlc(self):
        while not exists(join(TMP_DIR, self.video_file[0])):
            sleep(WAIT_FOR_IT)
        command = "vlc http://localhost:%s -q" % self.port
        if self.subtitle is not None:
            subtitle = self.subtitle.download(self.video_file)
            if subtitle is not None:
                command += " --sub-file %s" % subtitle
        try:
            system(command)
        except KeyboardInterrupt:
            log.debug("Closing VLC")
        _exit(0)

    def stream(self):
        if self.callback is not None and not self.streaming:
            self.streaming = True
            pieces = self.status.pieces
            self._served_blocks = [False for i in range(len(pieces))]
            self.stream_th = thread.start_new_thread(self.callback, (self, ))
            if not self.serve:
                self.player_th = thread.start_new_thread(self.run_vlc, ())

    def block_served(self, block):
        self._served_blocks[block] = True

    def defrag(self):
        numerales = ""
        pieces = self.status.pieces
        for i, piece in enumerate(pieces):
            numeral = "#" if piece else " "
            if self._served_blocks is not None and self._served_blocks[i]:
                numeral = ">"
            numeral += str(self.handle.piece_priority(i))
            numerales += numeral
        return "%s\n" % numerales

    def stats(self, defrag=False):
        status = self.status
        text = ""
        if self._video_file is not None:
            text += "Serving %s on http://localhost:%s\n" % (self.video_file[0],
                                                             self.port)
        if defrag:
            text += self.defrag()
        text += '%s %.2f%% complete ' % (STATES[status.state],
                                         status.progress * 100)
        text += '(down: %.1f kB/s up: %.1f kB/s peers: %d)\n' % \
            (status.download_rate / 1000, status.upload_rate / 1000,
             status.num_peers)
        text += "Elapsed Time %s" % (datetime.now() - self.start_time)
        return text


def main():
    log_set_up()
    parser = argparse.ArgumentParser()

    parser.add_argument("magnet", nargs='?', default=None)
    parser.add_argument("--sub", nargs='?', default=None)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--port", "-p", default="8888")

    args = parser.parse_args()

    manager = DownloadManager(args.magnet, port=args.port, serve=args.serve,
                              sub_lang=args.sub)
    manager.start()

if __name__ == "__main__":
    main()
