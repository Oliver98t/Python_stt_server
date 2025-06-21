from rest_framework import serializers
from api.models import Transcription, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User

class TranscriptionSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='transcription-highlight', format='html')

    class Meta:
        model = Transcription
        fields = ['url', 'id', 'highlight', 'owner', 'ip','created', 'transcription', 'wav_file']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    transcriptions = serializers.HyperlinkedRelatedField(many=True, view_name='transcription-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'transcriptions']