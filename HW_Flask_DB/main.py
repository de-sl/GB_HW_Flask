DATABASE_URL = "sqlite:///shop.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

Users = sqlalchemy.Table(
    # Таблица пользователей
    "Users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("first_name", sqlalchemy.String(15), nullable=False),
    sqlalchemy.Column("last_name", sqlalchemy.String(15), nullable=False),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True, nullable=False),
    sqlalchemy.Column("password", sqlalchemy.String, nullable=False),
)

Products = sqlalchemy.Table(
    # Таблица товаров
    "Products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("title", sqlalchemy.String(100), nullable=False),
    sqlalchemy.Column("descriptions", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("price", sqlalchemy.Float, nullable=False),
)


Orders = sqlalchemy.Table(
    # Таблица заказов
    "Orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, nullable=False),
    sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("Users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("Products.id")),
    sqlalchemy.Column(
        "create_at",
        sqlalchemy.DateTime,
        nullable=False,
        default=datetime.now(),
    ),
    sqlalchemy.Column("status", sqlalchemy.String, nullable=False),
)


enginie = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(enginie)