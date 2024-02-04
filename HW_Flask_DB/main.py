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

app = FastAPI()


# Функции подключкния и отключения от БД


@app.on_event("startup")
async def startup():
    """
    Создание соединения с базой
    данных при запуске приложения
    """
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """
    Закрытие соединения с базой данных
    при остановке прилодежения
    """
    await database.disconnect()


# Заполнение таблиц тестовыми данными



@app.get("/fake_users/{count}")
async def make_fake_users(count: int):
    """
    Заполение таблицы пользователи
    """
    for i in range(count):
        query = Users.insert().values(
            first_name=f"user{i}",
            last_name=f"surname{i}",
            email=f"mail{i}@mail.ru",
            password=f"Fake_pass{i}@#$",
        )
        await database.execute(query)
    return {"message": f"{count} фейковых пользователей создано"}


@app.get("/fake_products/{count}")
async def make_fake_products(count: int):
    """
    Заполнение таблицы товаров
    """
    for i in range(count):
        query = Products.insert().values(
            title=f"product title       {i}",
            descriptions=f"descriptions text    {i}",
            price=i + 10,
        )
        await database.execute(query)
    return {"message": f"{count} фейковых товаров создано"}


@app.get("/fake_orders/{count}")
async def make_fake_orders(count: int):
    """
    Заполнение таблицы заказы
    """
    for i in range(count):
        query = Orders.insert().values(
            user_id=random.randint(0, count),
            product_id=random.randint(0, count),
            create_at=datetime.now(),
            status=f"example_satus    {i}",
        )
        await database.execute(query)
    return {"message": f"{count} фейковых заказов создано"}


# Вывод всех значений из таблиц (select all)




@app.get("/all_users/", response_model=List[User])
async def get_all_users():
    """
    Получение всex пользователей
    """
    query = Users.select()

    return await database.fetch_all(query)


@app.get("/all_product/", response_model=List[Product])
async def get_all_products():
    """
    Получение всех товаров
    """
    query = Products.select()

    return await database.fetch_all(query)


@app.get("/all_orders/", response_model=List[OrderIn])
async def get_all_orders():
    """
    Получение всех заказов
    """
    query = Orders.select()

    return await database.fetch_all(query)


# Получение одного экземпляра из модели



@app.get("/user/{user_id}", response_model=User)
async def fetch_one_user(user_id: int):
    """
    Получение одного пользователя по id
    """
    query = Users.select().where(Users.c.id == user_id)
    one_user = await database.fetch_one(query)
    if one_user:
        return one_user
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.get("/product/{product_id}", response_model=Product)
async def fetch_one_product(product_id: int):
    """
    Получение одного товара  по id
    """
    query = Products.select().where(Products.c.id == product_id)
    one_product = await database.fetch_one(query)
    if one_product:
        return one_product
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.get("/order/{order_id}", response_model=Order)
async def fetch_one_order(order_id: int):
    """
    Получение одного заказа  по id
    """
    query = Orders.select().where(Orders.c.id == order_id)
    one_order = await database.fetch_one(query)
    if one_order:
        return one_order
    raise HTTPException(status_code=404, detail="Заказ не найден")


# Cоздание одного экземпляра модели



@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    """
    Создание пользователя
    """
    query = Users.insert().values(**user.model_dump())
    record_id = await database.execute(query)
    return {**user.model_dump(), "id": record_id}


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    """
    Создание товара
    """
    query = Products.insert().values(**product.model_dump())
    record_id = await database.execute(query)
    return {**product.model_dump(), "id": record_id}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    """
    Создание заказа
    """
    query = Orders.insert().values(**order.model_dump())
    record_id = await database.execute(query)
    return {**order.model_dump(), "id": record_id}


# Изменение (update) экземпляра модели



@app.put("/user/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    """
    Изменение пользователя
    """
    query = Users.update().where(Users.c.id == user_id).values(**new_user.model_dump())
    update_user = await database.execute(query)
    if update_user:
        return {**new_user.model_dump(), "id": user_id}
    raise HTTPException(status_code=404, detail="Пользователь не найден")


@app.put("/product/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    """
    Изменение товара
    """
    query = (
        Products.update()
        .where(Products.c.id == product_id)
        .values(**new_product.model_dump())
    )
    update_product = await database.execute(query)
    if update_product:
        return {**new_product.model_dump(), "id": product_id}
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.put("/order/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    """
    Изменение заказа
    """
    query = (
        Orders.update().where(Orders.c.id == order_id).values(**new_order.model_dump())
    )
    update_order = await database.execute(query)
    if update_order:
        return {**new_order.model_dump(), "id": order_id}
    raise HTTPException(status_code=404, detail="Заказ не найден")


# Удаление объекта модели (delete)



@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """
    Удаление пользователя по ID
    """
    query = Users.delete().where(Users.c.id == user_id)
    delted_user = await database.execute(query)
    if delted_user:
        return {"message": "Пользовател удален"}
    raise HTTPException(status_code=404, detail="Пользовтаель не найден")


@app.delete("/product/{product_id}")
async def delete_product(product_id: int):
    """
    Удаление  товара по ID
    """
    query = Products.delete().where(Products.c.id == product_id)
    delted_product = await database.execute(query)
    if delted_product:
        return {"message": "Товар  удален"}
    raise HTTPException(status_code=404, detail="Товар не найден")


@app.delete("/order/{order_id}")
async def delete_order(order_id: int):
    """
    Удаление  заказа  по ID
    """
    query = Orders.delete().where(Orders.c.id == order_id)
    delted_order = await database.execute(query)
    if delted_order:
        return {"message": "Заказ  удален"}
    raise HTTPException(status_code=404, detail="Заказ не найден")