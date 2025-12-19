from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings


def send_activation_email(request, user):
    """
    Envoie un email d'activation de compte à l'utilisateur.
    
    Args:
        request: La requête HTTP
        user: L'instance de l'utilisateur à activer
    
    Returns:
        bool: True si l'email a été envoyé avec succès, False sinon
    """
    try:
        # Encode l'ID de l'utilisateur de manière sécurisée
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # Crée un token d'activation pour l'utilisateur
        token = default_token_generator.make_token(user)
        # Récupère le domaine actuel de l'application
        domain = get_current_site(request).domain
        # Génère le lien d'activation avec les paramètres uid et token
        link = f"http://{domain}{reverse('activate', kwargs={'uid': uid, 'token': token})}"
        
        # Message à envoyer
        message = f"""Bonjour {user.first_name} {user.last_name},

Merci de vous être inscrit sur notre plateforme !

Pour activer votre compte, veuillez cliquer sur le lien suivant :
{link}

Ce lien est valide pendant 7 jours.

Si vous n'avez pas créé de compte, veuillez ignorer cet email.

Cordialement,
L'équipe"""
        
        # Envoie l'email à l'utilisateur
        send_mail(
            subject="Activation de compte",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )
        return True
    except Exception as e:
        # En production, vous devriez logger cette erreur avec un vrai logger
        error_msg = str(e)
        if "535" in error_msg or "BadCredentials" in error_msg or "Username and Password not accepted" in error_msg:
            print(f"Erreur d'authentification email: Les identifiants Gmail sont incorrects ou expirés.")
            print(f"Vérifiez que vous utilisez un 'App Password' Gmail valide dans EMAIL_HOST_PASSWORD.")
            print(f"Pour générer un App Password: https://myaccount.google.com/apppasswords")
        else:
            print(f"Erreur lors de l'envoi de l'email d'activation: {e}")
        return False


def send_reset_password_email(request, user):
    """
    Envoie un email de réinitialisation du mot de passe à l'utilisateur.
    """
    # Encode l'ID de l'utilisateur de manière sécurisée
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    # Crée un token pour réinitialiser le mot de passe
    token = default_token_generator.make_token(user)
    # Récupère le domaine actuel de l'application
    domain = get_current_site(request).domain
    # Génère le lien de réinitialisation avec les paramètres uid et token
    link = f"http://{domain}{reverse('password-reset-confirm', kwargs={'uid': uid, 'token': token})}"
    
    # Message à envoyer
    message = f"Réinitialisez votre mot de passe en cliquant sur ce lien : {link}"

    # Envoie l'email à l'utilisateur
    send_mail(
        subject="Réinitialisation du mot de passe",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,  # Utilise l'email par défaut configuré dans settings.py
        recipient_list=[user.email]
    )
