import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate
from app.schemas.product import ProductCreate
from app.schemas.category import CategoryCreate
from app.schemas.order import OrderItemBase
from app.schemas.review import ReviewCreate

# USER TESTLERİ

# Test 5
def test_user_create_valid():
    user = UserCreate(email="test@example.com", password="123")
    assert user.email == "test@example.com"
    assert user.password == "123"

# Test 6
def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreate(email="mail-degil", password="123")

# Test 7
def test_user_create_missing_fields():
    with pytest.raises(ValidationError):
        UserCreate(email="test@example.com") # Password eksik

# PRODUCT TESTLERİ

# Test 8
def test_product_create_valid():
    prod = ProductCreate(name="Laptop", price=100.0, stock=10, category_id=1)
    assert prod.name == "Laptop"

# Test 9: Eksik veri kontrolü
def test_product_missing_price():
    with pytest.raises(ValidationError):
        ProductCreate(name="Laptop", stock=10, category_id=1) # Price eksik

# Test 10: Yanlış veri tipi
def test_product_invalid_price_type():
    with pytest.raises(ValidationError):
        ProductCreate(name="Laptop", price="yuz", stock=10, category_id=1)

# Test 11: Opsiyonel alan (Description)
def test_product_optional_description():
    # Description göndermesek de hata vermemeli
    prod = ProductCreate(name="Mouse", price=50.0, stock=5, category_id=2)
    assert prod.description is None

# CATEGORY TESTLERİ

# Test 12
def test_category_create_valid():
    cat = CategoryCreate(name="Elektronik")
    assert cat.name == "Elektronik"

# Test 13
def test_category_missing_name():
    with pytest.raises(ValidationError):
        CategoryCreate() # name eksik

# ORDER TESTLERİ

# Test 14
def test_order_item_valid():
    item = OrderItemBase(product_id=1, quantity=5)
    assert item.quantity == 5

# Test 15
def test_order_item_invalid_quantity_type():
    with pytest.raises(ValidationError):
        OrderItemBase(product_id=1, quantity="beş")

# REVIEW TESTLERİ

# Test 16: Geçerli Yorum
def test_review_create_valid():
    rev = ReviewCreate(product_id=1, rating=5, comment="Süper")
    assert rev.rating == 5

# Test 17: Eksik Rating
def test_review_missing_rating():
    with pytest.raises(ValidationError):
        ReviewCreate(product_id=1, comment="Puan vermedim")