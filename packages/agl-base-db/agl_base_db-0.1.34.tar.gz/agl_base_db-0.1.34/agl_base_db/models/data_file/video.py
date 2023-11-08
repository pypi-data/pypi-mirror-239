from django.db import models

from agl_base_db.models.data_file.frame import Frame
from agl_base_db.models.data_file.frame import LegacyFrame

BATCH_SIZE = 1000
from .base_classes import AbstractVideo


class Video(AbstractVideo):
    def get_video_model(self):
        return Video
    def get_frame_model(self):
        return Frame
    

class LegacyVideo(AbstractVideo):
    file = models.FileField(upload_to="legacy_videos", blank=True, null=True)

    def get_video_model(self):
        return LegacyVideo
    def get_frame_model(self):
        return LegacyFrame

    