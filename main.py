from fastapi import FastAPI

# API fundamentals
# - What is REST API?
# - HTTP methods: GET, POST, PUT, PATCH, DELETE
# - HTTP status codes
# - Request and response
# - JSON
# - Path parameters
# - Query parameters
# Create a FastAPI application
app = FastAPI() # create the fastAPI applications objects 

#Home Route
@app.get("/")
def home():
    return {"message": "Welcome to my FastAPI Journey!"}}

#About Route
@app.get("/about")
def about():
    return {
    "name": "Abdul Rahman Ali",
    "course": "B.Tech CSE",
    "year": 3
}

#Skills Route
@app.get("/skills")
def skills():
    return {
    "skills": ["Python", "C", "HTML", "CSS", "JavaScript"]
}
