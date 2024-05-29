from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from .models import db, Laptop, Brand, CPU, GPU, OS, UseCase, Order, OrderDetails, ContactForm as ContactFormModel
from .forms import ContactForm, CheckoutForm, ViewOrderForm
import os
import random

main_bp = Blueprint('main', __name__)

def getImagePaths(app, product_id):
    base_path = os.path.join(current_app.static_folder, 'img', 'product', str(product_id))
    image_paths = []
    for i in range(1, 6):
        image_path = os.path.join(base_path, f'{i}.jpeg')
        if os.path.exists(image_path):
            image_paths.append(f'img/product/{product_id}/{i}.jpeg')
    return image_paths

def calculateTotalCost(cart):
    total_cost = 0
    for product_id_str, quantity in cart.items():
        product_id = int(product_id_str)
        product = db.session.get(Laptop, product_id)
        total_cost += product.price * quantity
    return total_cost

def generateOrderId():
    while True:
        order_id = random.randint(100000, 999999)
        existing_order = Order.query.get(order_id)
        if not existing_order:
            return order_id

@main_bp.route("/")
def index():
    usecases = UseCase.query.all()
    laptops = Laptop.query.filter(Laptop.id.in_([2, 4, 7])).all()
    return render_template("index.html", usecases=usecases, laptops=laptops)

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
    
    image_paths = getImagePaths(current_app, productid)
    
    return render_template("product.html", product=product, image_paths=image_paths)

@main_bp.route('/cart')
def viewCart():
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
def addToCart(product_id):
    cart = session.get('cart', {})
    quantity = int(request.form.get('quantity', '1'))
    
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity

    session['cart'] = cart
    return redirect(url_for('main.viewCart'))

@main_bp.route('/update_cart/<int:product_id>', methods=['POST'])
def updateCart(product_id):
    cart = session.get('cart', {})
    quantity_str = request.form.get('quantity', '1')
    
    try:
        quantity = int(quantity_str)
    except ValueError:  
        return redirect(url_for('main.viewCart'))

    product_id_str = str(product_id)
    if quantity <= 0:
        cart.pop(product_id_str, None)
    else:
        cart[product_id_str] = quantity
    session['cart'] = cart
    return redirect(url_for('main.viewCart'))

@main_bp.route('/remove_from_cart/<int:product_id>')
def removeFromCart(product_id):
    cart = session.get('cart', {})
    product_id_str = str(product_id)
    cart.pop(product_id_str, None)
    session['cart'] = cart
    return redirect(url_for('main.viewCart'))

@main_bp.route('/checkout', methods=['GET'])
def checkout():
    form = CheckoutForm()
    return render_template('checkout.html', form=form)

@main_bp.route('/checkout', methods=['POST'])
def submitOrder():
    form = CheckoutForm()
    if form.validate_on_submit():
        order_id = generateOrderId()
        new_order = Order(
            id=order_id,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            address=form.address.data,
            email=form.email.data,
            phone=form.phone.data,
            total_cost=calculateTotalCost(session.get('cart', {}))
        )
        
        db.session.add(new_order)
        db.session.commit()

        for product_id_str, quantity in session.get('cart', {}).items():
            product_id = int(product_id_str)
            order_detail = OrderDetails(order_id=new_order.id, laptop_id=product_id, quantity=quantity)
            db.session.add(order_detail)
        db.session.commit()

        session.pop('cart', None)
        return redirect(url_for('main.orderConfirmation', order_id=new_order.id))
    return render_template('checkout.html', form=form)

@main_bp.route('/order_confirmation/<int:order_id>')
def orderConfirmation(order_id):
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

@main_bp.route('/view_order', methods=['GET'])
def viewOrderGet():
    form = ViewOrderForm()
    return render_template('view_order.html', form=form)

@main_bp.route('/view_order', methods=['POST'])
def viewOrder():
    form = ViewOrderForm()
    if form.validate_on_submit():
        order_id = form.order_id.data
        order = db.session.get(Order, order_id)
        if order:
            return redirect(url_for('main.orderDetails', order_id=order_id))
        else:
            return render_template('order_not_found.html', order_id=order_id)
    return render_template('view_order.html', form=form)

@main_bp.route('/order_details/<int:order_id>')
def orderDetails(order_id):
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

@main_bp.route('/contact', methods=['GET'])
def displayContactForm():
    form = ContactForm()
    return render_template('contact_form.html', form=form)

@main_bp.route('/contact', methods=['POST'])
def submitContactForm():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact_form = ContactFormModel(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            phone=form.phone.data,
            email=form.email.data,
            order_number=form.order_number.data,
            question=form.question.data
        )
        
        db.session.add(new_contact_form)
        db.session.commit()
        return render_template('form_submitted.html')
    
    return render_template('contact_form.html', form=form)
