from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

# ── Create FastAPI app ─────────────────────────────
app = FastAPI()
# Temporary in-memory storage (structure phase only)
PATIENT_REPORTS = []

# ── Enable CORS so React frontend can communicate ─
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allows all origins during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Test route (to check backend is running) ───────
@app.get("/")
def home():
    return {"message": "Backend running successfully"}

# ── Symptom Checker endpoint ───────────────────────
@app.post("/symptoms")
async def receive_symptoms(request: Request):
    data = await request.json()
    print("Received:", data)

    # For now we return a dummy response
    # Later this will be replaced by AI prediction
    return {
        "message": "Symptoms received successfully",
        "data": data
    }
from fastapi import UploadFile, File, Form

# @app.post("/upload")
# async def upload_report(
#     xray: UploadFile = File(...),
#     clinical_notes: str = Form(...),
#     vitals: str = Form(...)
# ):
#     print("File received:", xray.filename)
#     print("Clinical notes:", clinical_notes)
#     print("Vitals:", vitals)

#     # Structure phase → just return success
#     return {
#         "message": "Report uploaded successfully",
#         "file_name": xray.filename
#     }
@app.post("/upload")
async def upload_report(
    xray: UploadFile = File(...),
    clinical_notes: str = Form(...),
    vitals: str = Form(...)
):
    report = {
        "id": len(PATIENT_REPORTS) + 1,
        "name": "New Patient",
        "symptoms": clinical_notes,
        "fileName": xray.filename,
        "vitals": vitals,
        "aiResult": {
            "label": "Pending AI Analysis",
            "confidence": "--",
            "severity": "low"
        }
    }

    PATIENT_REPORTS.append(report)

    return {"message": "Report uploaded successfully"}
@app.get("/reports")
async def get_reports():
    return PATIENT_REPORTS
