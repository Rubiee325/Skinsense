from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from ..core.dependencies import get_current_user
from ..db import get_database
from ..services.prediction_storage_service import get_user_predictions

router = APIRouter(prefix="/dermatologist", tags=["dermatologist"])


class PatientInfo(BaseModel):
    id: str
    name: str
    email: str
    age: int
    gender: str


@router.get("/patients", response_model=List[PatientInfo])
async def get_patients(current_user: dict = Depends(get_current_user)):
    """
    Get a list of all patients.
    Only dermatologists should ideally access this, but for the prototype 
    we allow any authenticated user with the 'dermatologist' role.
    """
    if current_user.get("role") != "dermatologist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only dermatologists can access this information"
        )
    
    db = get_database()
    patients_cursor = db.users.find({"role": "patient"})
    
    patients = []
    async for doc in patients_cursor:
        doc["id"] = str(doc["_id"])
        patients.append(PatientInfo(**doc))
    
    return patients


@router.get("/patient/{patient_id}/predictions")
async def get_patient_predictions(patient_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get prediction history for a specific patient.
    Requires dermatologist role.
    """
    if current_user.get("role") != "dermatologist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only dermatologists can access this information"
        )
    
    predictions = await get_user_predictions(patient_id)
    return {
        "predictions": predictions,
        "count": len(predictions)
    }
