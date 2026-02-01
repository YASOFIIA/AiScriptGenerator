from __future__ import annotations

import threading
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from app.core.config import settings
from app.services.runs import RunStore, RunState
from app.utils.csv_parser import parse_csv
from app.services.runner import run_bulk_generation

router = APIRouter(
    prefix="/bulk",
    tags=["bulk"]
)
store = RunStore()

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File()):
    if not  file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Invalid file type")

    raw = await file.read()
    if len(raw) > settings.MAX_FILE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large")

    tmp_path = settings.uploads_path / f"upload{file.filename}"
    tmp_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path.write_bytes(raw)

    rows= parse_csv(tmp_path)

    if not rows:
        raise HTTPException(status_code=400, detail="CSV is empty or not readable")

    if len(rows) > settings.MAX_ROWS:
        raise HTTPException(status_code=400, detail=f"Too many rows. Max is {settings.MAX_ROWS}")

    run = store.create_run(total_scripts=len(rows))
    run.input_csv_path = str(tmp_path)

    return {"run_id": run.run_id, "total_scripts": run.total_scripts}

@router.post("/{run_id}/start")
def start_run(run_id: str):
    run = store.get(run_id)
    if run.state in (RunState.RUNNING, RunState.COMPLETED):
        return {"run_id": run_id, "state": run.state}

    if not run.input_csv_path:
        raise HTTPException(status_code=400, detail="No CSV uploaded for this run")

    csv_path = Path(run.input_csv_path)
    rows = parse_csv(csv_path)

    t = threading.Thread(target=run_bulk_generation, args=(store, run_id, rows), daemon=True)
    t.start()

    return{"run_id": run_id,"state": "RUNNING"}

@router.get("/{run_id}/status")
def run_status(run_id: str):
    run = store.get(run_id)
    return {
        "run_id": run.run_id,
        "state": run.state,
        "message": run.message,
        "current_script": run.current_script,
        "total_scripts": run.total_scripts,
        "current_prompt": run.current_prompt,
        "total_prompts": run.total_prompts,
        "progress_pct": run.progress_pct,
        "error": run.error,
        "output_docx_path": run.output_docx_path,
    }

@router.get("/{run_id}/download")
def download(run_id: str):
    run = store.get(run_id)

    if run.state != RunState.COMPLETED or not run.output_docx_path:
        raise HTTPException(status_code=400, detail="Run is not completed yet")

    path = Path(run.output_docx_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="Output file not found")

    return FileResponse(
        path=str(path),
        filename=path.name,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

@router.post("/{run_id}/cancel")
def cancel(run_id: str):
    store.request_cancel(run_id)
    return {"run_id": run_id, "state": "CANCEL_REQUESTED"}