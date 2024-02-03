class User(BaseModel):
    """
    Модель пользователя c ID
    """

    id: int
    first_name: str = Field(..., title="Имя", min_length=5, max_length=50)
    last_name: str = Field(..., title="Фамилия", min_length=5, max_length=50)
    email: str = Field(..., title="Электронная почта", min_length=5, max_length=50)
    password: str = Field(..., title="Пароль", min_length=5, max_length=50)