import logging

from os.path import join

from babelfish import Language
from guessit import guess_video_info
from subliminal import download_best_subtitles
from subliminal.subtitle import get_subtitle_path
from subliminal.video import Video

from touchandgo.helpers import get_settings


log = logging.getLogger('touchandgo.download')


class SubtitleDownloader(object):
    def __init__(self, sub_lang):
        self.lang = sub_lang

    def download(self, video_file):
        subtitle = None
        settings = get_settings()
        download_dir = settings.save_path
        log.info("Downloading subtitle")
        filepath = join(download_dir, video_file[0])
        guess = guess_video_info(filepath, info=['filename'])
        video = Video.fromguess(filepath, guess)
        video.size = video_file[1]
        try:
            subtitle = download_best_subtitles([video], {Language(self.lang)},
                                               single=True)
        except ValueError:
            pass
        if subtitle is not None and len(subtitle):
            log.info("CLAH %s %s", download_dir, video.name)
            subtitle = get_subtitle_path(join(download_dir,
                                              video.name.replace("(", "\(")
                                              .replace(")", "\)")
                                              .replace(" ", "\ ")))
        log.info("video_file: %s, filepath: %s, guess: %s, video: %s, "
                 "subtitle: %s", video_file, filepath, guess, video, subtitle)
        return subtitle

