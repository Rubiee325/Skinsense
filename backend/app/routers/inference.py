from typing import List, Optional

from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
from sanity_check import is_skin_image_from_bytes


from ..services.ml_service import (
    get_detector_service,
    get_predictor_service,
    get_recommendation_service,
)


router = APIRouter(prefix="", tags=["inference"])


class PredictRequest(BaseModel):
    metadata: Optional[dict] = None


class SequenceItem(BaseModel):
    timestamp: str
    metadata: Optional[dict] = None


class PredictSequenceRequest(BaseModel):
    history: List[SequenceItem]


@router.post("/predict")
async def predict(
    file: UploadFile = File(...),
    metadata: Optional[str] = None,
) -> dict:
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    detector = get_detector_service()
    rec_engine = get_recommendation_service()

    contents = await file.read()

    # 🛑 ADD THIS BLOCK (SKIN VALIDATION)
    if not is_skin_image_from_bytes(contents):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid skin image"
        )

    # ✅ EXISTING CODE (UNCHANGED)
    result = detector.predict_image_bytes(contents, metadata=metadata)
    recs = rec_engine.get_recommendations(result)
    return {"prediction": result, "recommendations": recs}



@router.post("/predict_sequence")
async def predict_sequence(
    files: List[UploadFile] = File(...),
    metadata: Optional[str] = None,
    timestamps: Optional[str] = None,
) -> dict:
    if any(not f.content_type.startswith("image/") for f in files):
        raise HTTPException(status_code=400, detail="All files must be images")

    predictor = get_predictor_service()
    contents_list = [await f.read() for f in files]
    result = predictor.predict_sequence_bytes(
        contents_list, metadata_json=metadata, timestamps=timestamps
    )
    return result






