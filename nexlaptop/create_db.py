from app import app, db, Brand, CPU, GPU, OS, UseCase, Laptop, Order, OrderDetails

def init_db():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()  # Drop all tables to reset the database
        print("Creating all tables...")
        db.create_all()  # Create all tables


if __name__ == "__main__":
    init_db()
    print("Database initialized with test data.")
