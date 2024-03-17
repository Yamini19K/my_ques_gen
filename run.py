from app import create_app, db
from app.auth.models import User

my_flask_app = create_app('prod')
with my_flask_app.app_context():
    db.create_all()
    if not User.query.filter_by(user_admin='Yamini').first():
        User.create_user(user='Yamini', password='12345', email='yamini19kumar@gmail.com')
        my_flask_app.run()
