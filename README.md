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

### 1. **Pruebas Automatizadas**

- Las pruebas se ejecutan automáticamente al levantar los contenedores. Los resultados se muestran en la consola.

1. **Ver los resultados de las pruebas**:

   - Observa los resultados de las pruebas unitarias e integración en la consola. Ejemplo:
     ```plaintext
     ============================= test session starts ==============================
     platform linux -- Python 3.10.16, pytest-8.3.4, pluggy-1.5.0
     rootdir: /app
     plugins: anyio-4.7.0, cov-6.0.0
     collected 27 items

     tests/test_system.py ...........................                         [100%]

     ============================== 27 passed in 0.55s ==============================
     ```

2. **Explorar el código de las pruebas**:
   - Puedes revisar el código fuente de las pruebas en el directorio `tests/`:
     ```bash
     tree tests/
     ```

3. **Detalles de cobertura**:
   - Los reportes de cobertura se generan automáticamente y están disponibles en el directorio `coverage/`:
     ```bash
     ls coverage/
     ```

- **Notas**:
  - Las pruebas abarcan casos unitarios e integración para los endpoints principales.
  - Cualquier fallo en las pruebas será reportado directamente en la consola durante el despliegue.


### 2. **Documentación de la API**

- La API cuenta con documentación generada automáticamente en formato OpenAPI (Swagger).  
- Puedes acceder a la documentación desde tu navegador en la siguiente URL: [http://localhost:8000/docs](http://localhost:8000/docs)
- Si necesitas el esquema JSON de la API, está disponible en: [http://localhost:8000/openapi.json](http://localhost:8000/openapi.json)
- Se incluye una **Colección de POSTMAN** en la raíz del directorio `Inventory Management API.postman_collection.json`

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

- El contenedor inventory_db contiene toda la información de productos, inventarios y movimientos.

## Decisiones Tomadas Durante el Desarrollo

### Tecnologías utilizadas

1. **Lenguaje y Framework**:
   - **Lenguaje**: Python 3.10.
   - **Framework**: FastAPI por su eficiencia, soporte para OpenAPI/Swagger y facilidad de desarrollo para APIs RESTful.

       Python fue elegido basado en la entrevista previa en donde se solicitaba, sin embargo también se puede realizar en .NET, NodeJS/Express o Java/SpringBoot de acuerdo a los requerimientos técnicos de la empresa.

       Para edge tecnologies se recomienda usar Rust o Motoko para combinar lógica y bases de datos con seguridad criptográfica.

2. **Base de Datos**:
   - Se utilizó **PostgreSQL** por su capacidad de manejar índices complejos y optimizar consultas.

3. **Infraestructura Dockerizada**:
   - Uso de **Docker Compose** para orquestar los servicios: base de datos, API, respaldos y pruebas de carga.
   - Contenedores configurados para ser portables y de fácil despliegue en entornos locales o en la nube.

4. **Gestión de Respaldos**:
   - Configuración de un contenedor dedicado para ejecutar respaldos automáticos usando `pg_dump` y tareas programadas con `cron`.
   - Opción de realizar respaldos manuales en caso de requerirse.
   - Se utiliza un contenedor por separado para cubrir casos single points of failure.

5. **Pruebas**:
   - Cobertura amplia para pruebas unitarias automatizadas utilizando `pytest`, usando Seeds y también datos guardados y parseados dentro de las funciones.
   - Pruebas de carga manuales implementadas con **Locust** para asegurar la escalabilidad de la API bajo condiciones de alta concurrencia.

6. **Documentación**:
   - Generación automática de documentación en formato `OpenAPI/Swagger` para facilitar la integración de clientes con la API.

7. **Variables de Entorno**:
   - Gestión centralizada de variables de entorno y librerías a través de `.env` y `requirements.txt` para facilitar la configuración en diferentes entornos.

8. **Logs Estructurados**:
   - Configuración de logs en formato JSON con `python-json-logger` para integrarse con herramientas de monitoreo y depuración. 

### Diagrama de Arquitectura

```mermaid
graph LR
    User((Usuario)) -->|HTTP Requests| API[API RESTful]
    API -->|CRUD| DB[(Base de Datos PostgreSQL)]
    API -->|Respaldo Automático| Backup[Contenedor de Respaldos]
    User -->|Pruebas de Carga| Locust[Pruebas de Carga]
    API -->|Swagger UI| Docs[Documentación de la API]
    Tests[Pruebas Automatizadas] -->|Cobertura y Validación| API
```

**Descripción**:
- Los usuarios interactúan con la API RESTful para realizar operaciones CRUD.
- La API está respaldada por una base de datos PostgreSQL y un sistema de respaldos automáticos.
- Las pruebas de carga se ejecutan con Locust, simulando múltiples usuarios concurrentes.
- La documentación está accesible a través de una interfaz Swagger generada automáticamente.
- Pruebas unitarias y de integración validan la funcionalidad de la API.

