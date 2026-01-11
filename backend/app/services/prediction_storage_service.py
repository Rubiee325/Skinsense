from datetime import datetime
from typing import Dict, Any, Optional, List
from bson import ObjectId

from ..db import get_database


async def save_prediction(
    user_id: str,
    prediction_result: Dict[str, Any],
    image_filename: str
) -> str:
    """
    Save a prediction to MongoDB.
    Returns the prediction document ID.
    """
    db = get_database()
    predictions_collection = db["predictions"]
    
    # Extract relevant information from prediction result
    prediction_doc = {
        "user_id": user_id,
        "predicted_disease": prediction_result.get("predicted_disease", ""),
        "predicted_disease_code": prediction_result.get("predicted_disease_code", ""),
        "confidence": prediction_result.get("confidence", 0.0),
        "severity": prediction_result.get("severity_level", ""),
        "image_name": image_filename,
        "top_3_predictions": prediction_result.get("top_predictions", []),
        "model_version": prediction_result.get("model_version", ""),
        "is_invalid_image": prediction_result.get("is_invalid_image", False),
        "created_at": datetime.utcnow().isoformat()
    }
    
    result = await predictions_collection.insert_one(prediction_doc)
    return str(result.inserted_id)


async def get_user_predictions(
    user_id: str,
    limit: int = 50,
    skip: int = 0
) -> List[Dict[str, Any]]:
    """
    Get prediction history for a specific user.
    Returns list of predictions sorted by most recent first.
    """
    db = get_database()
    predictions_collection = db["predictions"]
    
    # Query predictions for this user, sorted by created_at descending
    cursor = predictions_collection.find(
        {"user_id": user_id}
    ).sort("created_at", -1).skip(skip).limit(limit)
    
    predictions = []
    async for doc in cursor:
        # Convert MongoDB _id to id for JSON serialization and Pydantic compatibility
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
        predictions.append(doc)
    
    return predictions


async def get_prediction_by_id(
    prediction_id: str,
    user_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Get a specific prediction by ID.
    If user_id is provided, ensures the prediction belongs to that user.
    """
    db = get_database()
    predictions_collection = db["predictions"]
    
    query = {"_id": ObjectId(prediction_id)}
    if user_id:
        query["user_id"] = user_id
    
    doc = await predictions_collection.find_one(query)
    if doc:
        # Convert MongoDB _id to id for JSON serialization and Pydantic compatibility
        doc["id"] = str(doc["_id"])
        doc.pop("_id", None)
    return doc


async def get_user_prediction_stats(user_id: str) -> Dict[str, Any]:
    """
    Get statistics about user's predictions.
    """
    db = get_database()
    predictions_collection = db["predictions"]
    
    # Count total predictions
    total_count = await predictions_collection.count_documents({"user_id": user_id})
    
    # Count predictions by disease
    pipeline = [
        {"$match": {"user_id": user_id}},
        {"$group": {
            "_id": "$predicted_disease",
            "count": {"$sum": 1}
        }},
        {"$sort": {"count": -1}}
    ]
    
    disease_counts = {}
    async for doc in predictions_collection.aggregate(pipeline):
        disease_counts[doc["_id"]] = doc["count"]
    
    return {
        "total_predictions": total_count,
        "predictions_by_disease": disease_counts
    }

