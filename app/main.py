from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.routers import products, inventory, movements
import logging.config
import traceback
import os
import json

# Configurar Logging
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_CONFIG_PATH = os.path.join(BASE_DIR, "logging_config.json")

if os.path.exists(LOG_CONFIG_PATH):
    with open(LOG_CONFIG_PATH, "r") as config_file:
        log_config = json.load(config_file)
    logging.config.dictConfig(log_config)
else:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

logger = logging.getLogger("inventory_api")

# Configuración de la Aplicación FastAPI
app = FastAPI(
    title="Inventory Management API",
    version="1.0",
    description="API para gestionar productos, inventario y movimientos en una cadena de tiendas minoristas."
)

# Middleware: Manejo global de errores
class LogErrorsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.debug_mode = os.getenv("DEBUG", "False").lower() == "true"

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error({
                "path": request.url.path,
                "method": request.method,
                "error": str(e),
                "traceback": error_trace
            })
            error_message = {
                "detail": "Internal Server Error"
            }
            if self.debug_mode:
                error_message.update({"error": str(e), "traceback": error_trace})
            return JSONResponse(status_code=500, content=error_message)

# Agregar Middleware
app.add_middleware(LogErrorsMiddleware)

# Incluir Routers
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(inventory.router, prefix="/api/inventory", tags=["Inventory"])
app.include_router(movements.router, prefix="/api/movements", tags=["Movements"])

# Endpoint Principal
@app.get("/", tags=["Root"], summary="Verificar el estado de la API")
def read_root():
    """Endpoint principal para comprobar que la API está en funcionamiento."""
    return {"message": "Bienvenido al Sistema de Gestión de Inventario!"}
