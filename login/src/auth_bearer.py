from jose import jwt
from jose.exceptions import JWEInvalidAuth
from jwt.exceptions import InvalidKeyTypeError
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import TokenTable


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 Minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 DAYS
ALGORITHM = "HS256"
JWT_SECRET_KEY = "TEST3062024KEY"
JWT_REFRESH_SECRET_KEY = "resfrescandoclavesecreta3062024"



def decodeJWT(jwtoken: str):
    try:
        # Decode and verify the token
        payload = jwt.decode(jwtoken, JWT_SECRET_KEY, ALGORITHM)
        print(payload)
        return payload
    except JWEInvalidAuth:
        raise HTTPException(
            status_code=403,
            detail="Invalid decoding"
        )


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):

        super(JWTBearer, self).__init__(auto_error=auto_error)

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403,
                    detail="Invalid authentication scheme."
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(
                    status_code=403,
                    detail="Invalid token or expired token."
                )
            else:
                raise HTTPException(status_code=403, detail="Invalid authorization code.")



jwt_bearer = JWTBearer()