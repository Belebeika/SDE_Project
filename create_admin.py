from app import app, db
from Model.models import User

with app.app_context():
    admin = User(
        firstname='admin',
        lastname='user',
        age=30,
        email='ilya885400@mail.ru',
        phone_number='123456789',
        employer_status=True,
        is_admin=True,
        workplace='Admin Workplace',
        post='Admin Post',
        region_id=1
    )

    admin.set_password('admin')

    db.session.add(admin)
    db.session.commit()
    print('Admin user created successfully.')
