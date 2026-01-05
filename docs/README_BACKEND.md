## Backend (FastAPI + PyTorch)

### Overview

- `app/main.py` – FastAPI application factory and router wiring.
- `app/routers/` – API endpoints:
  - `/predict` – Single-image detector + Grad-CAM + recommendations.
  - `/predict_sequence` – Temporal SkinMorph risk predictor.
  - `/upload` – Stub for lesion/region registration.
  - `/timeline` – Stub for longitudinal tracking.
  - `/report` – PDF export stub for clinician handoff.
- `app/ml/` – ML components:
  - `detector.py` – MobileNetV3-based multi-class classifier.
  - `predictor.py` – Temporal LSTM head over backbone features.
  - `preprocessing.py` – Image transforms and normalization.
  - `explainability.py` – Grad-CAM generator.
  - `recommendations.py` – Rule-based recommendation engine.

### Local development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

API will be available at `http://localhost:8000`.

### Key scripts

- `train_detector.py` – MobileNetV3 detector training using PyTorch Lightning on an `ImageFolder` dataset.
- `train_predictor.py` – Temporal predictor demo training on synthetic sequence data.
- `data_preprocess.py` – Dataset directory setup, ISIC metadata download stub, and Fitzpatrick stratification hook.
- `evaluate.py` – Per-class evaluation on a validation set and placeholder for tone-stratified metrics.
- `sanity_check.py` – Sends demo images to `/predict` to validate end-to-end wiring.

### Demo data

- Expected directory layout for quick tests:

```text
data/
  demo_detector/
    train/
      classA/
      classB/
    val/
      classA/
      classB/
  demo_predictor/
    seq1/
      t0.png
      t1.png
```

Populate with a few small PNG/JPEG images to run a one-epoch demo training.






