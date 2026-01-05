## SkinMorph – Skin Disease Detection, Prediction & Recommendations

SkinMorph is a full‑stack prototype for **skin disease detection**, **risk progression prediction**, and **personalized recommendations** with a **mobile‑first React frontend** and a **FastAPI + PyTorch backend**.

This is **research / educational software**, **not a medical device** and **not for clinical decision‑making**.

### Main capabilities

- **Detector**: Multi‑class CNN classifier for common dermatoses + suspicious neoplasms (transfer learning on MobileNetV3).
- **SkinMorph predictor**: Temporal model that predicts risk trajectories and change heatmaps at **30 days / 6 months / 1 year**.
- **Recommendation engine**: Rule‑based evidence‑inspired skincare and referral suggestions.
- **Timeline & tracking**: Longitudinal lesion tracking and visualization.
- **Explainability**: Grad‑CAM saliency maps and tone‑aware metrics.
- **Clinician handoff**: PDF report export stub for sharing with clinicians.

### Quickstart (local, without Docker)

```bash
cd skinmorph/backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\\Scripts\\activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Then in a second terminal:

```bash
cd skinmorph/frontend
npm install
npm start
```

Backend runs on `http://localhost:8000`, frontend on `http://localhost:3000` by default.

### Quickstart (Docker)

```bash
cd skinmorph
docker-compose up --build
```

Then open the printed frontend URL in your browser.

### Repository layout

- `backend/` – FastAPI app, ML services, training & evaluation scripts.
- `frontend/` – React (TypeScript) app with Tailwind CSS.
- `models/` – Model definitions, demo weights placeholders.
- `data/` – Dataset downloaders, preprocessing hooks, demo data.
- `notebooks/` – EDA and sample training notebooks.
- `docs/` – Model card, ethics & privacy, regulatory checklist.
- `deploy/` – Deployment artifacts and Docker configuration.
- `tests/` – Pytest suite for backend API and ML pipeline.

For more details see `docs/README_BACKEND.md`, `docs/README_FRONTEND.md`, and `docs/MODEL_CARD.md`.






