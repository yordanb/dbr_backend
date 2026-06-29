from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
from app.core.database import get_mte_db

router = APIRouter(prefix="/equipment", tags=["Equipment"])

class EquipmentUpdate(BaseModel):
    data: Dict[str, Any]

@router.get("/{table_name}")
def list_table(table_name: str, db: Session = Depends(get_mte_db)):
    try:
        safe_table = "".join(c for c in table_name if c.isalnum() or c == "_")
        rows = db.execute(text(f"SELECT * FROM {safe_table} ORDER BY no LIMIT 500")).fetchall()
        return [dict(row._mapping) for row in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/{table_name}/{id}")
def update_item(table_name: str, id: int, payload: EquipmentUpdate, db: Session = Depends(get_mte_db)):
    try:
        safe_table = "".join(c for c in table_name if c.isalnum() or c == "_")
        set_clause = ", ".join([f"{k} = :{k}" for k in payload.data.keys()])
        query = text(f"UPDATE {safe_table} SET {set_clause} WHERE no = :id")
        params = payload.data.copy()
        params["id"] = id
        db.execute(query, params)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/{table_name}")
def add_item(table_name: str, payload: EquipmentUpdate, db: Session = Depends(get_mte_db)):
    try:
        safe_table = "".join(c for c in table_name if c.isalnum() or c == "_")
        keys = payload.data.keys()
        cols = ", ".join(keys)
        vals = ", ".join([f":{k}" for k in keys])
        query = text(f"INSERT INTO {safe_table} ({cols}) VALUES ({vals})")
        db.execute(query, payload.data)
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/search/{cn}")
def search_by_cn(cn: str, db: Session = Depends(get_mte_db)):
    try:
        clean = cn.strip().replace("'", "''")
        query = text("""
            SELECT
                'tb_lighting_eqp' as source_table, no, cn, coalesce(unit_type::text,'') as unit_type, coalesce(unit_model::text,'') as unit_model, coalesce(cn_serial_no::text,'') as cn_serial_no, coalesce(engine_serial_no::text,'') as engine_serial_no, coalesce(engine_merk::text,'') as engine_merk, coalesce(arrived_year::text,'') as arrived_year, coalesce(arrived_month::text,'') as arrived_month, aktif
            FROM tb_lighting_eqp WHERE cn = :cn
            UNION ALL
            SELECT
                'tb_spex_mobile' as source_table, no, cn, coalesce(unit_type::text,''), coalesce(unit_model::text,''), coalesce(cn_serial_no::text,''), coalesce(engine_serial_no::text,''), coalesce(engine_merk::text,''), coalesce(arrived_year::text,''), coalesce(arrived_month::text,''), aktif
            FROM tb_spex_mobile WHERE cn = :cn
            UNION ALL
            SELECT
                'tb_spex_pumping' as source_table, no, cn, coalesce(unit_type::text,''), coalesce(unit_product::text,''), coalesce(cn_serial_no::text,''), '', coalesce(engine_genset_merk::text,''), coalesce(arrived_year::text,''), coalesce(arrived_month::text,''), aktif
            FROM tb_spex_pumping WHERE cn = :cn
            UNION ALL
            SELECT
                'tb_bigwheel' as source_table, no, cn, coalesce(unit_type::text,''), coalesce(unit_product::text,''), coalesce(cn_serial_no::text,''), coalesce(engine_model::text,''), coalesce(engine_merk::text,''), coalesce(arrived_year::text,''), coalesce(arrived_month::text,''), aktif
            FROM tb_bigwheel WHERE cn = :cn
        """)
        rows = db.execute(query, {"cn": clean}).mappings().all()
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
