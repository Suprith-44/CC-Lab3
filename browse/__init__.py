from products import dao


class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @classmethod
    def load(cls, data: dict):
        """
        Create a Product instance from a dictionary.
        """
        return cls(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            cost=data['cost'],
            qty=data.get('qty', 0)  # Default to 0 if qty is missing
        )


def list_products() -> list[Product]:
    """
    Retrieve a list of all products from the database.

    Returns:
        list[Product]: A list of Product objects.
    """
    products_data = dao.list_products()
    return [Product.load(product) for product in products_data]  # List comprehension for efficiency


def get_product(product_id: int) -> Product:
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The ID of the product.

    Returns:
        Product: The corresponding Product object.
    """
    product_data = dao.get_product(product_id)
    return Product.load(product_data)


def add_product(product: dict):
    """
    Add a new product to the database.

    Args:
        product (dict): A dictionary containing product details.
    """
    dao.add_product(product)


def update_qty(product_id: int, qty: int):
    """
    Update the quantity of a specific product.

    Args:
        product_id (int): The ID of the product to update.
        qty (int): The new quantity for the product.

    Raises:
        ValueError: If qty is negative.
    """
    if qty < 0:
        raise ValueError('Quantity cannot be negative')
    dao.update_qty(product_id, qty)
