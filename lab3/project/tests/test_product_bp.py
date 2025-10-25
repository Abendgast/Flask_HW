import unittest
from app import app

class ProductsTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_products_index(self):
        """Тест головної сторінки продуктів."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("продукт".encode('utf-8'), response.data)

if __name__ == "__main__":
    unittest.main()
