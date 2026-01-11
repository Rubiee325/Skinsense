from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from ..core.dependencies import get_current_user
from ..services.prediction_storage_service import (
    get_user_predictions,
    get_user_prediction_stats
)


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


class PredictionHistoryItem(BaseModel):
    """Individual prediction history item."""
    id: str = Field(..., description="Prediction ID")
    predicted_disease: str
    predicted_disease_code: str
    confidence: float
    severity: str
    image_name: str
    top_3_predictions: List[dict]
    model_version: str = Field(..., alias="model_version", description="Model version used for prediction")
    is_invalid_image: bool
    created_at: str
    
    model_config = {"protected_namespaces": ()}


class DashboardResponse(BaseModel):
    """Dashboard response with prediction history and stats."""
    predictions: List[dict]
    total_count: int
    stats: dict


class PredictionStatsResponse(BaseModel):
    """Prediction statistics response."""
    total_predictions: int
    predictions_by_disease: dict


@router.get("/predictions", response_model=DashboardResponse)
async def get_dashboard(
    current_user: dict = Depends(get_current_user),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of predictions to return"),
    skip: int = Query(0, ge=0, description="Number of predictions to skip for pagination")
):
    """
    Get user's prediction history dashboard.
    Requires authentication.
    Returns recent predictions with pagination support.
    """
    try:
        user_id = current_user.get("_id") or current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid user")
        
        # Get predictions
        predictions = await get_user_predictions(user_id, limit=limit, skip=skip)
        
        # Get stats
        stats = await get_user_prediction_stats(user_id)
        
        return DashboardResponse(
            predictions=predictions,
            total_count=stats.get("total_predictions", 0),
            stats=stats
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch dashboard data: {str(e)}"
        )


@router.get("/stats", response_model=PredictionStatsResponse)
async def get_prediction_stats(
    current_user: dict = Depends(get_current_user)
):
    """
    Get prediction statistics for the logged-in user.
    Includes total predictions and breakdown by disease.
    """
    try:
        user_id = current_user.get("_id") or current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid user")
            
        stats = await get_user_prediction_stats(user_id)
        
        return PredictionStatsResponse(
            total_predictions=stats.get("total_predictions", 0),
            predictions_by_disease=stats.get("predictions_by_disease", {})
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch statistics: {str(e)}"
        )


@router.get("/recent")
async def get_recent_predictions(
    current_user: dict = Depends(get_current_user),
    count: int = Query(10, ge=1, le=50, description="Number of recent predictions to return")
):
    """
    Get most recent predictions for the logged-in user.
    """
    try:
        user_id = current_user.get("_id") or current_user.get("id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid user")
            
        predictions = await get_user_predictions(user_id, limit=count, skip=0)
        
        return {
            "recent_predictions": predictions,
            "count": len(predictions)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch recent predictions: {str(e)}"
        )

