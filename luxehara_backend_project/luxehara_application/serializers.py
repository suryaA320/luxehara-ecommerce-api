from rest_framework import serializers
from luxehara_application.models import User
from django.contrib.auth.password_validation import validate_password



#  Add Serializers below
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "mobile_number","role", "user_status"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "mobile_number","alternate_number", "address", "state", "city", "pincode", "password", "password2", "role", "user_status"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")  # Remove extra password field

        user = User.objects.create(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password properly
        user.save()

        return user