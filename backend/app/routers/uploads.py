from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Image, Lesion, Observation, User
from ..services.ml_service import get_detector_service


router = APIRouter(prefix="/upload", tags=["uploads"])

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("")
async def upload_and_register(
    file: UploadFile = File(...),
    user_external_id: Optional[str] = Form(None),
    body_site: Optional[str] = Form(None),
    notes: Optional[str] = Form(None),
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db),
) -> dict:
    """
    Upload an image, run detection, and register a lesion + observation.
    Returns IDs that can be used in the timeline.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    contents = await file.read()

    # Upsert user
    user: Optional[User] = None
    if user_external_id:
        user = db.query(User).filter_by(external_id=user_external_id).first()
    if user is None:
        user = User(external_id=user_external_id)
        db.add(user)
        db.flush()

    lesion = Lesion(user_id=user.id, body_site=body_site, notes=notes)
    db.add(lesion)
    db.flush()

    detector = get_detector_service()
    pred = detector.predict_image_bytes(contents, metadata=metadata)
    top = pred.get("top_class") or {}

    obs = Observation(
        lesion_id=lesion.id,
        captured_at=datetime.utcnow(),
        top_class=top.get("label"),
        top_prob=float(top.get("probability", 0.0)),
        raw_metadata_json=metadata,
    )
    db.add(obs)
    db.flush()

    # Store file path for later retrieval
    filename = f"lesion{lesion.id}_obs{obs.id}_{file.filename}"
    save_path = UPLOAD_DIR / filename
    save_path.write_bytes(contents)
    img = Image(observation_id=obs.id, file_path=str(save_path))
    db.add(img)
    db.commit()

    return {
        "status": "ok",
        "user_id": user.id,
        "lesion_id": lesion.id,
        "observation_id": obs.id,
        "top_class": top,
    }