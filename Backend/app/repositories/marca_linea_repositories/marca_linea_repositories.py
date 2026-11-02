from sqlalchemy.orm import Session, contains_eager
from app.models.models_db.Marca import Marca
from app.models.models_db.Linea import Linea

class MarcaLineaRepository:
    
    @staticmethod
    def obtener_marca_nombre(db:Session, nombre:str) -> Marca|None:
        return db.query(Marca).filter(Marca.nombre==nombre).first()

    @staticmethod
    def obtener_marca_id(db:Session, id_marca:int) -> Marca|None:
        return db.query(Marca).filter(Marca.id_marca==id_marca).first()
    
    @staticmethod
    def obtener_linea_por_nombre_y_marca(db: Session, nombre_linea: str, id_marca: int) -> Linea | None:
      return db.query(Linea).filter(Linea.nombre == nombre_linea, Linea.id_marca == id_marca).first()

    @staticmethod
    def obtener_linea_id(db: Session, id_linea: int) -> Linea | None:
      return db.query(Linea).filter(Linea.id_linea == id_linea).first()

    @staticmethod
    def listar_marcas_activas(db: Session,skip: int = 0, limit: int = 25) -> list[Marca]:
        subquery_marcas = (
        db.query(Marca.id_marca)
        .filter(Marca.activo == True)
        .order_by(Marca.id_marca)
        .offset(skip)
        .limit(limit)
        .subquery()
        )
        return (
        db.query(Marca)
        .join(subquery_marcas, Marca.id_marca == subquery_marcas.c.id_marca)
        .outerjoin(Linea, (Marca.id_marca == Linea.id_marca) & (Linea.activo == True))
        .options(contains_eager(Marca.lineas))
        .order_by(Marca.id_marca, Linea.id_linea)
        .all()
          )
  
    @staticmethod
    def crear_marca(db:Session, nombre:str)->Marca:
        nueva_marca= Marca(nombre=nombre)
        db.add(nueva_marca)
        db.commit()
        db.refresh(nueva_marca)
        return nueva_marca
    
    @staticmethod
    def crear_linea(db:Session, nombre_linea:str, id_marca:int)->Linea:
        nueva_linea = Linea(nombre=nombre_linea, id_marca=id_marca)
        db.add(nueva_linea)
        db.commit()
        db.refresh(nueva_linea)
        return nueva_linea
    
    @staticmethod
    def cambiar_estado_marca(db: Session, marca: Marca) -> Marca:
     marca.activo = not marca.activo
     db.commit()
     db.refresh(marca)
     return marca

    @staticmethod
    def cambiar_estado_linea(db: Session, linea: Linea) -> Linea:
     linea.activo = not linea.activo
     db.commit()
     db.refresh(linea)
     return linea

    @staticmethod
    def eliminar_marca_logica_cascada(db: Session, marca: Marca) -> None:
     marca.activo = False
     for linea in marca.lineas:
        linea.activo = False
     db.commit()