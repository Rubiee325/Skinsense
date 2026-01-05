import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

from ..ml.detector import DetectorModel
from ..ml.predictor import SkinMorphPredictor
from ..ml.recommendations import RecommendationEngine


@lru_cache(maxsize=1)
def get_detector_service() -> DetectorModel:
    return DetectorModel()


@lru_cache(maxsize=1)
def get_predictor_service() -> SkinMorphPredictor:
    return SkinMorphPredictor()


@lru_cache(maxsize=1)
def get_recommendation_service() -> RecommendationEngine:
    return RecommendationEngine()


def parse_metadata(metadata_json: Optional[str]) -> Dict[str, Any]:
    if not metadata_json:
        return {}
    try:
        return json.loads(metadata_json)
    except json.JSONDecodeError:
        return {}






