from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# -----------------------------
# DATABASE INITIALISATION
# -----------------------------
def init_db():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


# -----------------------------
# HOME ROUTE
# -----------------------------
@app.route('/')
def home():
    return """
    <h1>Product Management System</h1>
    <p>
        <a href="/add">Add Product</a> |
        <a href="/products">View Products</a>
    </p>
    """


# -----------------------------
# ADD PRODUCT ROUTE
# -----------------------------
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']

        if name == "" or price == "":
            return "Please fill in all fields <br><a href='/add'>Go back</a>"

        conn = sqlite3.connect('products.db')
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()

        return """
        <h3>Product added successfully!</h3>
        <a href="/add">Add another</a> |
        <a href="/products">View products</a>
        """

    return """
    <h2>Add Product</h2>
    <form method="POST">
        Product Name: <input type="text" name="name"><br><br>
        Price: <input type="number" step="0.01" name="price"><br><br>
        <button type="submit">Add Product</button>
    </form>
    <br>
    <a href="/">Back Home</a>
    """


# -----------------------------
# VIEW PRODUCTS ROUTE
# -----------------------------
@app.route('/products')
def view_products():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("SELECT * FROM products")
    products = c.fetchall()
    conn.close()

    table = """
    <h2>All Products</h2>
    <table border="1" cellpadding="8">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
        </tr>
    """

    for p in products:
        table += f"""
        <tr>
            <td>{p[0]}</td>
            <td>{p[1]}</td>
            <td>{p[2]}</td>
        </tr>
        """

    table += """
    </table>
    <br>
    <a href="/">Back Home</a> |
    <a href="/add">Add Product</a>
    """

    return table


# -----------------------------
# RUN APP
# -----------------------------
if __name__ == '__main__':
    init_db()
    app.run(debug=True)