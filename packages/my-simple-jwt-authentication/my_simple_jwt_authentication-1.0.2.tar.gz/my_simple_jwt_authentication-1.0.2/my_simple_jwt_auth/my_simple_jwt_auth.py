import jwt
import pytz
from uuid import uuid4
from datetime import datetime, timedelta


class JwtAuthentication:
    def authenticate(self, header, secret_key):
        token = self.get_token_from_header(header)
        if not token:
            return None

        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            raise ValueError("Invalid signature.")
        except jwt.exceptions.ExpiredSignatureError:
            raise ValueError("Token has been expired.")
        except Exception as e:
            raise ValueError("invalid token.")

        username = payload.get("username")
        return username

    @property
    def jti(self):
        jti = str(uuid4())
        return jti

    def generate_access_token(self, jti, username, access_key_expire_time, secret_key):
        now = datetime.now(tz=pytz.timezone("Asia/Tehran"))
        paylaod = {
            "username": username,
            "jti": jti,
            "iat": datetime.now(),
            "exp": now + timedelta(days=access_key_expire_time),
        }

        access_token = jwt.encode(payload=paylaod, key=secret_key, algorithm="HS256")
        return access_token

    def generate_refresh_token(
        self, jti, username, refresh_key_expire_time, secret_key
    ):
        now = datetime.now(tz=pytz.timezone("Asia/Tehran"))
        paylaod = {
            "username": username,
            "jti": jti,
            "iat": datetime.now(),
            "exp": now + timedelta(days=refresh_key_expire_time),
        }

        access_token = jwt.encode(payload=paylaod, key=secret_key, algorithm="HS256")
        return access_token

    def generate_access_and_refresh_token(
        self, username, access_key_expire_time, refresh_key_expire_time, secret_key
    ):
        jti = self.jti
        access_token = self.generate_access_token(
            jti, username, access_key_expire_time, secret_key
        )
        refresh_token = self.generate_refresh_token(
            jti, username, refresh_key_expire_time, secret_key
        )
        return access_token, refresh_token, jti

    def decode_refresh_token(self, refresh_token, secret_key):
        payload = jwt.decode(refresh_token, key=secret_key, algorithms="HS256")
        jti = payload.get("jti")
        username = payload.get("username")
        return jti, username

    def get_token_from_header(self, header):
        access_token = header.split(" ")[1]
        return access_token


jwt_authentication = JwtAuthentication()
