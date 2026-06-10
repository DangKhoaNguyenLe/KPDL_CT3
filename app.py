from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json
import requests

app = Flask(__name__)
app.secret_key = 'tour_secret_key_2024'

# ============================================================
# API HELPERS
# ============================================================
BACKEND_URL = "http://localhost:8000/api"

def fetch_tours():
    try:
        response = requests.get(f"{BACKEND_URL}/tours")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching tours: {e}")
    return []

def fetch_tour(tour_id):
    try:
        response = requests.get(f"{BACKEND_URL}/tours/{tour_id}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching tour: {e}")
    return None

# ============================================================
# HÀM TIỆN ÍCH
# ============================================================
def get_cart():
    return session.get('cart', {})

def get_cart_count():
    cart = get_cart()
    return sum(item['quantity'] for item in cart.values())

def get_cart_total():
    cart = get_cart()
    total = 0
    tours = fetch_tours()
    for item in cart.values():
        tour = next((t for t in tours if t['id'] == item['tour_id']), None)
        if tour:
            total += tour['price'] * item['quantity']
    return total

def format_price(price):
    return f"{price:,.0f}".replace(',', '.')

app.jinja_env.filters['format_price'] = format_price

# ============================================================
# ROUTES
# ============================================================

# TRANG CHỦ
@app.route('/')
def index():
    tours = fetch_tours()
    featured_tours = tours[:3] if tours else []
    cart_count = get_cart_count()
    return render_template('index.html',
                           featured_tours=featured_tours,
                           cart_count=cart_count)

# DANH SÁCH TOUR
@app.route('/tours')
def tours():
    category = request.args.get('category', 'all')
    sort_by = request.args.get('sort', 'default')
    search = request.args.get('search', '').lower()

    all_tours = fetch_tours()
    filtered = all_tours.copy()

    # Lọc theo danh mục
    if category != 'all':
        filtered = [t for t in filtered if t['category'] == category]

    # Tìm kiếm
    if search:
        filtered = [t for t in filtered if
                    search in t['name'].lower() or
                    search in t['destination'].lower()]

    # Sắp xếp
    if sort_by == 'price_asc':
        filtered.sort(key=lambda x: x['price'])
    elif sort_by == 'price_desc':
        filtered.sort(key=lambda x: x['price'], reverse=True)
    elif sort_by == 'rating':
        filtered.sort(key=lambda x: x['rating'], reverse=True)

    cart_count = get_cart_count()
    return render_template('tours.html',
                           tours=filtered,
                           category=category,
                           sort_by=sort_by,
                           search=search,
                           cart_count=cart_count)

# CHI TIẾT TOUR
@app.route('/tour/<int:tour_id>')
def tour_detail(tour_id):
    tour = fetch_tour(tour_id)
    if not tour:
        return redirect(url_for('tours'))
    cart_count = get_cart_count()
    return render_template('tour_detail.html', tour=tour, cart_count=cart_count)

# GIỎ HÀNG
@app.route('/cart')
def cart():
    cart = get_cart()
    cart_items = []
    tours = fetch_tours()
    for key, item in cart.items():
        tour = next((t for t in tours if t['id'] == item['tour_id']), None)
        if tour:
            cart_items.append({
                'key': key,
                'tour': tour,
                'quantity': item['quantity'],
                'date': item.get('date', ''),
                'guests': item.get('guests', 1),
                'subtotal': tour['price'] * item['quantity']
            })
    total = sum(i['subtotal'] for i in cart_items)
    cart_count = get_cart_count()
    return render_template('cart.html',
                           cart_items=cart_items,
                           total=total,
                           cart_count=cart_count)

# THÊM VÀO GIỎ HÀNG
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    tour_id = int(request.form.get('tour_id'))
    quantity = int(request.form.get('quantity', 1))
    date = request.form.get('date', '')
    guests = int(request.form.get('guests', 1))

    cart = get_cart()
    key = f"{tour_id}_{date}"

    if key in cart:
        cart[key]['quantity'] += quantity
    else:
        cart[key] = {
            'tour_id': tour_id,
            'quantity': quantity,
            'date': date,
            'guests': guests
        }

    session['cart'] = cart
    return redirect(url_for('cart'))

# XÓA KHỎI GIỎ HÀNG
@app.route('/remove_from_cart/<key>')
def remove_from_cart(key):
    cart = get_cart()
    if key in cart:
        del cart[key]
    session['cart'] = cart
    return redirect(url_for('cart'))

# CẬP NHẬT SỐ LƯỢNG
@app.route('/update_cart', methods=['POST'])
def update_cart():
    key = request.form.get('key')
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    if key in cart:
        if quantity <= 0:
            del cart[key]
        else:
            cart[key]['quantity'] = quantity
    session['cart'] = cart
    return redirect(url_for('cart'))

# THANH TOÁN (demo)
@app.route('/checkout', methods=['POST'])
def checkout():
    session['cart'] = {}
    return render_template('checkout_success.html')

# API lấy số lượng giỏ hàng
@app.route('/api/cart_count')
def api_cart_count():
    return jsonify({'count': get_cart_count()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
