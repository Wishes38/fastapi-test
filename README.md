# FastAPI E-Commerce API Project for Test

![CI Status](https://github.com/Wishes38/fastapi-test/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/github/Wishes38/fastapi-test/graph/badge.svg?token=K00URDU4LB)](https://codecov.io/github/Wishes38/fastapi-test)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

Bu proje, **FastAPI** framework'ü kullanılarak geliştirilmiş bir E-Ticaret REST API uygulamasıdır. Kullanıcı yönetimi, ürün kataloğu, sipariş işleme ve yorumlama gibi temel e-ticaret fonksiyonlarını içerir. Proje; modern yazılım geliştirme prensiplerine (SOLID), Test Driven Development (TDD) yaklaşımlarına ve CI/CD süreçlerine uygun olarak hazırlanmıştır.

## 🛠️ Kullanılan Teknolojiler

* **Framework:** FastAPI
* **Dil:** Python 3.10+
* **Veritabanı:** PostgreSQL (Production & Test Ortamları)
* **ORM:** SQLAlchemy (Asenkron destekli)
* **Validasyon:** Pydantic v2
* **Konteynerizasyon:** Docker & Docker Compose
* **Güvenlik:** Argon2 & Passlib (Güvenli Şifreleme / Hashing)
* **Test:** Pytest, HTTPX, Pytest-Cov
* **CI/CD:** GitHub Actions, Codecov

---

## 🚀 Kurulum Talimatları (Adım Adım)

Projeyi yerel ortamınızda çalıştırmak için aşağıdaki adımları takip edin.

### 1. Projeyi Klonlayın
```bash
git clone  https://github.com/Wishes38/fastapi-test.git
cd fastapi-test
```

⚠️ Önemli Not: Projenin çalışması için gerekli olan çevresel değişkenlerin bulunduğu .env dosyası repo içerisine dahil edilmiştir. Klonlama işleminden sonra ekstra bir .env dosyası oluşturmanıza gerek yoktur, mevcut dosya otomatik olarak kullanılacaktır.

Sanal Ortamı (Virtual Environment) Kurun
```bash
# Windows için:
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux için:
python3 -m venv venv
source venv/bin/activate
```
2. Gereksinimleri Yükleyin
```bash
pip install -r requirements.txt
```

Docker ile Çalıştırma 🐳
```bash
docker-compose up -d --build
```

Uvicorn ile Projeyi Başlatma

```bash
uvicorn app.main:app --reload
```

📖 API Dokümantasyonu (Swagger & OpenAPI)
FastAPI'nin sunduğu otomatik dokümantasyon arayüzleri sayesinde tüm endpoint'leri tarayıcı üzerinden deneyebilirsiniz.

Swagger UI (İnteraktif): http://127.0.0.1:8000/docs

ReDoc (Alternatif Görünüm): http://127.0.0.1:8000/redoc

OpenAPI JSON: http://127.0.0.1:8000/openapi.json

## 🔌 API Endpoint Listesi

Projede bulunan tüm kaynaklar ve işlevleri aşağıda listelenmiştir.

### 👤 Users (Kullanıcı İşlemleri)
| Metot | Endpoint | Açıklama | Parametreler / Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/users/` | Yeni kullanıcı oluştur | **Body:** `UserCreate` |
| `GET` | `/users/` | Tüm kullanıcıları listele | **Query:** `skip`, `limit` |
| `GET` | `/users/{user_id}` | Tek bir kullanıcıyı getir | **Path:** `user_id` |
| `PUT` | `/users/{user_id}` | Kullanıcı bilgilerini güncelle | **Path:** `user_id`, **Body:** `UserUpdate` |
| `DELETE` | `/users/{user_id}` | Kullanıcıyı sil | **Path:** `user_id` |

### 📦 Products (Ürün İşlemleri)
| Metot | Endpoint | Açıklama | Parametreler / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/products/` | Tüm ürünleri listele | **Query:** `skip`, `limit` |
| `POST` | `/products/` | Yeni ürün ekle | **Body:** `ProductCreate` |
| `GET` | `/products/{product_id}` | Ürün detayını görüntüle | **Path:** `product_id` |
| `DELETE` | `/products/{product_id}` | Ürünü sil | **Path:** `product_id` |
| `PUT` | `/products/{product_id}` | Ürün bilgilerini güncelle | **Path:** `product_id`, **Body:** `ProductUpdate` |

### 📂 Categories (Kategori İşlemleri)
| Metot | Endpoint | Açıklama | Parametreler / Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/categories/` | Yeni kategori oluştur | **Body:** `CategoryCreate` |
| `GET` | `/categories/` | Tüm kategorileri listele | **Query:** `skip`, `limit` |
| `GET` | `/categories/{category_id}` | Kategori detayını görüntüle | **Path:** `category_id` |
| `PUT` | `/categories/{category_id}` | Kategoriyi güncelle | **Path:** `category_id`, **Body:** `CategoryUpdate` |
| `DELETE` | `/categories/{category_id}` | Kategoriyi sil | **Path:** `category_id` |

### 🛒 Orders (Sipariş İşlemleri)
| Metot | Endpoint | Açıklama | Parametreler / Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/orders/` | Yeni sipariş oluştur | **Query:** `user_id`, **Body:** `OrderCreate` |
| `GET` | `/orders/` | Tüm siparişleri listele | **Query:** `skip`, `limit` |
| `GET` | `/orders/{order_id}` | Sipariş detayını görüntüle | **Path:** `order_id` |
| `DELETE` | `/orders/{order_id}` | Siparişi sil | **Path:** `order_id` |
| `PUT` | `/orders/{order_id}/status` | Sipariş durumunu güncelle | **Path:** `order_id`, **Query:** `status` |

### ⭐ Reviews (Yorum ve Değerlendirme)
| Metot | Endpoint | Açıklama | Parametreler / Body |
| :--- | :--- | :--- | :--- |
| `POST` | `/reviews/` | Yorum yap | **Query:** `user_id`, **Body:** `ReviewCreate` |
| `GET` | `/reviews/product/{product_id}` | Bir ürüne ait yorumları getir | **Path:** `product_id` |
| `GET` | `/reviews/{review_id}` | Yorum detayını görüntüle | **Path:** `review_id` |
| `PUT` | `/reviews/{review_id}` | Yorumu güncelle | **Path:** `review_id`, **Body:** `ReviewUpdate` |
| `DELETE` | `/reviews/{review_id}` | Yorumu sil | **Path:** `review_id` |

### 🌐 General
| Metot | Endpoint | Açıklama | Parametreler / Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Root (API Sağlık Kontrolü) | - |


```bash
pytest
```

Test Coverage (Kapsama) Raporu Almak İçin:
```bash
pytest --cov=app tests/
```
Detaylı HTML Raporu İçin:
```bash
pytest --cov=app --cov-report=html tests/
# Oluşan htmlcov/index.html dosyasını tarayıcıda açın.
```

⚙️ CI/CD ve Test Otomasyonu
Bu proje GitHub Actions kullanılarak sürekli entegrasyon (CI) sürecine dahil edilmiştir. Test tutarlılığı (Consistency) için test ortamında da üretim ortamındaki gibi PostgreSQL kullanılmaktadır.

GitHub Actions: Her push ve pull request işleminde otomatik olarak tetiklenir.

Sanal bir Linux sunucusu üzerinde PostgreSQL Service Container başlatılır.

Tüm testler (pytest) bu izole veritabanı ortamında koşulur.

Codecov Entegrasyonu:

Testler tamamlandığında coverage raporu otomatik olarak Codecov servisine yüklenir.

Projenin test kapsamı rozet (badge) olarak bu dosyanın en üstünde görüntülenir.
