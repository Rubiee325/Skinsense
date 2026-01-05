## SkinMorph Model Card (Prototype)

### Overview

SkinMorph is a research prototype for **skin lesion image analysis**, combining:

- **Detector**: Multi-class CNN that outputs probabilities over common dermatoses and a "melanoma-suspect" category.
- **Temporal predictor**: Lightweight temporal head that estimates risk trajectories (pigmentation, acne, wrinkle risk) at 30 days, 6 months, and 1 year.
- **Recommendation engine**: Rule-based layer that translates outputs into skincare and referral suggestions.

This system is **not a medical device** and **must not** be used to make or replace clinical diagnoses.

### Intended use

- **Intended users**: Researchers, ML engineers, and clinicians experimenting with explainable dermatology AI in an offline / lab setting.
- **Intended use cases**:
  - Exploring feasibility of lesion tracking and risk simulation.
  - Prototyping explainability (Grad-CAM) and timeline visualizations.
  - Teaching and demonstration in academic settings.
- **Out of scope**:
  - Triage decisions, treatment initiation, or therapy changes.
  - Self-diagnosis by patients.
  - Any autonomous or semi-autonomous clinical decision support.

### Data and limitations

- This repo ships **no clinical dataset**. Scripts reference public dermoscopy datasets such as ISIC/HAM10000 only via download helpers and placeholders.
- Real-world performance critically depends on:
  - Diversity of skin tones (Fitzpatrick I–VI).
  - Representation of different anatomical sites and camera devices.
  - Accurate labels, ideally histopathologically confirmed for neoplasms.
- **Likely limitations**:
  - **Skin-tone bias**: Public datasets are often skewed towards lighter skin tones. Without proactive curation, performance may be substantially worse on darker tones.
  - **Selection bias**: Images from specialist clinics differ from primary care or consumer-grade photos.
  - **Label noise**: Non-biopsy-confirmed labels can mislead training.

### Skin-tone–aware metrics

- The `evaluate.py` script is designed to be extended with **Fitzpatrick skin-type annotations** so that metrics can be reported per tone group.
- Recommended practice:
  - Stratify performance (e.g., sensitivity/specificity, calibration) by Fitzpatrick I–II, III–IV, V–VI.
  - Evaluate false-negative rates for melanoma-suspect lesions separately by skin tone.

### Model details

- **Backbone**: MobileNetV3-small (ImageNet-pretrained, PyTorch) for both detector and temporal feature extraction. Optional heavier backbones (e.g., ResNet/EfficientNet) can be plugged in for training.
- **Detector head**: Fully connected layer mapping backbone features to dermatosis classes.
- **Temporal predictor**:
  - Frozen backbone as feature extractor.
  - Small LSTM/MLP head to predict risk scores at future timepoints.
  - Optional future extension: conditional U-Net for plausible future appearance synthesis.
- **Explainability**: Grad-CAM heatmaps overlaid on the input image to indicate salient regions. These maps are **qualitative** and not a guarantee of model reasoning correctness.

### Risks and failure modes

- **Under-detection of melanoma and atypical lesions**, especially in underrepresented skin tones.
- **Overconfidence** in benign predictions (false reassurance).
- **Artifact sensitivity**: Hair, rulers, tattoos, compression artifacts, or other lesions in frame may distort outputs.
- **Temporal extrapolation**: Risk trajectories and simulated futures are trained on limited or synthetic data and may not reflect real clinical evolution.

### Mitigations and recommendations

- Always display **strong disclaimers** in the UI: this is not a diagnostic tool.
- For any "melanoma-suspect" or high-risk output:
  - Nudge users toward **in-person dermatology evaluation**.
  - Avoid language that suggests a definitive diagnosis.
- For low-risk outputs:
  - Emphasize **uncertainty** and **need for monitoring**, especially for changing lesions.
- Use skin-tone-stratified evaluation and, where possible, **oversample** underrepresented tones during training.

### Privacy and data retention

- Default configuration is **local-only processing**; images stay on the user's machine unless explicitly configured otherwise.
- Recommended policies (for production-like deployments, to be defined by the operator):
  - Explicit **opt-in** for data used in research or model improvement.
  - Clear description of data retention duration and deletion options.
  - Encryption at rest and in transit for any stored or transmitted images/metadata.

### Regulatory considerations

- This prototype is not cleared or approved by any regulatory body (e.g., FDA, EMA, MHRA).
- To move toward regulated clinical use, a sponsor would need to:
  - Define a precise **intended use** and risk classification.
  - Conduct **prospective clinical validation** with appropriate sample size and diversity.
  - Implement full **quality management, post-market surveillance, and cybersecurity** controls.

### Versioning and updates

- Model weights and code are expected to change frequently in research settings.
- Any deployment should:
  - Pin a specific model version.
  - Maintain clear changelogs.
  - Re-validate performance after any substantial change to data or architecture.






