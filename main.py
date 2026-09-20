from fastapi import FastAPI

app = FastAPI()
#Query Parameters
#uses: filtering , searching ,sorting etc
#eg.
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