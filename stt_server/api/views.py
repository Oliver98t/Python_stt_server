from rest_framework import viewsets, permissions, status, renderers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import MultiPartParser, FormParser
from api.models import Transcription
from api.serializers import TranscriptionSerializer, UserSerializer
from api.permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
import subprocess
from re import sub

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'transcription': reverse('transcription-list', request=request, format=format)
    })

class TranscriptionViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Transcription.objects.all()
    serializer_class = TranscriptionSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,permissions.IsAuthenticated,
                          IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        transcription = self.get_object()
        return Response(transcription.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get(self, request):
        return Response({'message': 'You are authenticated'})

    def create(self, request, *args, **kwargs):
        # Save the instance first to get the file path
        wav_file = request.FILES.get('wav_file')
        response = super().create(request, *args, **kwargs)
        instance = self.get_queryset().get(pk=response.data['id'])
        wav_file_path = instance.wav_file.path
        print(wav_file_path)
        cmd = [
            '/home/oli19/whisper.cpp/build/bin/whisper-cli',
            wav_file_path,
            '-m',
            '/home/oli19/whisper.cpp/models/ggml-base.en.bin',
            '-np'
        ]
        # filter output string
        result = subprocess.run(cmd, capture_output=True, text=True)
        transcription_string = sub(r'^[^\]]*\]\s*', '', result.stdout)
        instance.transcription = transcription_string
        
        # get client ip
        client_ip = request = request.META.get('REMOTE_ADDR')
        instance.ip = client_ip
        
        # save updated instance
        instance.save(update_fields=['transcription', 'ip'])
        
        # send response
        data = response.data
        data.update({
            'transcription': instance.transcription,
            'ip': instance.ip,
        })

        return Response(data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer