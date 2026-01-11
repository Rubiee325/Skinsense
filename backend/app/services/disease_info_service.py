from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class SeverityLevel(str, Enum):
    MILD = "Mild"
    MODERATE = "Moderate"
    SEVERE = "Severe"


@dataclass
class DiseaseInfo:
    """Medical information for a skin disease."""
    disease_name: str
    description: str
    common_symptoms: List[str]
    possible_causes: List[str]
    precautions: List[str]
    recommended_next_steps: str
    default_severity: SeverityLevel


# Comprehensive disease information mapping
DISEASE_INFO_MAP: Dict[str, DiseaseInfo] = {
    "benign_nevus": DiseaseInfo(
        disease_name="Benign Nevus (Mole)",
        description="A benign nevus is a common mole that is typically harmless. Most people have between 10-40 moles on their body. They can be flat or raised, round or oval, and vary in color from pink to dark brown.",
        common_symptoms=["Pigmented spot on skin", "Round or oval shape", "Uniform color", "Small size (<6mm typically)", "Stable appearance"],
        possible_causes=["Genetic factors", "Sun exposure", "Hormonal changes", "Age"],
        precautions=["Regular monitoring for changes (ABCDE rule)", "Use sunscreen SPF 30+", "Avoid excessive sun exposure", "Regular dermatological check-ups"],
        recommended_next_steps="Monitor for changes in size, shape, color, or texture. See a dermatologist if any changes occur or if you notice new moles after age 30.",
        default_severity=SeverityLevel.MILD
    ),
    "melanoma_suspect": DiseaseInfo(
        disease_name="Suspicious Melanoma",
        description="Melanoma is a serious form of skin cancer that develops in melanocytes (pigment-producing cells). Early detection is crucial for successful treatment. Suspicious lesions should be evaluated by a dermatologist immediately.",
        common_symptoms=["Asymmetric shape", "Irregular borders", "Color variation", "Diameter >6mm", "Evolution over time", "Irregular texture"],
        possible_causes=["UV radiation exposure", "Genetic predisposition", "History of sunburns", "Multiple atypical moles", "Weakened immune system"],
        precautions=["Immediate dermatological consultation required", "Avoid sun exposure", "Use high SPF sunscreen", "Regular full-body skin exams", "Avoid tanning beds"],
        recommended_next_steps="URGENT: Consult a dermatologist immediately for professional evaluation, biopsy if indicated, and follow-up care. Early detection significantly improves treatment outcomes.",
        default_severity=SeverityLevel.SEVERE
    ),
    "seborrheic_keratosis": DiseaseInfo(
        disease_name="Seborrheic Keratosis",
        description="Seborrheic keratosis are benign, non-cancerous growths that appear as waxy, scaly, slightly elevated lesions. They are very common, especially in older adults, and do not require treatment unless they cause discomfort or cosmetic concerns.",
        common_symptoms=["Waxy appearance", "Raised texture", "Stuck-on appearance", "Brown, black, or tan color", "Scaly surface", "Common on face, chest, shoulders, back"],
        possible_causes=["Age-related", "Genetic factors", "Sun exposure (possible association)", "Hormonal changes"],
        precautions=["No treatment necessary unless symptomatic", "Avoid picking or scratching", "Monitor for changes", "Sun protection"],
        recommended_next_steps="These are benign and typically do not require treatment. If they become irritated, change significantly, or you want them removed for cosmetic reasons, consult a dermatologist.",
        default_severity=SeverityLevel.MILD
    ),
    "acne": DiseaseInfo(
        disease_name="Acne Vulgaris",
        description="Acne is a common skin condition characterized by pimples, blackheads, whiteheads, and sometimes deeper nodules or cysts. It occurs when hair follicles become clogged with oil and dead skin cells, often triggered by hormonal changes.",
        common_symptoms=["Pimples", "Blackheads (open comedones)", "Whiteheads (closed comedones)", "Red, inflamed bumps", "Pustules", "Nodules or cysts (in severe cases)", "Oily skin"],
        possible_causes=["Hormonal changes (puberty, menstruation, pregnancy)", "Excess oil production", "Dead skin cells", "Bacteria (Propionibacterium acnes)", "Clogged pores", "Genetics", "Certain medications", "Diet (debated)"],
        precautions=["Gentle cleansing twice daily", "Avoid picking or squeezing", "Use non-comedogenic products", "Avoid excessive washing", "Keep skin moisturized", "Avoid harsh scrubs", "Change pillowcases regularly"],
        recommended_next_steps="Mild acne can often be managed with over-the-counter treatments containing benzoyl peroxide or salicylic acid. If acne is moderate to severe, persistent, or causing scarring, consult a dermatologist for prescription treatments.",
        default_severity=SeverityLevel.MODERATE
    ),
    "eczema": DiseaseInfo(
        disease_name="Eczema (Atopic Dermatitis)",
        description="Eczema is a chronic inflammatory skin condition characterized by dry, itchy, and inflamed skin. It often occurs in flare-ups and can significantly impact quality of life. It's most common in children but can persist into adulthood.",
        common_symptoms=["Dry, itchy skin", "Red or brownish-gray patches", "Small raised bumps that may leak fluid", "Thickened, cracked skin", "Raw, sensitive skin from scratching", "Areas commonly affected: face, hands, feet, inside of elbows/knees"],
        possible_causes=["Genetic factors", "Immune system dysfunction", "Environmental triggers", "Dry skin", "Irritants (soaps, detergents)", "Allergens", "Stress", "Weather changes", "Skin barrier dysfunction"],
        precautions=["Moisturize regularly (especially after bathing)", "Use mild, fragrance-free products", "Avoid triggers", "Wear soft, breathable fabrics", "Avoid scratching (use cold compresses)", "Keep nails short", "Humidify air in dry climates"],
        recommended_next_steps="Use emollients regularly and identify triggers. Over-the-counter hydrocortisone cream may help mild cases. For persistent or severe eczema, consult a dermatologist for prescription treatments including topical corticosteroids, calcineurin inhibitors, or systemic medications.",
        default_severity=SeverityLevel.MODERATE
    ),
    "psoriasis": DiseaseInfo(
        disease_name="Psoriasis",
        description="Psoriasis is a chronic autoimmune condition that causes rapid skin cell turnover, leading to thick, scaly, red patches of skin. It's a systemic condition that can affect joints (psoriatic arthritis) and has associations with other health conditions.",
        common_symptoms=["Red patches covered with silvery scales", "Dry, cracked skin that may bleed", "Itching, burning, or soreness", "Thickened nails", "Swollen and stiff joints (psoriatic arthritis)", "Common locations: elbows, knees, scalp, lower back"],
        possible_causes=["Autoimmune dysfunction", "Genetic predisposition", "Immune system triggers", "Stress", "Infections", "Skin injuries", "Certain medications", "Weather changes"],
        precautions=["Moisturize regularly", "Avoid scratching", "Use gentle, fragrance-free products", "Protect skin from injury", "Manage stress", "Avoid smoking and excessive alcohol", "Sun exposure (in moderation, with doctor approval)"],
        recommended_next_steps="Consult a dermatologist for diagnosis and treatment plan. Treatment options include topical corticosteroids, vitamin D analogs, light therapy, systemic medications, and biologics. Treatment depends on severity and patient factors.",
        default_severity=SeverityLevel.MODERATE
    ),
    "rosacea": DiseaseInfo(
        disease_name="Rosacea",
        description="Rosacea is a chronic inflammatory skin condition primarily affecting the face, characterized by persistent redness, visible blood vessels, and sometimes pimple-like bumps. It tends to worsen over time without treatment and has distinct subtypes.",
        common_symptoms=["Facial redness (especially cheeks, nose, chin, forehead)", "Visible blood vessels (telangiectasia)", "Bumps and pimples", "Eye irritation (ocular rosacea)", "Thickened skin on nose (rhinophyma, in advanced cases)", "Burning or stinging sensation", "Dry, sensitive skin"],
        possible_causes=["Genetic predisposition", "Abnormal blood vessel function", "Demodex mites", "Helicobacter pylori infection (possible link)", "Immune system response", "Environmental factors"],
        precautions=["Identify and avoid triggers (spicy foods, alcohol, heat, sun, stress)", "Use gentle, fragrance-free skincare", "Protect from sun (SPF 30+, physical blockers)", "Avoid harsh scrubs and hot water", "Keep skin cool", "Use green-tinted makeup to neutralize redness"],
        recommended_next_steps="Consult a dermatologist for proper diagnosis and treatment. Treatment may include topical medications (metronidazole, azelaic acid), oral antibiotics for moderate-severe cases, laser therapy for visible vessels, and long-term management strategies.",
        default_severity=SeverityLevel.MODERATE
    ),
    "not_skin": DiseaseInfo(
        disease_name="Not Skin / Invalid Image",
        description="The uploaded image does not appear to be a valid skin lesion image. The model cannot provide a reliable prediction for non-skin images or images that don't clearly show a skin condition.",
        common_symptoms=["Image quality too low", "No clear skin lesion visible", "Image may show non-skin objects", "Insufficient detail for analysis"],
        possible_causes=["Poor image quality", "Incorrect image type", "Image doesn't contain skin", "Image too blurry or out of focus", "Improper lighting or angle"],
        precautions=["Ensure good lighting when capturing images", "Take clear, focused photos", "Capture skin at appropriate distance", "Ensure image contains visible skin lesion", "Use high-resolution camera if available"],
        recommended_next_steps="Please retake the image with better lighting, focus, and ensure it clearly shows the skin condition. If you have concerns about a skin condition, consult a dermatologist directly for professional evaluation.",
        default_severity=SeverityLevel.MILD
    ),
    # Additional expanded diseases
    "actinic_keratosis": DiseaseInfo(
        disease_name="Actinic Keratosis",
        description="Actinic keratosis are rough, scaly patches on skin caused by years of sun exposure. They are considered precancerous lesions that can develop into squamous cell carcinoma if left untreated.",
        common_symptoms=["Rough, scaly patches", "Flat or slightly raised", "Color varies (pink, red, brown)", "Common on sun-exposed areas", "May itch or burn"],
        possible_causes=["Cumulative sun exposure", "UV radiation damage", "Fair skin", "Age (more common in older adults)", "Weakened immune system"],
        precautions=["Sun protection (SPF 30+)", "Wear protective clothing", "Avoid peak sun hours", "Regular dermatological monitoring", "Early treatment recommended"],
        recommended_next_steps="Consult a dermatologist for evaluation and treatment. Options include cryotherapy, topical medications (5-FU, imiquimod), photodynamic therapy, or surgical removal depending on the lesion.",
        default_severity=SeverityLevel.MODERATE
    ),
    "basal_cell_carcinoma": DiseaseInfo(
        disease_name="Basal Cell Carcinoma",
        description="Basal cell carcinoma is the most common type of skin cancer. It grows slowly and rarely spreads, but should be treated promptly to prevent local damage and disfigurement.",
        common_symptoms=["Pearly or waxy bump", "Flat, flesh-colored or brown scar-like lesion", "Bleeding or scabbing sore that heals and returns", "Common on sun-exposed areas"],
        possible_causes=["UV radiation exposure", "Fair skin", "Age", "History of sunburns", "Chronic sun exposure"],
        precautions=["Sun protection essential", "Regular skin checks", "Early treatment", "Monitor for changes", "Avoid tanning beds"],
        recommended_next_steps="URGENT: Consult a dermatologist immediately. Treatment options include surgical excision, Mohs surgery, cryotherapy, or topical medications depending on the lesion size and location.",
        default_severity=SeverityLevel.SEVERE
    ),
    "squamous_cell_carcinoma": DiseaseInfo(
        disease_name="Squamous Cell Carcinoma",
        description="Squamous cell carcinoma is the second most common skin cancer. It can be more aggressive than basal cell carcinoma and has a higher risk of spreading if not treated early.",
        common_symptoms=["Firm, red nodule", "Flat lesion with scaly, crusted surface", "Sore that doesn't heal", "Wart-like growth", "Common on sun-exposed areas"],
        possible_causes=["UV radiation exposure", "Fair skin", "Chronic sun exposure", "History of actinic keratosis", "Weakened immune system"],
        precautions=["Sun protection essential", "Early detection and treatment", "Regular dermatological exams", "Monitor all skin lesions", "Avoid tanning"],
        recommended_next_steps="URGENT: Consult a dermatologist immediately. Treatment typically involves surgical removal. The method depends on size, location, and depth of the lesion. Early treatment is critical.",
        default_severity=SeverityLevel.SEVERE
    ),
    "dermatitis": DiseaseInfo(
        disease_name="Contact Dermatitis",
        description="Contact dermatitis is skin inflammation caused by direct contact with an irritant or allergen. It can be either irritant (from chemicals/substances) or allergic (immune system reaction).",
        common_symptoms=["Red rash", "Itching", "Dry, cracked skin", "Blisters (in severe cases)", "Burning or tenderness", "Swelling"],
        possible_causes=["Irritants (soaps, detergents, solvents)", "Allergens (nickel, fragrances, preservatives)", "Plants (poison ivy, oak)", "Latex", "Cosmetics", "Medications"],
        precautions=["Identify and avoid triggers", "Use gentle, fragrance-free products", "Wear gloves when handling irritants", "Moisturize regularly", "Avoid scratching"],
        recommended_next_steps="Identify and eliminate the trigger. Over-the-counter hydrocortisone cream and antihistamines may help. For persistent or severe cases, consult a dermatologist or allergist for patch testing and prescription treatment.",
        default_severity=SeverityLevel.MILD
    ),
    "urticaria": DiseaseInfo(
        disease_name="Urticaria (Hives)",
        description="Urticaria are raised, itchy welts on the skin that appear suddenly and can vary in size. They're often caused by an allergic reaction but can also occur from other triggers.",
        common_symptoms=["Raised, red welts", "Itching", "Appear and disappear quickly", "Vary in size", "May join together", "Can occur anywhere on body"],
        possible_causes=["Allergic reactions", "Foods", "Medications", "Insect stings", "Infections", "Stress", "Temperature changes", "Pressure on skin"],
        precautions=["Identify triggers", "Avoid known allergens", "Antihistamines", "Cool compresses", "Avoid scratching", "Wear loose clothing"],
        recommended_next_steps="Over-the-counter antihistamines can help. For chronic or severe hives, consult a doctor or allergist. If hives are accompanied by difficulty breathing or swelling of face/throat, seek emergency medical attention immediately.",
        default_severity=SeverityLevel.MILD
    ),
    "seborrheic_dermatitis": DiseaseInfo(
        disease_name="Seborrheic Dermatitis",
        description="Seborrheic dermatitis is a common inflammatory skin condition that causes scaly patches, red skin, and stubborn dandruff. It commonly affects oily areas of the body like the scalp, face, and chest.",
        common_symptoms=["Scaly patches", "Red skin", "Dandruff", "Itchy scalp or skin", "Oily or greasy patches", "Yellow or white flakes", "Common on scalp, eyebrows, sides of nose"],
        possible_causes=["Yeast (Malassezia)", "Oily skin", "Hormonal changes", "Stress", "Cold, dry weather", "Certain medical conditions", "Weakened immune system"],
        precautions=["Use anti-dandruff shampoo", "Wash regularly", "Avoid harsh soaps", "Manage stress", "Protect from cold weather", "Use gentle skincare"],
        recommended_next_steps="Over-the-counter anti-dandruff shampoos (containing ketoconazole, selenium sulfide, or zinc pyrithione) can help. For persistent or severe cases, consult a dermatologist for prescription-strength treatments.",
        default_severity=SeverityLevel.MILD
    ),
    "tinea": DiseaseInfo(
        disease_name="Tinea (Fungal Infection)",
        description="Tinea is a fungal infection of the skin that can affect various parts of the body (ringworm, athlete's foot, jock itch). It's contagious and thrives in warm, moist environments.",
        common_symptoms=["Red, scaly ring-shaped rash", "Itching", "Clear center with raised edges", "Blistering (in some cases)", "Location depends on type (body, feet, groin, scalp)"],
        possible_causes=["Fungal infection (dermatophytes)", "Warm, moist environments", "Direct contact with infected person/animal", "Sharing towels or clothing", "Poor hygiene", "Weakened immune system"],
        precautions=["Keep skin dry and clean", "Don't share towels or clothing", "Wear breathable fabrics", "Avoid walking barefoot in public areas", "Change clothes and socks regularly", "Use antifungal powders"],
        recommended_next_steps="Over-the-counter antifungal creams (clotrimazole, miconazole) usually effective for mild cases. For persistent, severe, or widespread infections, consult a doctor for oral antifungal medications.",
        default_severity=SeverityLevel.MILD
    ),
    "vitiligo": DiseaseInfo(
        disease_name="Vitiligo",
        description="Vitiligo is a condition that causes loss of skin color in patches. It occurs when melanocytes (pigment-producing cells) are destroyed. It's not harmful but can affect appearance and quality of life.",
        common_symptoms=["Loss of skin color in patches", "Premature whitening of hair", "Loss of color in tissues inside mouth/nose", "Symmetrical pattern (in many cases)"],
        possible_causes=["Autoimmune condition", "Genetic factors", "Triggering event (stress, sunburn, chemical exposure)", "Neurochemical factors (possible)"],
        precautions=["Sun protection (affected areas burn easily)", "Camouflage makeup if desired", "Emotional support", "Avoid skin trauma"],
        recommended_next_steps="Consult a dermatologist for diagnosis and treatment options. Treatments include topical corticosteroids, calcineurin inhibitors, light therapy, depigmentation (for extensive cases), or surgical options. Treatment success varies.",
        default_severity=SeverityLevel.MILD
    )
}


def get_disease_info(disease_name: str) -> Optional[DiseaseInfo]:
    """Get disease information by disease name."""
    return DISEASE_INFO_MAP.get(disease_name.lower())


def get_severity_from_confidence(confidence: float, default_severity: SeverityLevel) -> SeverityLevel:
    """Determine severity level based on confidence score and disease type."""
    if confidence < 0.5:
        # Low confidence might indicate mild case or uncertainty
        return SeverityLevel.MILD
    elif default_severity == SeverityLevel.SEVERE:
        # Severe diseases remain severe if confidence is high
        return SeverityLevel.SEVERE if confidence > 0.7 else SeverityLevel.MODERATE
    elif default_severity == SeverityLevel.MODERATE:
        # Moderate can stay moderate or become mild/severe based on confidence
        if confidence > 0.8:
            return SeverityLevel.MODERATE
        elif confidence < 0.6:
            return SeverityLevel.MILD
        else:
            return SeverityLevel.MODERATE
    else:
        # Mild diseases
        if confidence > 0.9:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MILD

