from flask import Flask, render_template, request, redirect, url_for, jsonify
import csv
import os

app = Flask(__name__)

CSV_FILE = "inventory.csv"

# Initialize CSV file if not exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Product ID", "Product Name", "Category", "Price", "Stock", "Total Sales"])

# Read inventory data
def read_inventory():
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

# Write data to CSV
def write_inventory(data):
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Product ID", "Product Name", "Category", "Price", "Stock", "Total Sales"])
        writer.writerows(data)

# Home Page
@app.route('/')
def index():
    return render_template('index.html')

# View Products
@app.route('/products')
def view_products():
    products = read_inventory()
    return render_template('view_products.html', products=products)

# Add Product
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_id = request.form['product_id']
        name = request.form['name']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']

        data = read_inventory()
        data.append([product_id, name, category, price, stock, 0])
        write_inventory(data)

        return redirect(url_for('view_products'))
    return render_template('add_product.html')

# Delete Product
@app.route('/delete_product/<product_id>')
def delete_product(product_id):
    data = read_inventory()
    new_data = [row for row in data if row["Product ID"] != product_id]
    write_inventory(new_data)
    return redirect(url_for('view_products'))

# Update Stock (Record Sale)
@app.route('/update_stock/<product_id>', methods=['POST'])
def update_stock(product_id):
    data = read_inventory()
    for row in data:
        if row["Product ID"] == product_id and int(row["Stock"]) > 0:
            row["Stock"] = str(int(row["Stock"]) - 1)
            row["Total Sales"] = str(int(row["Total Sales"]) + 1)
            break
    write_inventory([list(row.values()) for row in data])
    return jsonify({"message": "Stock updated successfully"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
