from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from vendingmachine.common.base_manager import BaseManager
from vendingmachine.user import models as user_models

from . import models, schemas


class ProductManager(BaseManager):
    def create_product(self, product: schemas.CreateProduct, created_by: int):
        db_product = models.Product(
            name=product.name,
            description=product.description,
            price=product.price,
            created_by=created_by,  # type: ignore
        )
        inventory = models.Inventory(product=db_product, quantity=product.inventory_count)  # type: ignore
        self.db.add(db_product)
        self.db.add(inventory)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def list_products(self):
        return self.db.query(models.Product).options(selectinload(models.Product.inventory)).all()

    def get_product(self, product_id: int):
        p = self.db.query(models.Product).filter(models.Product.id == product_id).first()
        if not p:
            raise HTTPException(status_code=404, detail="Product not found")

        return p

    def get_product_inventory(self, product_id: int):
        inventory = self.db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
        if not inventory:
            raise HTTPException(status_code=404, detail="Inventory not found")

        return inventory

    def update_product(
        self,
        current_user: user_models.User,
        product_id: int,
        product: schemas.UpdateProduct,
    ):
        db_product = self.get_product(product_id)
        if db_product.created_by != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to update this product",
            )

        for key, value in product.model_dump().items():
            if value is not None:
                if key == "inventory_count":
                    inventory = (
                        self.db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
                    )
                    inventory.quantity = value  # type: ignore
                else:
                    setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete_product(self, current_user: user_models.User, product_id: int):
        db_product = self.get_product(product_id)
        if db_product.created_by != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to delete this product",
            )

        self.db.delete(db_product)
        self.db.commit()
        return db_product

    def reduce_product_inventory(self, product_id: int, quantity: int):
        inventory = self.db.query(models.Inventory).filter(models.Inventory.product_id == product_id).first()
        inventory.quantity -= quantity  # type: ignore
        self.db.commit()
