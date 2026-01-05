from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List


RULES_PATH = Path(__file__).with_name("recommendation_rules.json")


def _load_rules() -> List[Dict[str, Any]]:
    if RULES_PATH.exists():
        try:
            return json.loads(RULES_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    # Fallback minimal rules if JSON is missing or invalid
    return [
        {
            "id": "default_general",
            "if_top_class": None,
            "min_prob": 0.0,
            "recommendations": [],
        }
    ]


RULES: List[Dict[str, Any]] = _load_rules()


@dataclass
class RecommendationEngine:
    def get_recommendations(
        self, detector_output: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        top = detector_output.get("top_class") or {}
        label = top.get("label")
        prob = float(top.get("probability", 0.0))

        recs: List[Dict[str, Any]] = []
        for rule in RULES:
            target = rule.get("if_top_class")
            if target is not None and target != label:
                continue
            if prob >= float(rule.get("min_prob", 0.0)):
                recs.extend(rule.get("recommendations", []))

        if not recs:
            recs.append(
                {
                    "title": "General skin health guidance",
                    "summary": "Use daily broad-spectrum SPF 30+ sunscreen and monitor lesions for change in size, shape, or color.",
                    "evidence_level": "B",
                    "when_to_see_doctor": "If any lesion changes rapidly, bleeds, or is painful.",
                }
            )

        return recs


