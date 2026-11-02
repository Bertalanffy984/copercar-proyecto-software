from fastapi import FastAPI
from app.routers import jwt_auth_router
from app.routers.vehiculos_routers import vehiculo_router 
from app.routers.usuarios_routers import usuarios_router
from app.routers.movimientos_routers import movimientos_router
from app.routers.reportes_routers import reportes_router
from app.routers.marca_linea_routers import marca_linea_router
app = FastAPI(title="COPERCAR", version="1.1")

#router para la autenticacion
app.include_router(jwt_auth_router.router)

#router para el crud de los vehiculos
app.include_router(vehiculo_router.router)

#router para la gestion de usuarios por parte del administrador
app.include_router(usuarios_router.router)

#router para la gestion de movimientos por parte del administrador
app.include_router(movimientos_router.router)

#router para devolver los reportes
app.include_router(reportes_router.router)

#router para la gestion de las marcas y las lineas
app.include_router(marca_linea_router.router)

