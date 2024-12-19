# Sistema de Gestión de Inventario

## Descripción

Este proyecto consiste en una API REST para gestionar el inventario de una cadena de tiendas minoristas. Permite gestionar productos, transferir inventarios entre sucursales y configurar alertas de stock bajo.


## Instrucciones de Instalación

### Requisitos Previos
1. **Instalar Docker y Docker Compose**:
  Instálalos desde [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)  
   - Asegúrate de tener Docker y Docker Compose instalados en tu máquina.
   - Verifica que Docker esté funcionando ejecutando:
     ```bash
     docker --version
     docker-compose --version
     ```

2. Clonar este repositorio:
   ```bash
   git clone https://github.com/ohsalmeron/Inventory-API.git
   cd Inventory-API

### Levantar los Contenedores
1. **Ejecutar el comando principal**  
   - Construye y levanta los contenedores con un solo comando:
     ```bash
     docker-compose up --build
     ```

2. **Alta de servicios**  
   - El proyecto incluye un archivo `init.sql` para inicializar la base de datos, `.env` con las variables de entorno necesarias, así como los requerimientos de Python en `requirements.txt`.  
   - Una vez ejecutado el comando anterior, todos los servicios estarán activos automáticamente:
     - Base de datos PostgreSQL
     - Restful API de inventario
     - Sistema de respaldos automáticos
     - Pruebas automatizadas
     - Herramienta de pruebas de carga (Locust)

## Verificación de Componentes

### 1. **Pruebas Unitarias**

- Las pruebas unitarias se ejecutan automáticamente al levantar los contenedores con `docker-compose up`.  
- Los resultados de las pruebas se muestran directamente en la consola.  
- Puedes revisar el código de las pruebas en la carpeta `/tests/` ejecutando:
  ```bash
  ls tests/
  ```

- Los reportes de cobertura se generan en el directorio coverage/. Para verificar su contenido, ejecuta:
  ```bash
  ls coverage/
  ```

### 2. **Documentación de la API**

- La API cuenta con documentación generada automáticamente en formato OpenAPI (Swagger).  
- Puedes acceder a la documentación desde tu navegador en la siguiente URL: [http://localhost:8000/docs](http://localhost:8000/docs)
- Si necesitas el esquema JSON de la API, está disponible en: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- También se incluye una **Colección de POSTMAN** en la raíz del directorio `Inventory Management API.postman_collection.json`

### 3. **Pruebas de Carga con Locust**

- Accede a la interfaz de usuario de Locust para configurar y ejecutar pruebas de carga en la siguiente URL:  
  [http://localhost:8089/](http://localhost:8089/)

- Se recomienda configurar las pruebas siguiendo las mejores prácticas:
  - **Number of Users** (peak concurrency): 500 o más usuarios simultaneos
  - **Ramp up** (users added per sec): De 10 hasta un máximo de 100 usuarios agregados por segundo.
  - **Host** (URL interna de docker) para las pruebas de carga: `http://inventory_api:8000`

### 4. **Backups Automatizados**

- El servicio de respaldos automáticos está configurado con un **cron** dentro del contenedor `inventory_db_backup`.  
- Para verificar la programación de los respaldos, ingresa al contenedor y ejecuta el siguiente comando:

  ```bash
  docker exec -it inventory_db_backup bash
  crontab -l
  ```

- Los respaldos se generan diariamente en el directorio /backups dentro del contenedor.

Cada archivo tiene un nombre con formato: `inventory_backup_YYYYMMDD_HHMMSS.sql.`

Si necesitas realizar un respaldo manual, usa este comando:

  ```bash
  docker exec -it inventory_db_backup bash
  PGPASSWORD=postgres pg_dump -U postgres -h inventory_db inventory > /backups/respaldo_manual.sql
  ```

- Los respaldos generados pueden revisarse en el directorio de backups:

  ```bash
  docker exec -it inventory_db_backup bash
  ls /backups
  ```

### 5. **Acceso y Verificación de la Base de Datos**

- Para ingresar al contenedor de la base de datos y ejecutar comandos SQL manualmente, sigue estos pasos:

1. Accede al contenedor de la base de datos:
  ```bash
  docker exec -it inventory_db bash
  psql -U postgres -d inventory
  ```

Una vez dentro del cliente de PostgreSQL, puedes ejecutar comandos SQL. Por ejemplo:

Mostrar todas las tablas:
  ```bash
  \dt
  ```









## Tecnologías utilizadas

- **Lenguaje:** Python
- **Framework:** FastAPI
- **Base de Datos:** PostgreSQL
- **Contenedores:** Docker y Docker Compose  
- **Documentación API:** OpenAPI/Swagger (generada automáticamente por FastAPI)  
- **Testing:** Pytest (unitarias e integración), Locust como herramientas de carga
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