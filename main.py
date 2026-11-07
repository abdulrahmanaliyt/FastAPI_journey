from typing import Any

from fastapi import FastAPI, HTTPException, status

from database.database_class import Database
from schema.ProductCreate import ProductCreate
from schema.ProductUpdate import ProductUpdate


app = FastAPI(title="Product API")
db = Database()

@app.get("/products")
def get_products() -> list[dict[str, Any]]:
    return db.get_all_products()

@app.get("/product/{product_id}")
def get_product(product_id: int) -> dict[str, Any]:
    product = db.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@app.post("/product", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate) -> dict[str, Any]:
    new_id = db.create(product)
    return {"message": "Product created successfully", "product_id": new_id}


@app.patch("/product/{product_id}")
def update_product(product_id: int, product_update: ProductUpdate) -> dict[str, Any]:
    updated_product = db.update(product_id, product_update)
    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return updated_product


@app.delete("/product/{product_id}")
def delete_product(product_id: int) -> dict[str, str]:
    if not db.delete(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {"message": "Product deleted successfully"}
