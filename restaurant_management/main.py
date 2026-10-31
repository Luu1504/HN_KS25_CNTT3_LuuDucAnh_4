from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


def create_response(status_code: int, error: str, message: str, data):
    return {
        "statusCode": status_code,
        "error": error,
        "message": message,
        "data": data
    }


@app.post("/dishes")
def create_dish(dish_in: schemas.DishCreate, db: Session = Depends(get_db)):
    category = db.query(models.DishCategory).filter(
        models.DishCategory.id == dish_in.dish_category_id).first()
    if category == None:
        return create_response(400, "Bad Request", "Danh mục món ăn không tồn tại.", None)

    existing_dish = db.query(models.Dish).filter(
        models.Dish.dish_code == dish_in.dish_code).first()
    if existing_dish != None:
        return create_response(400, "Bad Request", "Mã món ăn đã tồn tại.", None)

    new_dish = models.Dish(
        dish_code=dish_in.dish_code,
        price=dish_in.price,
        dish_category_id=dish_in.dish_category_id
    )
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)

    response_data = schemas.DishResponse.model_validate(new_dish).model_dump()

    return create_response(201, None, "Thêm món ăn thành công", response_data)


@app.get("/dishes")
def get_dishes(db: Session = Depends(get_db)):
    dishes = db.query(models.Dish).all()

    data_list = []
    for dish in dishes:
        data_list.append(
            schemas.DishResponse.model_validate(dish).model_dump())

    return create_response(200, None, "Lấy danh sách món ăn thành công", data_list)


@app.delete("/dish-categories/{id}")
def delete_dish_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.DishCategory).filter(
        models.DishCategory.id == id).first()

    if category == None:
        return create_response(404, "Not Found", "Không tìm thấy danh mục món ăn.", None)

    dishes_in_category = db.query(models.Dish).filter(
        models.Dish.dish_category_id == id).all()
    if len(dishes_in_category) > 0:
        return create_response(400, "Bad Request", "Không thể xóa danh mục đang có món ăn.", None)

    db.delete(category)
    db.commit()

    return create_response(200, None, "Xóa danh mục món ăn thành công", None)
