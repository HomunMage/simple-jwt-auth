# JWTToken.py

from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from jose import JWTError, jwt

class JWTToken:
    """
    A class for creating and verifying JWT tokens.
    """
    def __init__(self, secret_key: str, algorithm: str = "HS256", access_token_expire_minutes: int = 30):
        """
        Initializes the JWTToken class.

        Args:
            secret_key: The secret key used to sign and verify tokens.
            algorithm: The algorithm used to sign the tokens (default: HS256).
            access_token_expire_minutes: The default expiration time for access tokens in minutes (default: 30).
        """
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_token_expire_minutes

    def create_access_token(self, username: str, expires_delta: timedelta | None = None) -> str:
        """
        Creates a JWT access token with the username as the subject.

        Args:
            username: The username to encode into the token.
            expires_delta: An optional timedelta for when the token should expire. If None, uses the default.

        Returns:
            The encoded JWT access token.
        """
        to_encode = {"sub": username}  # "sub" claim holds the username
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """
        Verifies a JWT token and returns the username if valid, None otherwise.

        Args:
            token: The JWT token to verify.

        Returns:
            The username extracted from the token if valid, otherwise None.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username = payload.get("sub")
            if username:
                return username
            else:
                return None  # "sub" claim is missing

        except JWTError:
            return None


# Example usage
if __name__ == "__main__":
    # Replace with your actual secret key.  **KEEP THIS SECRET!**
    SECRET_KEY = "your-secret-key"

    # Initialize the JWTToken class with your secret key
    jwt_token = JWTToken(SECRET_KEY)

    # 1. Encode username to get token
    username_to_encode = "testuser"
    access_token = jwt_token.create_access_token(username_to_encode)
    print(f"Generated Token: {access_token}")

    # 2. Decode token to get username
    decoded_username = jwt_token.verify_token(access_token)

    if decoded_username:
        print(f"Token is valid.  Decoded username: {decoded_username}")
    else:
        print("Token is invalid.")

    # 3. Invalid token example
    invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub3R0aGV1c2VyIiwiZXhwIjoxNzQ3OTM1MjQzfQ.2G_3d7e6L4n9P9v8zG0mP6qN2W8kX7qY3t1n2qKzM8"
    decoded_username = jwt_token.verify_token(invalid_token)

    if decoded_username:
        print(f"Token is valid. Decoded username: {decoded_username}")
    else:
        print("Token is invalid.")

    # 4. Expired token example
    expired_access_token = jwt_token.create_access_token("testuser", expires_delta=timedelta(seconds=-1))
    decoded_username = jwt_token.verify_token(expired_access_token)

    if decoded_username:
        print(f"Token is valid. Decoded username: {decoded_username}")
    else:
        print("Token is invalid or Expired.")