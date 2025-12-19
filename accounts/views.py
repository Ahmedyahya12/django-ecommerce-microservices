from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .serializers import EditProfileSerializer


from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)

from .models import CustomUser 
from .utils import send_activation_email, send_reset_password_email


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Tenter d'envoyer l'email d'activation
        email_sent = send_activation_email(request, user)
        
        if email_sent:
            return Response(
                {"message": "Inscription réussie ! Vérifiez votre email pour activer votre compte."}, 
                status=status.HTTP_201_CREATED
            )
        else:
            # Même si l'email n'a pas pu être envoyé, l'utilisateur est créé
            # En production, vous devriez logger cette erreur et peut-être créer un mécanisme de réessai
            return Response(
                {
                    "message": "Inscription réussie, mais l'email d'activation n'a pas pu être envoyé. Veuillez contacter le support.",
                    "warning": "email_not_sent"
                }, 
                status=status.HTTP_201_CREATED
            )


class ActivateAccountView(APIView):
    """
    Vue pour activer un compte utilisateur via un lien d'activation.
    Accepte les méthodes GET et POST.
    """
    
    def get(self, request, uid, token):
        return self.activate_account(uid, token)
    
    def post(self, request, uid, token):
        return self.activate_account(uid, token)
    
    def activate_account(self, uid, token):
        """
        Méthode commune pour activer le compte.
        """
        try:
            # Décoder l'UID depuis l'URL
            decoded_uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=decoded_uid)
        except (TypeError, ValueError, OverflowError):
            return Response(
                {"error": "Lien d'activation invalide. Le format de l'identifiant est incorrect."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Lien d'activation invalide. L'utilisateur n'existe pas."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Vérifier si le compte est déjà activé
        if user.is_active:
            return Response(
                {"message": "Votre compte est déjà activé."}, 
                status=status.HTTP_200_OK
            )
        
        # Vérifier la validité du token
        if not default_token_generator.check_token(user, token):
            return Response(
                {"error": "Lien d'activation expiré ou invalide. Veuillez demander un nouveau lien d'activation."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Activer le compte
        user.is_active = True
        user.save()
        
        return Response(
            {"message": "Compte activé avec succès ! Vous pouvez maintenant vous connecter."}, 
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = CustomUser.objects.get(email=email)  # Use your custom user model
        except:
            return Response({"error": "Email ou mot de passe incorrect"}, status=400)

        if not user.is_active:
            return Response({"error": "Compte non activé"}, status=401)

        # Authenticate using email since USERNAME_FIELD is 'email'
        user = authenticate(username=user.email, password=password)

        if not user:
            return Response({"error": "Email ou mot de passe incorrect"}, status=400)

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
           
        })

class EditProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = EditProfileSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            updated_user = serializer.save()
            email_changed = updated_user.is_active == False   # si email changé → compte désactivé


            # Si email modifié → envoyer un email d'activation
            if email_changed:
                send_activation_email(request, updated_user)
                
                return Response(
                    {
                        "message": "Email modifié. Vérifiez votre nouveau email pour réactiver votre compte.",
                        "email_changed": True
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    "message": "Profil mis à jour avec succès.",
                    "email_changed": False
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        try:
            user = CustomUser.objects.get(email=email)  # Use your custom user model
            send_reset_password_email(request, user)
        except:
            pass

        return Response({"message": "Si l'email existe, un lien a été envoyé."})


class ResetPasswordConfirmView(APIView):
    def post(self, request, uid, token):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(pk=uid)  # Use your custom user model
        except:
            return Response({"error": "Lien invalide"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token invalide"}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"message": "Mot de passe réinitialisé avec succès"})
