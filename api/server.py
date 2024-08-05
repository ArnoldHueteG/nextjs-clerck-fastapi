
import requests # <- (1)
from fastapi import FastAPI, Depends, Response, status # <- (2)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
import jwt

CLERK_PEM_PUBLIC_KEY = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA+9X2miCmNk3+4w9Dmgph
5Ls4GUiOuJzG627a1LrwEROAJAs4G6i2U8oFoft11LwhG4Z+lqn0pzr4skhgZic9
fn+p4hpcZnl7kCwD0FIiqxV9BhDDQvJmiqRVA5oGb6rxZXyIUjcZN9x1CjkvtkK0
q3XV/URammRNJKSarD3Ql85JlshvwY7QVg1GX0iyMVqChKuxdU/yNeDgawwAQIYM
2vZtz2prEbF3xVra1zZD8AEeZ0S34Ss2Aqrpe3hzzVZ3D6LnNtQC8Yp8MRucuzGN
826ilYAP1JAO21VhDfwjD7ctWjsEHUWOPBW1CYIimiPC3/M9zaA0DJGhZ7YBRICU
TwIDAQAB
-----END PUBLIC KEY-----
""" # <- (3)

app = FastAPI()
security = HTTPBearer()

@app.get("/")
async def root(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    response: Response # <- (4)
):
    print(f"Got token: {credentials.credentials[:10]}...")

    # (5) add all this section below
    try:
        token = credentials.credentials
        jwt.decode(token, key=CLERK_PEM_PUBLIC_KEY, algorithms=['RS256'])
        return {"message": "Hello World"}
    except jwt.exceptions.PyJWTError:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "Invalid token"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)