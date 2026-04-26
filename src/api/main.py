from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel

users = [
    {"id": 1, "name": "Иван", "email": "ivan@test.ru"},
    {"id": 2, "name": "Дима", "email": "dima@test.ru"},
    {"id": 3, "name": "Вова", "email": "vova@test.ru"}
]

products = [
    {"id": 1, "name": "Ноутбук", "price": 50000},
    {"id": 2, "name": "Мышь", "price": 1500}
    ]
app = FastAPI()
@app.get("/products")
def get_products(limit: int = 10,offset: int = 0):
    return {
        "limit": limit,
        "offset": offset,
        "products": products[offset:offset+limit]
    }

@app.get("/products/{id}")
def get_product(id: int):
    for product in products:
        if product["id"] == id:
            return product
    raise HTTPException(status_code=404, detail="Item not found")



class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate):
 return {
 "id": 5,
 "user_id": order.user_id,
 "product_id": order.product_id,
 "quantity": order.quantity,
 "message": "Заказ создан"
 }
@app.get("/users")
def get_users(limit: int = 10,offset: int = 0):
    return {
        "limit": limit,
        "offset": offset,
        "users": users[offset:offset+limit]
    }


@app.get("/users/{id}")
def get_user(id: int):
    for user in users:
        if user["id"] == id:
            return user
    raise HTTPException(status_code=404, detail="Item not found")


class UserCreate(BaseModel):
    name: str
    email: str
@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
 return {
 "id": 5,
 "name": user.name,
 "email": user.email,
 "message": "Пользователь создан"
 }
