from fastapi import FastAPI, Depends, Security
from fastapi.security import APIKeyHeader

app = FastAPI()
API_KEY = ""

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

@app.on_event("startup")
async def startup():
    if not API_KEY:
        print("Refusing to start")
        import sys
        sys.exit(1)
