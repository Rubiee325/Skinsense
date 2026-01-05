import io
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


router = APIRouter(prefix="/report", tags=["reports"])


@router.get("")
async def generate_report_stub(user_id: str | None = None) -> StreamingResponse:
    """
    Simple PDF export stub for clinician handoff.
    In a real deployment, this would include images, Grad-CAM overlays, and metrics.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(72, 750, "SkinMorph Prototype Report")

    c.setFont("Helvetica", 11)
    c.drawString(72, 720, f"Generated: {datetime.utcnow().isoformat()} UTC")
    c.drawString(72, 700, f"User ID: {user_id or 'demo-user'}")
    c.drawString(
        72,
        670,
        "This is a non-clinical research prototype. Outputs are not medical advice.",
    )
    c.drawString(72, 640, "TODO: Embed lesion history, Grad-CAM heatmaps, and metrics.")

    c.showPage()
    c.save()
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="skinmorph_report.pdf"'},
    )






