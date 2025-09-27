# accounts/views.py
from rest_framework import generics, permissions
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .tasks import send_email

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        user = serializer.save()  # this is the new User instance
        send_email(
            subject="Welcome to Project Nexus!",
            message=f"Hi {user.username}, thanks for registering.",
            recipient=[user.email],
        )

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def me_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)



