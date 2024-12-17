CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS products (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT,
  category TEXT,
  price DECIMAL,
  sku TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS inventory (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  store_id TEXT NOT NULL,
  quantity INT NOT NULL DEFAULT 0,
  min_stock INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS movements (
  id uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  product_id uuid REFERENCES products(id) ON DELETE CASCADE,
  source_store_id TEXT,
  target_store_id TEXT,
  quantity INT NOT NULL,
  timestamp TIMESTAMP DEFAULT NOW(),
  type TEXT CHECK (type IN ('IN', 'OUT', 'TRANSFER'))
);
