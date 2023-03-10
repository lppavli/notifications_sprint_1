import logging
from http import HTTPStatus

import jwt
from fastapi import HTTPException


class Auth:

    def decode_token(self, token):
        try:
            payload = jwt.decode(
                token,
                "top_secret",
                algorithms="HS256",
                options={"verify_signature": False},
            )
            logging.info(payload)
            if payload["sub"]:
                return payload["sub"]
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Scope for the token is invalid",
            )
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Token expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid token"
            )