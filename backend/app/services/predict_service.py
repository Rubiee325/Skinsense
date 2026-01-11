from datetime import datetime
from typing import Dict, Any, List, Optional
from ..services.ml_service import get_detector_service
from ..services.disease_info_service import (
    get_disease_info,
    get_severity_from_confidence,
    DiseaseInfo,
    SeverityLevel
)

# Model version (should match your deployed model version)
MODEL_VERSION = "1.0.0"


def enrich_prediction_with_medical_info(
    detector_output: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Enrich raw detector output with comprehensive medical information.
    Returns medical-grade prediction response.
    """
    top_class = detector_output.get("top_class", {})
    predicted_disease = top_class.get("label", "unknown")
    confidence = top_class.get("probability", 0.0)
    top_3_raw = detector_output.get("top_3_predictions", [])
    is_invalid_image = detector_output.get("is_invalid_image", False)
    
    # Get disease information
    disease_info = get_disease_info(predicted_disease)
    
    # If no disease info found, use default/unknown info
    if not disease_info:
        disease_info = DiseaseInfo(
            disease_name=predicted_disease.replace("_", " ").title(),
            description="Information not available for this condition.",
            common_symptoms=["Consult a dermatologist for detailed symptoms"],
            possible_causes=["Consult a dermatologist for potential causes"],
            precautions=["Consult a dermatologist for personalized care"],
            recommended_next_steps="Please consult a dermatologist for professional evaluation and treatment recommendations.",
            default_severity=SeverityLevel.MILD
        )
    
    # Determine severity based on confidence and disease type
    severity = get_severity_from_confidence(confidence, disease_info.default_severity)
    
    # Format top-3 predictions with disease names
    top_3_predictions = []
    for pred in top_3_raw:
        pred_disease = pred.get("label", "unknown")
        pred_confidence = pred.get("probability", 0.0)
        pred_info = get_disease_info(pred_disease)
        disease_name = pred_info.disease_name if pred_info else pred_disease.replace("_", " ").title()
        
        top_3_predictions.append({
            "disease": disease_name,
            "disease_code": pred_disease,
            "confidence": round(pred_confidence, 4)
        })
    
    # Build comprehensive response
    response = {
        "predicted_disease": disease_info.disease_name,
        "predicted_disease_code": predicted_disease,
        "confidence": round(confidence, 4),
        "top_predictions": top_3_predictions,
        "severity_level": severity.value,
        "disease_description": disease_info.description,
        "common_symptoms": disease_info.common_symptoms,
        "possible_causes": disease_info.possible_causes,
        "precautions": disease_info.precautions,
        "recommended_next_steps": disease_info.recommended_next_steps,
        "model_version": MODEL_VERSION,
        "prediction_time": datetime.utcnow().isoformat(),
        "medical_disclaimer": "This is not a medical diagnosis. This AI system is for informational purposes only and should not replace professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition.",
        "is_invalid_image": is_invalid_image,
        "confidence_threshold": detector_output.get("confidence_threshold", 0.3),
        "gradcam_overlay_png_b64": detector_output.get("gradcam_overlay_png_b64")
    }
    
    return response


def predict_skin_disease(
    image_bytes: bytes,
    metadata: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main prediction function that:
    1. Runs the detector model
    2. Enriches output with medical information
    3. Returns medical-grade response
    """
    detector = get_detector_service()
    raw_output = detector.predict_image_bytes(image_bytes, metadata=metadata)
    enriched_output = enrich_prediction_with_medical_info(raw_output)
    return enriched_output

