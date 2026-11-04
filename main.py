from fastapi import FastAPI

app = FastAPI()
# B. Query parameters
# Query parameters are values provided after ? in a URL.
# Example:
# /students?course=CSE&year=3

# 'http://127.0.0.1:8000/students?course=CSE&year=3' 


# Here:
# - course=CSE
# - year=3
# Implementation:
@app.get("/students")
def get_students(course: str, year: int):
    return {
        "course": course,
        "year": year
    }

# _____________________________________
# Example 2:
# url/users?name=abdul
# url/product?price=200

@app.get("/users1")
def get_users(name):
    return {"name":name}

#optional parameters
@app.get("/users2")
def get_users(name:str = None ):
    return {"name":name}

#default values parameters
@app.get("/products")
def get_users(limit: int =10 ):
    return {"limit":limit}

#multiple query parameters
@app.get("/items")
def get_items(item: str = None,price: int=0 ):
    return {
        "item":item,
        "price":price
    }
