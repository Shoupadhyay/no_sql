from langchain import LangChain
import os
from app_init import app

class LangChainIntegration:
    def __init__(self):
        self.api_key = os.environ['GOOGLE_GEMINI_API_KEY']
        self.model = LangChain(api_key=self.api_key, model_name="gemini-flash-1.5")

    def fine_tune_model(self, schema: str, examples: list, few_shot_params: dict):
        # Fine-tune the model with the provided schema, examples, and few-shot parameters
        self.model.fine_tune(schema=schema, examples=examples, **few_shot_params)

    def ask_question(self, question: str):
        # Ask a question to the fine-tuned model
        response = self.model.ask(question)
        return response

# Custom few-shot learning parameters
few_shot_params = {
    "examples": [
        {"input": "SELECT u.name, o.amount FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount > 100;", "output": "Returns the names of users and their order amounts where the amount is greater than 100."},
        {"input": "SELECT p.name, SUM(i.quantity) FROM products p JOIN inventory i ON p.id = i.product_id GROUP BY p.name;", "output": "Returns the names of products and the sum of their quantities in inventory."},
        {"input": "SELECT s.name, COUNT(ps.product_id) FROM suppliers s JOIN product_suppliers ps ON s.id = ps.supplier_id GROUP BY s.name;", "output": "Returns the names of suppliers and the count of products they supply."},
        {"input": "SELECT u.name, COUNT(o.id) FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'shipped' GROUP BY u.name;", "output": "Returns the names of users and the count of their shipped orders."},
        {"input": "SELECT p.name, AVG(r.rating) FROM products p JOIN reviews r ON p.id = r.product_id GROUP BY p.name;", "output": "Returns the names of products and the average rating for each product."},
        {"input": "SELECT c.name, COUNT(pc.product_id) FROM categories c JOIN product_categories pc ON c.id = pc.category_id GROUP BY c.name;", "output": "Returns the names of categories and the count of products in each category."},
        {"input": "SELECT u.name, SUM(t.amount) FROM users u JOIN transactions t ON u.id = t.user_id GROUP BY u.name;", "output": "Returns the names of users and the sum of their transaction amounts."},
        {"input": "SELECT p.name, i.quantity FROM products p JOIN inventory i ON p.id = i.product_id WHERE i.quantity < 10;", "output": "Returns the names of products and their quantities where the quantity is less than 10."},
        {"input": "SELECT u.name, o.product, o.amount FROM users u JOIN orders o ON u.id = o.user_id WHERE o.order_date > '2023-01-01';", "output": "Returns the names of users, their ordered products, and order amounts for orders placed after January 1, 2023."},
        {"input": "SELECT u.name, o.amount, u.email FROM users u JOIN orders o ON u.id = o.user_id WHERE o.amount > 100;", "output": "Returns the names, emails of users and their order amounts where the amount is greater than 100."},
        {"input": "SELECT p.name, SUM(i.quantity), p.price FROM products p JOIN inventory i ON p.id = i.product_id GROUP BY p.name, p.price;", "output": "Returns the names of products, their prices, and the sum of their quantities in inventory."},
        {"input": "SELECT s.name, COUNT(ps.product_id), s.contact_info FROM suppliers s JOIN product_suppliers ps ON s.id = ps.supplier_id GROUP BY s.name, s.contact_info;", "output": "Returns the names of suppliers, their contact info, and the count of products they supply."},
        {"input": "SELECT u.name, COUNT(o.id), u.address FROM users u JOIN orders o ON u.id = o.user_id WHERE o.status = 'shipped' GROUP BY u.name, u.address;", "output": "Returns the names of users, their addresses, and the count of their shipped orders."},
        {"input": "SELECT p.name, AVG(r.rating), p.description FROM products p JOIN reviews r ON p.id = r.product_id GROUP BY p.name, p.description;", "output": "Returns the names of products, their descriptions, and the average rating for each product."},
        {"input": "SELECT c.name, COUNT(pc.product_id), c.description FROM categories c JOIN product_categories pc ON c.id = pc.category_id GROUP BY c.name, c.description;", "output": "Returns the names of categories, their descriptions, and the count of products in each category."},
        {"input": "SELECT u.name, SUM(t.amount), u.phone_number FROM users u JOIN transactions t ON u.id = t.user_id GROUP BY u.name, u.phone_number;", "output": "Returns the names of users, their phone numbers, and the sum of their transaction amounts."},
        {"input": "SELECT p.name, i.quantity, p.category_id FROM products p JOIN inventory i ON p.id = i.product_id WHERE i.quantity < 10;", "output": "Returns the names of products, their category IDs, and their quantities where the quantity is less than 10."},
        {"input": "SELECT u.name, o.product, o.amount, u.email FROM users u JOIN orders o ON u.id = o.user_id WHERE o.order_date > '2022-01-01';", "output": "Returns the names of users, their emails, and the products they ordered where the order date is after January 1, 2022."},
    ],
    "schema": "CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100), email VARCHAR(100), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, last_login TIMESTAMP); CREATE TABLE orders (id INT PRIMARY KEY, user_id INT, product VARCHAR(100), amount DECIMAL(10, 2), order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status VARCHAR(50), shipping_address TEXT, FOREIGN KEY (user_id) REFERENCES users(id)); CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100), description TEXT, price DECIMAL(10, 2), stock INT, category_id INT, FOREIGN KEY (category_id) REFERENCES categories(id)); CREATE TABLE reviews (id INT PRIMARY KEY, user_id INT, product_id INT, rating INT CHECK (rating >= 1 AND rating <= 5), comment TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES products(id)); CREATE TABLE categories (id INT PRIMARY KEY, name VARCHAR(100), description TEXT); CREATE TABLE product_categories (product_id INT, category_id INT, PRIMARY KEY (product_id, category_id), FOREIGN KEY (product_id) REFERENCES products(id), FOREIGN KEY (category_id) REFERENCES categories(id)); CREATE TABLE transactions (id INT PRIMARY KEY, user_id INT, order_id INT, amount DECIMAL(10, 2), transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, status VARCHAR(50), payment_method VARCHAR(50), FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (order_id) REFERENCES orders(id)); CREATE TABLE inventory (id INT PRIMARY KEY, product_id INT, quantity INT, last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (product_id) REFERENCES products(id)); CREATE TABLE suppliers (id INT PRIMARY KEY, name VARCHAR(100), contact_info TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); CREATE TABLE product_suppliers (product_id INT, supplier_id INT, PRIMARY KEY (product_id, supplier_id), FOREIGN KEY (product_id) REFERENCES products(id), FOREIGN KEY (supplier_id) REFERENCES suppliers(id)); CREATE TABLE discounts (id INT PRIMARY KEY, product_id INT, discount_percentage DECIMAL(5, 2), start_date TIMESTAMP, end_date TIMESTAMP, FOREIGN KEY (product_id) REFERENCES products(id)); CREATE TABLE wishlists (id INT PRIMARY KEY, user_id INT, product_id INT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id), FOREIGN KEY (product_id) REFERENCES products(id)); CREATE TABLE notifications (id INT PRIMARY KEY, user_id INT, message TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (user_id) REFERENCES users(id));",
    return response
