from tempfile import NamedTemporaryFile
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.excel_import import import_excel
from app.services.file_hash import generate_hash

router = APIRouter(
    prefix="/api/v1/import",
    tags=["Import"],
)


@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    content = await file.read()
    file_hash = generate_hash(content)

    with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
        tmp.write(content)
        tmp.flush()
        result = import_excel(
            file_path=tmp.name,
            file_hash=file_hash,
            filename=file.filename,
            db=db,
        )

    return result
