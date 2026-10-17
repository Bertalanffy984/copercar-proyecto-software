from fastapi import FastAPI
from app.routers import jwt_auth_router
from app.routers.vehiculos_routers import vehiculo_routers 
app = FastAPI(title="SANTIAGO AMA A KAREN Y NO LE DICE NADA", version="1.0")

#router para la autenticacion
app.include_router(jwt_auth_router.router)

#router para el crud de los vehiculos
app.include_router(vehiculo_routers.router)


