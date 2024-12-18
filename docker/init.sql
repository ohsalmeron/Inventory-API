-- Habilitar la extensión uuid-ossp para generación de UUIDs
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tabla products
CREATE TABLE IF NOT EXISTS products (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  category TEXT,
  price DECIMAL,
  sku TEXT UNIQUE
);

-- Crear tabla inventory
CREATE TABLE IF NOT EXISTS inventory (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  store_id TEXT NOT NULL,
  quantity INT NOT NULL DEFAULT 0,
  min_stock INT NOT NULL DEFAULT 0
);

-- Crear tabla movements
CREATE TABLE IF NOT EXISTS movements (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  source_store_id TEXT,
  target_store_id TEXT,
  quantity INT NOT NULL,
  timestamp TIMESTAMP DEFAULT NOW(),
  type TEXT CHECK (type IN ('IN', 'OUT', 'TRANSFER')) NOT NULL
);

-- Crear índices para optimizar las consultas
CREATE INDEX IF NOT EXISTS idx_inventory_product_id
ON inventory (product_id);

CREATE INDEX IF NOT EXISTS idx_inventory_store_id
ON inventory (store_id);

CREATE INDEX IF NOT EXISTS idx_movements_product_id
ON movements (product_id);

CREATE INDEX IF NOT EXISTS idx_movements_source_store_id
ON movements (source_store_id);

CREATE INDEX IF NOT EXISTS idx_movements_target_store_id
ON movements (target_store_id);
