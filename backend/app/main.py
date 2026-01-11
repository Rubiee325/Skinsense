from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# app/main.py
from sanity_check import is_skin_image
import cv2
from .routers import inference, timeline, uploads, reports
from .db import Base, engine


def create_app() -> FastAPI:
    app = FastAPI(
        title="SkinMorph API",
        version="0.1.0",
        description="Skin disease detection, prediction, and recommendations prototype.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # For SQLite/local dev we auto-create tables.
    # For production/PostgreSQL, prefer Alembic migrations instead.
    Base.metadata.create_all(bind=engine)

    @app.get("/health")
    async def health() -> dict:
        return {"status": "ok"}

    app.include_router(inference.router)
    app.include_router(timeline.router)
    app.include_router(uploads.router)
    app.include_router(reports.router)

    return app


app = create_app()
def predict_image(image_path):
    image = cv2.imread(image_path)

    # 🔴 ADD THIS BLOCK
    if not is_skin_image(image):
        return {
            "status": "error",
            "message": "Uploaded image is not skin-related. Please upload a valid skin image."
        }

    # ✅ EXISTING CODE (UNCHANGED)
    result = run_skin_disease_prediction(image)
    return {
        "status": "success",
        "prediction": result
    }




