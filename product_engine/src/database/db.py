from sqlalchemy import URL

url_object = URL.create(
    "postgresql+asyncpg",
    username="postgres",
    password="postgres",
    host="fintech-postgresql",
    port=5432,
    database="product_engine"
)

db_settings = {
    "database_url": url_object,
    "echo": True,
}
