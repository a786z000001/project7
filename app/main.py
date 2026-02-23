from fastapi import FastAPI
from app.api.routes import router
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}
