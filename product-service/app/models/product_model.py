from typing import Optional, List, Literal
from sqlmodel import SQLModel, Field, Relationship


class Size(SQLModel, table=True):
    """
    Represents a specific size of a product item.

    Attributes:
        size_id (Optional[int]): Primary key for size.
        size (str): Size of the product (e.g., S, M, L).
        price (int): Price associated with this size.
        product_item_id (Optional[int]): Foreign key linking to ProductItem.
        stock (Stock): One-to-one relationship with Stock.
        product_item (Optional[ProductItem]): Many-to-one relationship with ProductItem.
    """
    size_id: Optional[int] = Field(None, primary_key=True)
    size: str  # Size of the product (e.g., S, M, L)
    price: int = Field(gt=0)  # Price associated with this size
    product_item_id: Optional[int] = Field(
        # Foreign key linking to ProductItem
        default=None, foreign_key="productitem.item_id")
    # One-to-one relationship with Stock
    stock: "Stock" = Relationship(back_populates="size")
    product_item: Optional["ProductItem"] = Relationship(
        back_populates="sizes")  # Many-to-one relationship with ProductItem


class ProductBase(SQLModel):
    """
    Base model for Product, used for shared attributes.

    Attributes:
        product_name (str): Name of the product.
        description (str): Description of the product.
    """
    product_name: str  # Name of the product
    description: str  # Description of the product


class ProductItemBase(SQLModel):
    """
    Base model for ProductItem, used for shared attributes.

    Attributes:
        color (str): Color of the product item.
    """
    color: str  # Color of the product item


class SizeModel(SQLModel):
    """
    Model for representing size details in forms.

    Attributes:
        size (str): Size of the product item.
        price (int): Price of the product item.
        stock (int): Stock level of the product item.
    """
    size: str  # Size of the product item
    price: int = Field(gt=0)  # Price of the product item
    stock: int  # Stock level of the product item


class ProductItemFormModel(ProductItemBase):
    """
    Model for representing product item details in forms.

    Attributes:
        sizes (List[SizeModel]): List of sizes for the product item.
    """
    sizes: List[SizeModel]  # List of sizes for the product item


class ProductFormModel(ProductBase):
    """
    Model for representing product details in forms.

    Attributes:
        product_items (List[ProductItemFormModel]): List of product items.
    """
    product_items: List[ProductItemFormModel]  # List of product items


class Product(ProductBase, table=True):
    """
    Database model for products.

    Attributes:
        product_id (Optional[int]): Primary key for Product.
        category_id (int): Foreign key linking to Category.
        gender_id (int): Foreign key linking to Gender.
        product_items (List[ProductItem]): One-to-many relationship with ProductItem.
    """
    product_id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for Product
    # Foreign key linking to Category
    category_id: int = Field(foreign_key="category.category_id")
    # Foreign key linking to Gender
    gender_id: int = Field(foreign_key="gender.gender_id")
    product_items: List["ProductItem"] = Relationship(
        back_populates="product")  # One-to-many relationship with ProductItem


class ProductItem(ProductItemBase, table=True):
    """
    Database model for product items.

    Attributes:
        item_id (Optional[int]): Primary key for ProductItem.
        product_id (Optional[int]): Foreign key linking to Product.
        image_url (str): URL of the product item image.
        product (Optional[Product]): Many-to-one relationship with Product.
        sizes (List[Size]): One-to-many relationship with Size.
    """
    item_id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for ProductItem
    # Foreign key linking to Product
    product_id: Optional[int] = Field(
        default=None, foreign_key="product.product_id")
    image_url: str  # URL of the product item image
    # Many-to-one relationship with Product
    product: Optional[Product] = Relationship(back_populates="product_items")
    # One-to-many relationship with Size
    sizes: List[Size] = Relationship(back_populates="product_item")


class Stock(SQLModel, table=True):
    """
    Database model for stock levels.

    Attributes:
        stock_id (Optional[int]): Primary key for Stock.
        size_id (Optional[int]): Foreign key linking to Size.
        stock (int): Stock level.
        size (Optional[Size]): One-to-one relationship with Size.

    Properties:
        stock_level (Literal["Low", "Medium", "High"]): Categorizes stock level as "Low", "Medium", or "High".
    """
    stock_id: Optional[int] = Field(
        default=None, primary_key=True)  # Primary key for Stock
    # Foreign key linking to Size
    size_id: Optional[int] = Field(default=None, foreign_key="size.size_id")
    stock: int = 0  # Stock level
    # One-to-one relationship with Size
    size: Optional[Size] = Relationship(back_populates="stock")

    @property
    def stock_level(self) -> Literal["Low", "Medium", "High"]:
        """
        Categorizes the stock level based on the quantity.

        Returns:
            Literal["Low", "Medium", "High"]: Stock level category.
        """
        if self.stock > 100:
            return "High"
        elif self.stock > 50:
            return "Medium"
        else:
            return "Low"


# Sample JSON payload for creating a product
sample_payload = {
    "product_name": "Shirt",
    "product_description": "New Shirt",
    "product_items": [
        {
            "color": "green",
            "image_url": "http://www.shirt.com",
            "sizes": [
                {
                    "size": "small",
                    "price": 200,
                    "stock": 50
                },
                {
                    "size": "medium",
                    "price": 250,
                    "stock": 10
                },
                {
                    "size": "large",
                    "price": 300,
                    "stock": 0
                }
            ]

        },
        {
            "color": "brown",
            "image_url": "http://www.shirt.com",
            "sizes": [
                {
                    "size": "extra small",
                    "price": 100,
                    "stock": 70
                },
                {
                    "size": "medium",
                    "price": 250,
                    "stock": 10
                },
                {
                    "size": "large",
                    "price": 300,
                    "stock": 0
                }
            ]
        },
        {
            "color": "black",
            "image_url": "http://www.shirt.com",
            "sizes": [
                {
                    "size": "small",
                    "price": 200,
                    "stock": 50
                },
                {
                    "size": "medium",
                    "price": 250,
                    "stock": 10
                },
                {
                    "size": "large",
                    "price": 300,
                    "stock": 0
                }
            ]
        }
    ]
}