CREATE TYPE order_status AS ENUM ('PENDING', 'SENT', 'CANCELED');

CREATE TABLE client (
  id SERIAL PRIMARY KEY,
  username VARCHAR NOT NULL UNIQUE,
  password VARCHAR NOT NULL,
  firstname VARCHAR NOT NULL,
  lastname VARCHAR NOT NULL,
  address VARCHAR NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE product (
  id SERIAL PRIMARY KEY,
  sku INTEGER NOT NULL UNIQUE,
  name VARCHAR NOT NULL,
  description VARCHAR,
  price FLOAT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock (
  id SERIAL PRIMARY KEY,
  product_id INTEGER NOT NULL UNIQUE,
  quantity INTEGER NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_stock_product FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE TABLE "order" (
  id VARCHAR PRIMARY KEY,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  client_id INTEGER NOT NULL,
  status order_status NOT NULL DEFAULT 'PENDING',
  CONSTRAINT fk_order_client FOREIGN KEY (client_id) REFERENCES client(id)
);

CREATE TABLE order_item (
  id SERIAL PRIMARY KEY,
  order_id VARCHAR NOT NULL,
  product_id INTEGER NOT NULL,
  quantity INTEGER NOT NULL,
  unit_price FLOAT NOT NULL,
  CONSTRAINT fk_order_item_order FOREIGN KEY (order_id) REFERENCES "order"(id),
  CONSTRAINT fk_order_item_product FOREIGN KEY (product_id) REFERENCES product(id)
);

CREATE INDEX idx_order_client_id ON "order"(client_id);
CREATE INDEX idx_order_status ON "order"(status);
CREATE INDEX idx_order_item_order_id ON order_item(order_id);
