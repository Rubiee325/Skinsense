## Frontend (React + TypeScript + Tailwind)

### Overview

- Tech stack:
  - React 18 + TypeScript.
  - React Router for navigation.
  - Tailwind CSS for styling (mobile-first).
  - Axios for HTTP calls to the FastAPI backend.

### Pages and flows

- `Onboarding` – Welcome, disclaimers, and getting started.
- `Capture` – Image upload with a simple AR-style guide box; sends image to `/predict`.
- `Result` – Shows detector output, Grad-CAM overlay, and recommendations.
- `Timeline` – Stubbed view for longitudinal tracking data from `/timeline`.
- `Simulator` – Calls `/predict_sequence` to visualize temporal risk outputs.
- `Recommendations` – Dedicated view of the recommendation list.
- `Referral` – Triggers `/report` and provides a link to open/download the PDF.

### Local development

```bash
cd frontend
npm install
npm start
```

- The app will run at `http://localhost:3000`.
- It expects the backend API at `http://localhost:8000` (configurable via `REACT_APP_API_BASE`).

### Styling

- Tailwind is configured via:
  - `tailwind.config.js`
  - `postcss.config.js`
  - `src/index.css`
- The default theme uses a dark, desaturated palette to keep focus on images and overlays.






