Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_add_item_to_order():
    # Тест добавления товара в заказ
    response = client.post("/orders/1/items", json={
        "order_id": 1,
        "product_id": 1,
        "quantity": 2
    })
    assert response.status_code == 200
    assert response.json()["quantity"] == 2

def test_out_of_stock():
    # Тест недостатка товара
    response = client.post("/orders/1/items", json={
        "order_id": 1,
        "product_id": 1,
        "quantity": 1000
    })
    assert response.status_code == 400

def test_nonexistent_product():
    # Тест несуществующего товара
    response = client.post("/orders/1/items", json={
        "order_id": 1,
        "product_id": 999,
        "quantity": 1
    })
    assert response.status_code == 404