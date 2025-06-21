from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.core.files.storage import FileSystemStorage
import os

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(self.location, name))
        return name

class Transcription(models.Model):
    owner = models.ForeignKey('auth.User', related_name='transcriptions', on_delete=models.CASCADE)
    ip = models.CharField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    transcription = models.TextField(blank=True, null=True)
    wav_file = models.FileField(upload_to='transcriptions_wav/', null=True, blank=True, storage=OverwriteStorage())

    class Meta:
        ordering = ['created']