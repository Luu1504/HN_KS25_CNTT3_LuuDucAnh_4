from pydantic import BaseModel, Field

class DishCreate(BaseModel):
    dish_code: str = Field(..., min_length=4, max_length=10)
    price: float = Field(..., gt=0)
    dish_category_id: int

class DishCategorySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class DishResponse(BaseModel):
    id: int
    dish_code: str
    price: float
    dish_category: DishCategorySchema

    class Config:
        from_attributes = True