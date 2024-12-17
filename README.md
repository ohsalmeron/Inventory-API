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

´
python -m venv venv
source venv/bin/activate
´

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


