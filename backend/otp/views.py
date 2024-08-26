from rest_framework import permissions, mixins, viewsets, generics, response, request, views, status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

class OTPVerifyView(views.APIView):
    serializer_class = OTPSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, otp_uuid, format=None):
        serializer = self.serializer_class(data=request.data)
        try:
            otpinstance = OTPInstance.objects.get(uuid=otp_uuid)
        except OTPInstance.DoesNotExist as e:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        otp = serializer.validated_data['otp']
        if otpinstance.otp != otp:
            otpinstance.max_otp_try -= 1
            otpinstance.save()
            if otpinstance.max_otp_try <= 0:
                otpinstance.delete()
            return response.Response({'remaining_tries': otpinstance.max_otp_try}, status=status.HTTP_401_UNAUTHORIZED)
        token = RefreshToken.for_user(otpinstance.user)
        otpinstance.delete()
        return response.Response({
            'refresh': str(token),
            'access': str(token.access_token)
        }, status=status.HTTP_200_OK)
