from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from pathlib import Path
from uuid import uuid4

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/embed")
async def upload_file(
    user_id: str = Query(...),
    file: UploadFile = File(...),
):
    try:
        # Preserve the original file extension
        extension = Path(file.filename).suffix

        # Generate a unique filename
        unique_filename = f"{uuid4()}{extension}"

        # Optionally organize files by user
        user_dir = UPLOAD_DIR / user_id
        user_dir.mkdir(parents=True, exist_ok=True)

        destination = user_dir / unique_filename

        with destination.open("wb") as buffer:
            while chunk := await file.read(1024 * 1024):
                buffer.write(chunk)

        return {
            "user_id": user_id,
            "filename": unique_filename,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "path": str(destination),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload file: {e}",
        )

    finally:
        await file.close()