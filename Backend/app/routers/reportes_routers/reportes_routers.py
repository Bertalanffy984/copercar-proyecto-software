from fastapi import APIRouter, Depends, Query, status
from datetime import date
from sqlalchemy.orm import Session
from app.database.conexion import get_db
from app.dependencies.rol_dependencies import obtener_administrador
from app.schemas.BaseDB.reporte import ReporteMensualResponse
from app.services.reportes_services.reportes_services import ReporteService

router = APIRouter(prefix="/reportes", tags=["Gestión de Reportes (Admin)"], dependencies=[Depends(obtener_administrador)])

@router.get("/finanzas", response_model=ReporteMensualResponse, status_code=status.HTTP_200_OK, summary=("Consultar ingresos,egresos y otras metricas"))
def consultar_reporte_mensual(anio: int = Query(..., ge=2000, le=date.today().year), mes: int = Query(..., ge=1, le=12),db: Session = Depends(get_db)):
  return ReporteService.generar_reporte_mensual(db=db, anio=anio, mes=mes)