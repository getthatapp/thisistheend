from faker import Faker
from blog.models import Entry, User
from . import db


def generate_entries(user_id, how_many=50):
    fake = Faker()

    user = User.query.get(user_id)
    if user:
        for i in range(how_many):
            post = Entry(
                title=fake.sentence(),
                body='\n'.join(fake.paragraphs(15)),
                is_published=True,
                author=user
            )
            db.session.add(post)
        db.session.commit()
    else:
        print("User not found")
