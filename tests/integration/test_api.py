import pytest
from app.main import app

# 1. KULLANICI ENTEGRASYONLARI
def test_create_user(client):
    # Veri tabanına kayıt düştü mü?
    response = client.post("/users/", json={"email": "integration@test.com", "password": "securepassword"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "integration@test.com"
    assert "id" in data

def test_create_user_duplicate_email(client):
    # AYNI mail ile tekrar kayıt (Hata Senaryosu - 400 Bad Request)
    client.post("/users/", json={"email": "duplicate@test.com", "password": "123"})
    response = client.post("/users/", json={"email": "duplicate@test.com", "password": "456"})
    assert response.status_code == 400
    assert "zaten kayıtlı" in response.json()["detail"]

def test_read_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# 2. KATEGORİ ENTEGRASYONLARI
def test_create_category(client):
    response = client.post("/categories/", json={"name": "Entegrasyon Kategori"})
    assert response.status_code == 200
    assert response.json()["name"] == "Entegrasyon Kategori"

# 3. ÜRÜN ENTEGRASYONLARI (İlişkili Kaynak Testi)
def test_create_product(client):
    # Ürün oluşturmak için önce Kategori ID'si lazım (Entegrasyon burası)
    cat_res = client.post("/categories/", json={"name": "Laptoplar"})
    cat_id = cat_res.json()["id"]
    
    response = client.post("/products/", json={
        "name": "MacBook Pro",
        "price": 50000.0,
        "stock": 5,
        "category_id": cat_id
    })
    assert response.status_code == 200
    assert response.json()["category_id"] == cat_id

def test_get_product_not_found(client):
    # Olmayan ID testi (Hata Senaryosu - 404 Not Found)
    response = client.get("/products/99999")
    assert response.status_code == 404

def test_update_product(client):
    # Oluştur -> Güncelle akışı
    cat_res = client.post("/categories/", json={"name": "Telefonlar"})
    prod_res = client.post("/products/", json={
        "name": "iPhone 11",
        "price": 20000.0,
        "stock": 10,
        "category_id": cat_res.json()["id"]
    })
    prod_id = prod_res.json()["id"]

    # Fiyatı güncelle
    update_res = client.put(f"/products/{prod_id}", json={"price": 25000.0})
    assert update_res.status_code == 200
    assert update_res.json()["price"] == 25000.0

def test_delete_product(client):
    # Oluştur -> Sil -> Kontrol Et
    cat_res = client.post("/categories/", json={"name": "Silinecekler"})
    prod_res = client.post("/products/", json={"name": "Sil Beni", "price": 10, "stock": 1, "category_id": cat_res.json()["id"]})
    prod_id = prod_res.json()["id"]

    # Sil
    del_res = client.delete(f"/products/{prod_id}")
    assert del_res.status_code == 200
    
    # Gerçekten silindi mi? (404 dönmeli)
    get_res = client.get(f"/products/{prod_id}")
    assert get_res.status_code == 404

# 4. SİPARİŞ ENTEGRASYONLARI (User + Product + Order İlişkisi)
def test_create_order(client):
    # Sipariş için User ve Product lazım
    user_res = client.post("/users/", json={"email": "buyer@int.com", "password": "123"})
    user_id = user_res.json()["id"]
    
    cat_res = client.post("/categories/", json={"name": "Sipariş Kategori"})
    prod_res = client.post("/products/", json={"name": "Kalem", "price": 10.0, "stock": 100, "category_id": cat_res.json()["id"]})
    prod_id = prod_res.json()["id"]

    # Sipariş ver
    order_data = {"items": [{"product_id": prod_id, "quantity": 5}]}
    res = client.post(f"/orders/?user_id={user_id}", json=order_data)
    
    assert res.status_code == 200
    assert res.json()["total_amount"] == 50.0 # 10.0 * 5 = 50.0 olmalı
    assert res.json()["status"] == "pending"

def test_update_order_status(client):
    # Sipariş statü güncelleme testi
    # Hızlıca user/product/order oluşturuyoruz
    user_id = client.post("/users/", json={"email": "status@int.com", "password": "123"}).json()["id"]
    cat_id = client.post("/categories/", json={"name": "Status Cat"}).json()["id"]
    prod_id = client.post("/products/", json={"name": "Silgi", "price": 5.0, "stock": 50, "category_id": cat_id}).json()["id"]
    
    order_id = client.post(f"/orders/?user_id={user_id}", json={"items": [{"product_id": prod_id, "quantity": 1}]}).json()["id"]

    # Statü değişiyor mu?
    res = client.put(f"/orders/{order_id}/status?status=shipped")
    assert res.status_code == 200
    assert res.json()["status"] == "shipped"

def test_create_review(client):
    # Yorum testi
    user_id = client.post("/users/", json={"email": "review@int.com", "password": "123"}).json()["id"]
    cat_id = client.post("/categories/", json={"name": "Review Cat"}).json()["id"]
    prod_id = client.post("/products/", json={"name": "Defter", "price": 20.0, "stock": 50, "category_id": cat_id}).json()["id"]
    
    res = client.post(f"/reviews/?user_id={user_id}", json={
        "product_id": prod_id,
        "rating": 5,
        "comment": "Harika ürün"
    })
    assert res.status_code == 200
    assert res.json()["rating"] == 5