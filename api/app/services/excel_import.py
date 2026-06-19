import pandas as pd
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models.import_log import ImportLog


def clean_value(value):

    if pd.isna(value):
        return None

    value = str(value)

    value = value.replace("\xa0", "")

    value = value.strip()

    if value == "":
        return None

    return value


def parse_excel_date(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    # ====================================
    # EXCEL SERIAL DATE
    # ====================================

    try:

        numeric_value = float(value)

        if numeric_value > 1000:

            excel_epoch = datetime(
                1899,
                12,
                30
            )

            return (
                excel_epoch +
                timedelta(days=numeric_value)
            ).date()

    except Exception:

        pass

    # ====================================
    # STRING DATE FORMATS
    # ====================================

    formats = (

        "%d/%m/%y",
        "%d/%m/%Y",

        "%Y-%m-%d",

        "%Y-%m-%d %H:%M:%S",

        "%Y-%m-%d %H:%M",

        "%d-%m-%Y",

        "%d-%m-%y"
    )

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).date()

        except Exception:

            pass

    return None


def parse_start_breakdown(value):

    if pd.isna(value):
        return None

    value = str(value).strip()

    if value == "":
        return None

    if "(" in value:

        value = value.split("(")[0].strip()

    formats = (

        "%d/%m/%y",
        "%d/%m/%Y",

        "%Y-%m-%d",

        "%Y-%m-%d %H:%M:%S"
    )

    for fmt in formats:

        try:

            return datetime.strptime(
                value,
                fmt
            ).date()

        except Exception:

            pass

    return None


def import_excel(
    file_path: str,
    file_hash: str,
    filename: str,
    db: Session
):

    # ====================================
    # CHECK DUPLICATE FILE
    # ====================================

    existing = (
        db.query(ImportLog)
        .filter(
            ImportLog.file_hash == file_hash
        )
        .first()
    )

    if existing:

        return {
            "status": "duplicate_file",
            "filename": filename,
            "total_rows": existing.total_rows
        }

    # ====================================
    # READ EXCEL
    # ====================================

    df = pd.read_excel(
        file_path,
        engine="openpyxl",
        dtype=str
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # remove unnamed columns

    df = df.loc[
        :,
        ~df.columns.str.contains("^Unnamed")
    ]

    # remove empty columns

    df = df.loc[
        :,
        df.columns != ""
    ]

    df = df.loc[
        :,
        df.columns != "\xa0"
    ]

    total_rows = len(df)

    if total_rows == 0:

        return {
            "status": "empty_file",
            "filename": filename,
            "total_rows": 0
        }

    # ====================================
    # BUILD RECORDS
    # ====================================

    records = []

    for row in df.to_dict("records"):

        records.append({

            "report_date_raw":
                clean_value(
                    row.get("DATE")
                ),

            "report_date":
                parse_excel_date(
                    row.get("DATE")
                ),

            "breakdown_start_date":
                parse_start_breakdown(
                    row.get("Start Break Down")
                ),

            "cn":
                clean_value(
                    row.get("C/N")
                ),

            "section":
                clean_value(
                    row.get("SECTION")
                ),

            "trouble_description":
                clean_value(
                    row.get("Trouble Description")
                ),

            "breakdown_code":
                clean_value(
                    row.get("Code")
                ),

            "hm_start":
                clean_value(
                    row.get("HM Start")
                ),

            "location":
                clean_value(
                    row.get("LOC")
                ),

            "start_breakdown":
                clean_value(
                    row.get("Start Break Down")
                ),

            "start_time":
                clean_value(
                    row.get("Start Time")
                ),

            "finish_time":
                clean_value(
                    row.get("Finish Time")
                ),

            "total":
                clean_value(
                    row.get("Total")
                ),

            "wo_number":
                clean_value(
                    row.get("WO")
                ),

            "notification_number":
                clean_value(
                    row.get("NOTIFICATION")
                ),

            "action_taken":
                clean_value(
                    row.get("ACTION")
                ),

            "mechanic":
                clean_value(
                    row.get("MECHANIC")
                ),

            "gl":
                clean_value(
                    row.get("GL")
                )
        })

    # ====================================
    # INSERT DATABASE
    # ====================================

    insert_sql = text("""
    INSERT INTO dbr.breakdown_history
    (
        report_date_raw,
        report_date,
        breakdown_start_date,
        cn,
        section,
        trouble_description,
        breakdown_code,
        hm_start,
        location,
        start_breakdown,
        start_time,
        finish_time,
        total,
        wo_number,
        notification_number,
        action_taken,
        mechanic,
        gl
    )
    VALUES
    (
        :report_date_raw,
        :report_date,
        :breakdown_start_date,
        :cn,
        :section,
        :trouble_description,
        :breakdown_code,
        :hm_start,
        :location,
        :start_breakdown,
        :start_time,
        :finish_time,
        :total,
        :wo_number,
        :notification_number,
        :action_taken,
        :mechanic,
        :gl
    )
    """)

    try:

        db.execute(
            insert_sql,
            records
        )

        db.commit()

    except Exception:

        db.rollback()

        raise

    # ====================================
    # SAVE IMPORT LOG
    # ====================================

    import_log = ImportLog(

        filename=filename,

        file_hash=file_hash,

        total_rows=total_rows,

        inserted_rows=total_rows,

        skipped_rows=0
    )

    db.add(import_log)

    db.commit()

    # ====================================
    # RESPONSE
    # ====================================

    return {

        "status": "success",

        "filename": filename,

        "total_rows": total_rows,

        "inserted": total_rows,

        "skipped": 0
    }
