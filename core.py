raw_dishes = [
    {"dish_code": "F301", "category": "main", "price": 150000, "status": "available"},
    {"dish_code": " f101 ", "category": "appetizer", "price": 55000, "status": "available"},
    {"dish_code": "F202", "category": "dessert", "price": 45000, "status": "sold_out"},
    {"dish_code": "F102", "category": "appetizer", "price": 65000, "status": "unavailable"},
    {"dish_code": "F302", "category": "main", "price": 180000, "status": "available"}
]

def clean_and_validate_dishes(dishes):
    valid_dishes = []
    for dish in dishes:
        dish["dish_code"] = dish["dish_code"].strip().upper()
        code = dish["dish_code"]
        if len(code) > 1 and code[0] == 'F':
            is_valid = True
            for char in code[1:]:
                if not char.isdigit():
                    is_valid = False
                    break
            if is_valid == True:
                valid_dishes.append(dish)
    return valid_dishes






cleaned_dishes = clean_and_validate_dishes(raw_dishes)
print(cleaned_dishes)
    

    
