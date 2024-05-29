from nexlaptop import create_app
from nexlaptop.models import db, Brand, CPU, GPU, OS, UseCase, Laptop

app = create_app()

with app.app_context():
    db.create_all()

    brand_data = [
        Brand(id=1, name='Lenovo'),
        Brand(id=2, name='Apple'),
        Brand(id=3, name='LG'),
        Brand(id=4, name='MSI')
    ]

    cpu_data = [
        CPU(id=1, name='Intel® Core™ Ultra 5 125U'),
        CPU(id=2, name='Intel® Core™ i7-14700HX'),
        CPU(id=3, name='Intel® Core™ i5-13500H'),
        CPU(id=4, name='Apple M3'),
        CPU(id=5, name='Apple M2')
    ]

    gpu_data = [
        GPU(id=1, name='Integrated Intel Arc™Graphics'),
        GPU(id=2, name='NVIDIA® GeForce RTX™ 4070'),
        GPU(id=3, name='Integrated Intel Iris® Xe Graphics'),
        GPU(id=4, name='Apple M3'),
        GPU(id=5, name='Apple M2')
    ]

    os_data = [
        OS(id=1, name='Windows 11'),
        OS(id=2, name='MacOS')
    ]

    usecase_data = [
        UseCase(id=1, name='Home', description='Light office tasks, media consumption, portability'),
        UseCase(id=2, name='Gaming', description='Powerful hardware for gaming or professional applications'),
        UseCase(id=3, name='Business', description='Security, durability, and stability for your business')
    ]

    laptop_data = [
        Laptop(id=1, price=2484.46, brand_id=1, model='ThinkPad X1 Carbon Gen 12', screensize=14.0, cpu_id=1, gpu_id=1, memory=32, storage=2000, os_id=1, usecase_id=3),
        Laptop(id=2, price=2919.0, brand_id=1, model='Legion Pro 5i Gen 9', screensize=16.0, cpu_id=2, gpu_id=2, memory=32, storage=1000, os_id=1, usecase_id=2),
        Laptop(id=3, price=1599.99, brand_id=1, model='Yoga Slim 6i Gen 8', screensize=14.0, cpu_id=3, gpu_id=3, memory=16, storage=512, os_id=1, usecase_id=1),
        Laptop(id=4, price=2729.0, brand_id=2, model='MacBook Pro', screensize=14.2, cpu_id=4, gpu_id=4, memory=8, storage=1000, os_id=2, usecase_id=1),
        Laptop(id=5, price=1498.5, brand_id=2, model='MacBook Air', screensize=13.6, cpu_id=5, gpu_id=5, memory=8, storage=256, os_id=2, usecase_id=1),
        Laptop(id=6, price=1999.99, brand_id=3, model='LG Gram', screensize=17.0, cpu_id=1, gpu_id=1, memory=16, storage=512, os_id=1, usecase_id=1),
        Laptop(id=7, price=1299.0, brand_id=4, model='Prestige 14 Evo', screensize=14.0, cpu_id=3, gpu_id=3, memory=16, storage=512, os_id=1, usecase_id=3)
    ]

    db.session.add_all(brand_data)
    db.session.add_all(cpu_data)
    db.session.add_all(gpu_data)
    db.session.add_all(os_data)
    db.session.add_all(usecase_data)
    db.session.add_all(laptop_data)

    db.session.commit()

    print("Database initialised with initial data")
