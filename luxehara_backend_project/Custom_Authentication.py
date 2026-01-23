from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # Extract token from cookies instead of headers
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            return None  # No token, proceed without authentication
        
        try:
            # Validate the token
            validated_token = self.get_validated_token(access_token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception as e:
            raise AuthenticationFailed("Invalid or expired token")
