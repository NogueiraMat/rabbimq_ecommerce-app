# 🛒 E-commerce Project - FastAPI + RabbitMQ + PostgreSQL

## 📌 Project Description

This is an e-commerce application built with **FastAPI** for the API layer, **RabbitMQ** for asynchronous processing of orders and inventory updates, and **PostgreSQL** as the relational database.

The system is structured around the following key components:

- **Users**: Handles user registration and authentication.
- **Orders**: Manages customer orders.
- **Order Items**: Contains details about the items included in each order.
- **Inventory**: Keeps track of available stock for each product.
- **RabbitMQ Messaging**: Processes orders asynchronously to improve scalability and performance.

---

## ⚙️ Setup Instructions


# 1. Start PostgreSQL and RabbitMQ containers
```bash
docker compose up --build
```


# 2. Navigate to the `database` folder
```bash
cd database
```

# 3. Copy the migration SQL file into the PostgreSQL container
```bash
docker cp migration.sql ecommerce-postgres:/migration.sql
```

# 4. Access the PostgreSQL container and run the migration to create tables
```bash
docker exec -it ecommerce-postgres /bin/bash
```

```bash
psql -U admin -d ecommerce -f migration.sql
```

# 5. Return to the project root and create a virtual environment
```bash
cd ..
python3 -m venv venv
```

# 6. Activate the virtual environment
```bash
source venv/bin/activate
```

# 7. Install project dependencies
```bash
pip install -r requirements.txt
```

# 8. Run the FastAPI application
```bash
uvicorn api.main:app --reload
```
