# Sistema de Gestión de Inventario

## Descripción

Este proyecto tiene como objetivo desarrollar una API REST para la gestión del inventario de una cadena de tiendas minoristas. El sistema permitirá la creación, consulta, actualización y eliminación de productos, así como la gestión del inventario por tienda, incluyendo transferencias de stock y alertas por bajo inventario.

## Tecnologías a Utilizar

- **Lenguaje:** Python 3.9+  
- **Framework:** FastAPI  
- **Base de Datos:** PostgreSQL  
- **Contenedores:** Docker y Docker Compose  
- **Documentación API:** OpenAPI/Swagger (generada automáticamente por FastAPI)  
- **Testing:** Pytest (unitarias e integración), herramientas de carga (ej: Locust, Artillery)
- **Logs:** Formato JSON estructurado

## Preparación del Entorno con Docker

Para este proyecto **no necesitas instalar dependencias localmente**. Utilizaremos Docker y Docker Compose para ejecutar tanto la aplicación FastAPI como la base de datos PostgreSQL en contenedores.

### Requisitos Previos

1. **Docker**: Instálalo desde [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)  
2. **Docker Compose**: Suele instalarse junto con Docker. Confirma con:  
   ```bash
   docker-compose --version

## Configuración de la Base de Datos

### 1. Levantar PostgreSQL con Docker Compose

El proyecto incluye un archivo `docker-compose.yml` para configurar la base de datos PostgreSQL. Sigue estos pasos:

1. **Ejecuta Docker Compose:**
   ```bash
   docker-compose up -d


Verificar la Base de Datos y Tablas
Queremos asegurarnos de que el script init.sql que creamos anteriormente se ejecutó correctamente y las tablas existen.

Conéctate al contenedor PostgreSQL usando psql:

   ```bash
  docker exec -it inventory_db psql -U postgres -d inventory







## Arquitectura y Alcance

El proyecto se basa en una arquitectura por capas:

- **Capa de Presentación (API - FastAPI):** Aquí se exponen los endpoints REST.  
- **Capa de Negocio (Servicios):** Implementa la lógica de negocio, validaciones y reglas de la aplicación.  
- **Capa de Datos (Repositorios):** Abstracción de acceso a la base de datos, consultas, inserciones y actualizaciones.  
- **Base de Datos (PostgreSQL):** Almacenamiento persistente. Se definirán índices para consultas frecuentes y se utilizarán transacciones en operaciones críticas.

**Principales Endpoints:**

- **Gestión de Productos**  
  - `GET /api/products`: Lista productos con filtros (categoría, precio, stock) y paginación.  
  - `GET /api/products/{id}`: Obtener detalles de un producto.  
  - `POST /api/products`: Crear un nuevo producto (validando campos obligatorios).  
  - `PUT /api/products/{id}`: Actualizar un producto existente.  
  - `DELETE /api/products/{id}`: Eliminar un producto.

- **Gestión de Inventario**  
  - `GET /api/stores/{id}/inventory`: Listar inventario por tienda.  
  - `POST /api/inventory/transfer`: Transferir productos entre tiendas, validando stock disponible.  
  - `GET /api/inventory/alerts`: Listar productos con stock bajo (por debajo de `minStock`).

**Pruebas y Calidad:**
- Tests unitarios con al menos 80% de cobertura.
- Tests de integración para flujos críticos (ej. transferencia de productos).
- Tests de carga (500 req/seg) para asegurar rendimiento.

**Despliegue:**
- Se utilizarán Dockerfile y docker-compose.
- Variables de entorno para configuración.
- Documentación con OpenAPI/Swagger generada automáticamente.
- Logs estructurados en JSON.
- Instrucciones de despliegue en entornos en la nube (AWS/GCP/Azure/DigitalOcean).
- Scripts de inicialización de la BD y configuración de backups.








README con:
○ Instrucciones de instalación
○ Documentación de API
○ Decisiones técnicas
○ Diagrama de arquitectura

El siguiente proyecto fue elaborado en Archlinux

# Instalación y Entorno

## Versionamiento
Archlinux base-devel
Python 3.12.7
Docker 27.3.1
Docker Compose 2.32.0

En Archlinux
sudo pacman -S python
sudo apt install python

Usando un entorno virtual para mayor seguridad

´´´bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
´´´ 
pip install fastapi uvicorn[standard] sqlalchemy psycopg2-binary python-dotenv pydantic


fastapi: framework para la API.
uvicorn[standard]: servidor ASGI para correr FastAPI.
sqlalchemy: ORM para PostgreSQL.
psycopg2-binary: conector de Python a PostgreSQL.
python-dotenv: para cargar variables de entorno desde archivos .env.
pydantic: para validación y modelado de datos.


Estructura inicial

inventory-management/
  ├─ app/
  │   ├─ main.py
  │   ├─ config.py
  │   ├─ database.py
  │   ├─ models/
  │   │   ├─ __init__.py
  │   │   ├─ product.py
  │   │   ├─ inventory.py
  │   │   └─ movement.py
  │   ├─ schemas/
  │   │   ├─ __init__.py
  │   │   ├─ product.py
  │   │   ├─ inventory.py
  │   │   └─ movement.py
  │   ├─ repositories/
  │   │   ├─ __init__.py
  │   │   ├─ products_repository.py
  │   │   ├─ inventory_repository.py
  │   │   └─ movements_repository.py
  │   ├─ services/
  │   │   ├─ __init__.py
  │   │   ├─ products_service.py
  │   │   ├─ inventory_service.py
  │   │   └─ movements_service.py
  │   ├─ routers/
  │   │   ├─ __init__.py
  │   │   ├─ products.py
  │   │   ├─ inventory.py
  │   │   └─ movements.py
  │   └─ __init__.py
  ├─ docker/
  │   ├─ docker-compose.yml
  │   └─ init.sql
  ├─ tests/
  │   ├─ unit/
  │   └─ integration/
  ├─ .env
  ├─ requirements.txt
  ├─ README.md



## Inicialización de base de datos

Inicializar servicio de docker
systemctl start docker

´
cd docker
docker-compose up -d
docker exec -i inventory_db psql -U postgres -d inventory < init.sql
´

docker/init.sql





FastAPI generará automáticamente la documentación en:

http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (Redoc)