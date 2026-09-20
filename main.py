from fastapi import FastAPI

app = FastAPI()
#Path Parameters

#Users dynamic Route
@app.get("/users1/{user_id1}")
def get_users1(user_id1):
    return {"user_id1": user_id1}

#Users dynamic Route with validation
@app.get("/users2/{user_id2}")
def get_users2(user_id2:int):
    return {"user_id2": user_id2}

#Users dynamic Route with validation
@app.get("/users/{user_id}")
def get_users(user_id:str):
    return {"user_id": user_id}


