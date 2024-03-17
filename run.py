from app import create_app,db

if __name__ == '__main__':
    my_flask_app = create_app('prod')
    with my_flask_app.app_context():
        db.create_all()
    my_flask_app.run()
