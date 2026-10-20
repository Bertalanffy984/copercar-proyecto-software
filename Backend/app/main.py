from fastapi import FastAPI
from app.routers import jwt_auth_router
from app.routers.vehiculos_routers import vehiculo_routers 
from app.routers.usuarios_routers import usuarios_routers
from app.routers.movimientos_routers import movimientos_routers
from app.routers.reportes_routers import reportes_routers
app = FastAPI(title="COPERCAR", version="1.0")

#router para la autenticacion
app.include_router(jwt_auth_router.router)

#router para el crud de los vehiculos
app.include_router(vehiculo_routers.router)

#router para la gestion de usuarios por parte del administrador
app.include_router(usuarios_routers.router)

#router para la gestion de movimientos por parte del administrador
app.include_router(movimientos_routers.router)

#router para devolver los reportes
app.include_router(reportes_routers.router)

