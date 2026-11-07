
import sqlite3
from pathlib import Path
from typing import Any

from schema.ProductCreate import ProductCreate
from schema.ProductUpdate import ProductUpdate


class Database:
    def __init__(self, db_name: str = "products.db"):
        self.db_path = Path(db_name)
        self.create_table()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def create_table(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    stock INTEGER NOT NULL,
                    status TEXT NOT NULL
                )
            """)

    def create(self, product: ProductCreate) -> int:
        data = product.model_dump()

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO products (name, price, stock, status)
                VALUES (?, ?, ?, ?)
                """,
                (data["name"], data["price"], data["stock"], data["status"])
            )
            return int(cursor.lastrowid)

    def get_product(self, product_id: int) -> dict[str, Any] | None:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()

            return dict(row) if row else None

    def get_all_products(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(
                "SELECT * FROM products ORDER BY id"
            ).fetchall()

            return [dict(row) for row in rows]

    def update(
        self,
        product_id: int,
        product_update: ProductUpdate
    ) -> dict[str, Any] | None:

        data = product_update.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        if not data:
            return self.get_product(product_id)

        columns = {"name", "price", "stock", "status"}

        if not data.keys() <= columns:
            raise ValueError("Unsupported product field")

        assignments = ", ".join(
            f"{column} = ?" for column in data
        )

        with self._connect() as conn:
            cursor = conn.execute(
                f"UPDATE products SET {assignments} WHERE id = ?",
                (*data.values(), product_id)
            )

            if cursor.rowcount == 0:
                return None

        return self.get_product(product_id)

    def delete(self, product_id: int) -> bool:
        with self._connect() as conn:
            cursor = conn.execute(
                "DELETE FROM products WHERE id = ?",
                (product_id,)
            )

            return cursor.rowcount > 0
