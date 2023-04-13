from google.auth.transport import requests
from google.oauth2 import id_token
from starlette.requests import Request
from configs import Config

# TODO: Does Google's verify_auth2_token() function retreive Google's certs every time the function is called? Is there any way to cache the response?


async def get_email(request: Request):
    try:
        print('came here')
        token = request.headers.get("Authorization")
        # print(token)
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), Config.GOOGLE_CLIENT_ID
        )
        email = idinfo["email"]
        return email

    except ValueError:
        return None
