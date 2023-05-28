from faker import Faker
from blog.models import Entry
from . import db


def generate_entries(how_many=50):
    fake = Faker()

    if Entry.query.count() == 0:
        for i in range(how_many):
            post = Entry(
                title=fake.sentence(),
                body='\n'.join(fake.paragraphs(15)),
                is_published=True
            )
            db.session.add(post)
        db.session.commit()