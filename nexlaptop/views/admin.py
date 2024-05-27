from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Laptop, Brand, CPU, GPU, OS, UseCase

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/", methods=["GET", "POST"])
def admin():
    brands = Brand.query.all()
    cpus = CPU.query.all()
    gpus = GPU.query.all()
    oses = OS.query.all()
    usecases = UseCase.query.all()
    laptops = Laptop.query.all()
    return render_template("admin.html", brands=brands, cpus=cpus, gpus=gpus, oses=oses, usecases=usecases, laptops=laptops)

@admin_bp.route("/add_product", methods=["POST"])
def add_product():
    try:
        brand_id = request.form['brand_id']
        model = request.form['model']
        screensize = request.form['screensize']
        cpu_id = request.form['cpu_id']
        gpu_id = request.form['gpu_id']
        memory = request.form['memory']
        storage = request.form['storage']
        os_id = request.form['os_id']
        usecase_id = request.form['usecase_id']
        price = request.form['price']
        
        new_product = Laptop(
            brand_id=brand_id,
            model=model,
            screensize=screensize,
            cpu_id=cpu_id,
            gpu_id=gpu_id,
            memory=memory,
            storage=storage,
            os_id=os_id,
            usecase_id=usecase_id,
            price=price
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding product: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/remove_product", methods=["POST"])
def remove_product():
    try:
        product_id = request.form['product_id']
        product = db.session.get(Laptop, product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            flash('Product removed successfully!', 'success')
        else:
            flash('Product not found!', 'danger')
    except Exception as e:
        flash(f'Error removing product: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/add_brand", methods=["POST"])
def add_brand():
    try:
        name = request.form['brand_name']
        new_brand = Brand(name=name)
        db.session.add(new_brand)
        db.session.commit()
        flash('Brand added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding brand: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/remove_brand", methods=["POST"])
def remove_brand():
    try:
        brand_id = request.form['brand_id']
        brand = db.session.get(Brand, brand_id)
        if brand:
            db.session.delete(brand)
            db.session.commit()
            flash('Brand removed successfully!', 'success')
        else:
            flash('Brand not found!', 'danger')
    except Exception as e:
        flash(f'Error removing brand: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/add_cpu", methods=["POST"])
def add_cpu():
    try:
        name = request.form['cpu_name']
        new_cpu = CPU(name=name)
        db.session.add(new_cpu)
        db.session.commit()
        flash('CPU added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding CPU: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/remove_cpu", methods=["POST"])
def remove_cpu():
    try:
        cpu_id = request.form['cpu_id']
        cpu = db.session.get(CPU, cpu_id)
        if cpu:
            db.session.delete(cpu)
            db.session.commit()
            flash('CPU removed successfully!', 'success')
        else:
            flash('CPU not found!', 'danger')
    except Exception as e:
        flash(f'Error removing CPU: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/add_gpu", methods=["POST"])
def add_gpu():
    try:
        name = request.form['gpu_name']
        new_gpu = GPU(name=name)
        db.session.add(new_gpu)
        db.session.commit()
        flash('GPU added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding GPU: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/remove_gpu", methods=["POST"])
def remove_gpu():
    try:
        gpu_id = request.form['gpu_id']
        gpu = db.session.get(GPU, gpu_id)
        if gpu:
            db.session.delete(gpu)
            db.session.commit()
            flash('GPU removed successfully!', 'success')
        else:
            flash('GPU not found!', 'danger')
    except Exception as e:
        flash(f'Error removing GPU: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/add_os", methods=["POST"])
def add_os():
    try:
        name = request.form['os_name']
        new_os = OS(name=name)
        db.session.add(new_os)
        db.session.commit()
        flash('OS added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding OS: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/remove_os", methods=["POST"])
def remove_os():
    try:
        os_id = request.form['os_id']
        os = db.session.get(OS, os_id)
        if os:
            db.session.delete(os)
            db.session.commit()
            flash('OS removed successfully!', 'success')
        else:
            flash('OS not found!', 'danger')
    except Exception as e:
        flash(f'Error removing OS: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/add_usecase", methods=["POST"])
def add_usecase():
    try:
        name = request.form['usecase_name']
        description = request.form['description']
        new_usecase = UseCase(name=name, description=description)
        db.session.add(new_usecase)
        db.session.commit()
        flash('Use Case added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding Use Case: {e}', 'danger')
    return redirect(url_for('admin.admin'))

@admin_bp.route("/remove_usecase", methods=["POST"])
def remove_usecase():
    try:
        usecase_id = request.form['usecase_id']
        usecase = db.session.get(UseCase, usecase_id)
        if usecase:
            db.session.delete(usecase)
            db.session.commit()
            flash('Use Case removed successfully!', 'success')
        else:
            flash('Use Case not found!', 'danger')
    except Exception as e:
        flash(f'Error removing Use Case: {e}', 'danger')
    return redirect(url_for('admin.admin'))
