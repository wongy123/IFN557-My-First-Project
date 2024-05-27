from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, current_app
from models import db, Laptop, Brand, CPU, GPU, OS, UseCase, Order, OrderDetails
import os

main_bp = Blueprint('main', __name__)

def get_image_paths(app, product_id):
    base_path = os.path.join(app.static_folder, 'img', 'product', str(product_id))
    image_paths = []
    for i in range(1, 6):
        image_path = os.path.join(base_path, f'{i}.jpeg')
        if os.path.exists(image_path):
            image_paths.append(f'img/product/{product_id}/{i}.jpeg')
    return image_paths

@main_bp.route("/")
def index():
    usecases = UseCase.query.all()
    laptops = Laptop.query.filter(Laptop.id.in_([2, 4, 7])).all()
    return render_template("index.html", usecases=usecases, laptops = laptops)

@main_bp.route("/products")
def products():
    brands = Brand.query.all()
    cpus = CPU.query.all()
    gpus = GPU.query.all()
    oses = OS.query.all()
    usecases = UseCase.query.all()

    brand_filter = request.args.getlist('brand')
    cpu_filter = request.args.getlist('cpu')
    gpu_filter = request.args.getlist('gpu')
    os_filter = request.args.getlist('os')
    usecase_filter = request.args.getlist('usecase')

    query = Laptop.query

    if brand_filter:
        query = query.filter(Laptop.brand_id.in_(brand_filter))
    if cpu_filter:
        query = query.filter(Laptop.cpu_id.in_(cpu_filter))
    if gpu_filter:
        query = query.filter(Laptop.gpu_id.in_(gpu_filter))
    if os_filter:
        query = query.filter(Laptop.os_id.in_(os_filter))
    if usecase_filter:
        query = query.filter(Laptop.usecase_id.in_(usecase_filter))

    laptops = query.all()

    return render_template("products.html", laptops=laptops, brands=brands, cpus=cpus, gpus=gpus, oses=oses, usecases=usecases, 
                           brand_filter=brand_filter, cpu_filter=cpu_filter, gpu_filter=gpu_filter, os_filter=os_filter, 
                           usecase_filter=usecase_filter)

@main_bp.route("/product/<int:productid>")
def viewProduct(productid):
    product = db.session.get(Laptop, productid)
    
    if not product:
        print(f"No product found with ID {productid}")
        abort(404)  # Return a 404 error if the product is not found
    
    image_paths = get_image_paths(current_app, productid)
    
    return render_template("product.html", product=product, image_paths=image_paths)

@main_bp.route('/cart')
def view_cart():
    cart = session.get('cart', {})
    products = []
    total_price = 0
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = db.session.get(Laptop, product_id)
        products.append({'product': product, 'quantity': quantity, 'subtotal': product.price * quantity})
        total_price += product.price * quantity
    return render_template('cart.html', products=products, total_price=total_price)

@main_bp.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', '1'))
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity

    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('main.view_cart'))


@main_bp.route('/update_cart/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    cart = session.get('cart', {})
    quantity_str = request.form.get('quantity', '1')
    
    try:
        quantity = int(quantity_str)
    except ValueError:  
        flash('Invalid quantity. Please enter a valid number.', 'danger')
        return redirect(url_for('main.view_cart'))

    product_id_str = str(product_id)
    if quantity <= 0:
        cart.pop(product_id_str, None)
    else:
        cart[product_id_str] = quantity
    session['cart'] = cart
    flash('Cart updated!', 'success')
    return redirect(url_for('main.view_cart'))

@main_bp.route('/remove_from_cart/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    cart.pop(product_id_str, None)
    session['cart'] = cart
    flash('Product removed from cart!', 'success')
    return redirect(url_for('main.view_cart'))

@main_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        cart = session.get('cart', {})
        
        total_cost = 0
        for product_id_str, quantity in cart.items():
            product_id = int(product_id_str)
            product = db.session.get(Laptop, product_id)
            total_cost += product.price * quantity
        
        new_order = Order(
            first_name=first_name,
            last_name=last_name,
            address=address,
            email=email,
            phone=phone,
            total_cost=total_cost
        )
        
        db.session.add(new_order)
        db.session.commit()

        for product_id_str, quantity in cart.items():
            product_id = int(product_id_str)
            order_detail = OrderDetails(order_id=new_order.id, laptop_id=product_id, quantity=quantity)
            db.session.add(order_detail)
        db.session.commit()

        session.pop('cart', None)
        flash('Order submitted successfully!', 'success')
        return redirect(url_for('main.order_confirmation', order_id=new_order.id))
    return render_template('checkout.html')

@main_bp.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = db.session.get(Order, order_id)
    order_details = OrderDetails.query.filter_by(order_id=order_id).all()
    products = []
    total_price = 0
    for detail in order_details:
        product = db.session.get(Laptop, detail.laptop_id)
        subtotal = product.price * detail.quantity
        total_price += subtotal
        products.append({'product': product, 'quantity': detail.quantity, 'subtotal': subtotal})
    return render_template('order_confirmation.html', order=order, products=products, total_price=total_price)

@main_bp.route('/view_order', methods=['GET', 'POST'])
def view_order():
    if request.method == 'POST':
        order_id = request.form['order_id']
        return redirect(url_for('main.order_details', order_id=order_id))
    return render_template('view_order.html')

@main_bp.route('/order_details/<int:order_id>')
def order_details(order_id):
    order = db.session.get(Order, order_id)
    order_details = OrderDetails.query.filter_by(order_id=order_id).all()
    products = []
    total_price = 0
    for detail in order_details:
        product = db.session.get(Laptop, detail.laptop_id)
        subtotal = product.price * detail.quantity
        total_price += subtotal
        products.append({'product': product, 'quantity': detail.quantity, 'subtotal': subtotal})
    return render_template('order_details.html', order=order, products=products, total_price=total_price)
