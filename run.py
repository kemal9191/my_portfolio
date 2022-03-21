from app import create_app, db

app = create_app()
db.create_all(app=app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)