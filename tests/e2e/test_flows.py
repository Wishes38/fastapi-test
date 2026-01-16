import pytest
from app.main import app

# SENARYO 1: Tam Alışveriş Döngüsü (Kullanıcı -> Kategori -> Ürün -> Sipariş)

def test_flow_full_shopping_cycle(client):
    # 1. Kullanıcı Sisteme Kaydolur
    user_res = client.post("/users/", json={"email": "shopper@e2e.com", "password": "123"})
    assert user_res.status_code == 200
    user_id = user_res.json()["id"]

    # 2. Yönetici Kategori Ekler
    cat_res = client.post("/categories/", json={"name": "Gaming"})
    cat_id = cat_res.json()["id"]

    # 3. Yönetici Ürün Ekler
    prod_res = client.post("/products/", json={
        "name": "PS5", "price": 20000.0, "stock": 50, "category_id": cat_id
    })
    prod_id = prod_res.json()["id"]

    # 4. Kullanıcı O Ürünü Sipariş Verir
    order_res = client.post(f"/orders/?user_id={user_id}", json={
        "items": [{"product_id": prod_id, "quantity": 1}]
    })
    
    # Sonuç: Sipariş başarıyla oluşmalı ve tutar doğru hesaplanmalı
    assert order_res.status_code == 200
    assert order_res.json()["total_amount"] == 20000.0

# SENARYO 2: Ürün Yaşam Döngüsü (Ekle -> Güncelle -> Oku -> Sil)
def test_flow_product_lifecycle(client):
    # Setup: Kategori lazım
    cat_id = client.post("/categories/", json={"name": "Lifecycle Cat"}).json()["id"]
    
    # 1. Ürün Ekle
    prod_res = client.post("/products/", json={"name": "Eski Model", "price": 100.0, "stock": 10, "category_id": cat_id})
    prod_id = prod_res.json()["id"]

    # 2. Ürünü Güncelle (Fiyat Artışı ve İsim Değişikliği)
    client.put(f"/products/{prod_id}", json={"price": 150.0, "name": "Yeni Model"})
    
    # 3. Güncellemeyi Doğrula
    get_res = client.get(f"/products/{prod_id}")
    assert get_res.json()["price"] == 150.0
    assert get_res.json()["name"] == "Yeni Model"

    # 4. Ürünü Sil
    client.delete(f"/products/{prod_id}")
    
    # 5. Silindiğini Doğrula
    assert client.get(f"/products/{prod_id}").status_code == 404

# SENARYO 3: Kullanıcı Profil Yönetimi (Kayıt -> Pasife Al -> Sil)
def test_flow_user_management(client):
    # 1. Kayıt
    res = client.post("/users/", json={"email": "profile@e2e.com", "password": "123"})
    user_id = res.json()["id"]

    # 2. Profil Getir
    assert client.get(f"/users/{user_id}").status_code == 200

    # 3. Profili Pasife Al (Soft Delete mantığı güncelleme ile)
    client.put(f"/users/{user_id}", json={"is_active": False})
    
    # 4. Kontrol Et (Pasif mi?)
    user_data = client.get(f"/users/{user_id}").json()
    assert user_data["is_active"] is False

    # 5. Tamamen Sil (Soft Delete Endpoint)
    del_res = client.delete(f"/users/{user_id}")
    assert del_res.status_code == 200

# SENARYO 4: Sipariş Yönetimi ve İptali
def test_flow_order_management(client):
    # Setup (Bağımsız veri oluşturma)
    user_id = client.post("/users/", json={"email": "order_man@e2e.com", "password": "123"}).json()["id"]
    cat_id = client.post("/categories/", json={"name": "Order Cat"}).json()["id"]
    prod_id = client.post("/products/", json={"name": "T-Shirt", "price": 50.0, "stock": 100, "category_id": cat_id}).json()["id"]

    # 1. Sipariş Ver
    order_id = client.post(f"/orders/?user_id={user_id}", json={"items": [{"product_id": prod_id, "quantity": 2}]}).json()["id"]

    # 2. Durum Güncelle (Kargolandı)
    client.put(f"/orders/{order_id}/status?status=shipped")
    
    # 3. Kontrol
    assert client.get(f"/orders/{order_id}").json()["status"] == "shipped"

    # 4. Siparişi Sil (İptal)
    client.delete(f"/orders/{order_id}")
    assert client.get(f"/orders/{order_id}").status_code == 404

# SENARYO 5: Yorum ve Değerlendirme Akışı
def test_flow_reviews(client):
    # Setup
    user_id = client.post("/users/", json={"email": "critic@e2e.com", "password": "123"}).json()["id"]
    cat_id = client.post("/categories/", json={"name": "Review Cat"}).json()["id"]
    prod_id = client.post("/products/", json={"name": "Book", "price": 25.0, "stock": 100, "category_id": cat_id}).json()["id"]

    # 1. Yorum Yap
    rev_res = client.post(f"/reviews/?user_id={user_id}", json={"product_id": prod_id, "rating": 5, "comment": "Harika"})
    rev_id = rev_res.json()["id"]

    # 2. Yorumu Ürün Altında Gör
    prod_reviews = client.get(f"/reviews/product/{prod_id}").json()
    assert len(prod_reviews) > 0
    assert prod_reviews[0]["comment"] == "Harika"

    # 3. Yorumu Düzenle
    client.put(f"/reviews/{rev_id}", json={"comment": "Fena değil", "rating": 3})
    
    # 4. Düzenlemeyi Kontrol Et
    updated_rev = client.get(f"/reviews/{rev_id}").json()
    assert updated_rev["comment"] == "Fena değil"
    assert updated_rev["rating"] == 3

    # 5. Yorumu Sil
    client.delete(f"/reviews/{rev_id}")
    assert client.get(f"/reviews/{rev_id}").status_code == 404