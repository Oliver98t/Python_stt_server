from api.models import Snippet
from api.serializers import SnippetSerializer
from rest_framework.response import Response
from api.models import Snippet, Transcription
from api.serializers import SnippetSerializer, TranscriptionSerializer
from rest_framework import permissions
from api.permissions import IsOwnerOrReadOnly
from api.serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from time import sleep
import subprocess
from re import sub

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'api': reverse('snippet-list', request=request, format=format),
        'transcription': reverse('transcription-list', request=request, format=format)
    })

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TranscriptionViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        transcription = self.get_object()
        return Response(transcription.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        wav_file = request.FILES.get('wav_file')
        print(wav_file)

        # Save the instance first to get the file path
        response = super().create(request, *args, **kwargs)
        instance = self.get_queryset().get(pk=response.data['id'])

        cmd = [
            '/home/oli19/whisper.cpp/build/bin/whisper-cli',
            '/home/oli19/projects/Backend/django_sandbox/stt_server/media/transcriptions_wav/jfk.wav',
            '-m',
            '/home/oli19/whisper.cpp/models/ggml-base.en.bin',
            '-np'
        ]

        # Run the command and get the output
        result = subprocess.run(cmd, capture_output=True, text=True)
        transcription_string = sub(r'^[^\]]*\]\s*', '', result.stdout)
        
        # Update the transcription field with the output
        instance.transcription = transcription_string
        instance.save(update_fields=['transcription'])

        # Modify the response data as needed
        data = response.data
        data['transcription'] = instance.transcription  # update the field in the response

        return Response(data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer