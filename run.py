from app import create_app, db

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    with app.app_context():
        db.create_all()  # Creates tables if not using Alembic
    app.run(debug=True)