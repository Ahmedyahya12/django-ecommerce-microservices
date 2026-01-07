from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser  # Importation du modèle CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["last_name", "first_name", "email", "password", "password2", "phone_number"]

    def validate_email(self, value):
        # Vérifier si l'email existe déjà dans la base de données
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cet email existe déjà.")
        return value

    def validate(self, data):
        # Vérifie si les mots de passe correspondent
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        # Supprime le champ password2 et crée l'utilisateur
        validated_data.pop("password2")
        user = CustomUser.objects.create_user(
            username=validated_data["email"],  
            last_name=validated_data["last_name"],
            first_name=validated_data["first_name"],
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number", ""),
            is_active=False  # Activation par email
        )
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False},
            "username": {"required": False},
        }

    def update(self, instance, validated_data):
        # ---- 1) Vérifier si l’email change ----
        if "email" in validated_data and validated_data["email"] != instance.email:
            new_email = validated_data["email"]

            instance.email = new_email
            # instance.username = new_email   # 🔥 Synchroniser username avec email
            instance.is_active = False      # Désactiver le compte pour réactivation

        # ---- 2) Mise à jour prénom / nom ----
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        # ---- 3) Mise à jour du mot de passe ----
        if "password" in validated_data and validated_data["password"]:
            instance.password = make_password(validated_data["password"])

        # ---- 4) Sauvegarde ----
        instance.save()

        return instance

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    def validate(self, data):
        # Vérifie si les mots de passe de confirmation et de réinitialisation correspondent
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas")
        return data


class UserSerializer(serializers.ModelSerializer):
     
     class Meta:
          model=User
          fields=['id','email','first_name','last_name']

