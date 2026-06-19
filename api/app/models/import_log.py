from sqlalchemy import (
    Column,
    BigInteger,
    Integer,
    String,
    DateTime,
    func
)

from app.core.database import Base


class ImportLog(Base):

    __tablename__ = "import_log"
    __table_args__ = {"schema": "dbr"}

    id = Column(BigInteger, primary_key=True)

    filename = Column(String(255))

    file_hash = Column(String(64), unique=True)

    total_rows = Column(Integer)

    inserted_rows = Column(Integer)

    skipped_rows = Column(Integer)

    imported_at = Column(
        DateTime,
        server_default=func.now()
    )
