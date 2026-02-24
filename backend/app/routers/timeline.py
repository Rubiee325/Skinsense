from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Lesion, Observation


router = APIRouter(prefix="/timeline", tags=["timeline"])


@router.get("")
async def get_timeline(user_id: int | None = None, db: Session = Depends(get_db)) -> dict:
    """
    Return a simple longitudinal view of lesions and their observations.
    """
    q = db.query(Lesion)
    if user_id is not None:
        q = q.filter(Lesion.user_id == user_id)
    lesions = q.all()

    lesion_payload = []
    for lesion in lesions:
        events = []
        for obs in sorted(lesion.observations, key=lambda o: o.captured_at):
            events.append(
                {
                    "observation_id": obs.id,
                    "captured_at": obs.captured_at.isoformat(),
                    "top_class": obs.top_class,
                    "top_prob": obs.top_prob,
                }
            )
        lesion_payload.append(
            {
                "lesion_id": lesion.id,
                "user_id": lesion.user_id,
                "body_site": lesion.body_site,
                "notes": lesion.notes,
                "events": events,
            }
        )

    return {"user_id": user_id, "lesions": lesion_payload}