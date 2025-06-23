from server.app import create_app, db
from server.models.user import User
from server.models.guest import Guest
from server.models.episode import Episode
from server.models.appearance import Appearance
from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create users
    user = User(username='admin')
    user.set_password('password')
    db.session.add(user)

    # Create guests
    guest1 = Guest(name='Tom Hanks', occupation='Actor')
    guest2 = Guest(name='Taylor Swift', occupation='Singer')
    db.session.add_all([guest1, guest2])

    # Create episodes
    episode1 = Episode(date=date(2023, 1, 1), number=1)
    episode2 = Episode(date=date(2023, 1, 2), number=2)
    db.session.add_all([episode1, episode2])

    db.session.commit()

    # Create appearances
    appearance1 = Appearance(rating=5, guest_id=guest1.id, episode_id=episode1.id)
    appearance2 = Appearance(rating=4, guest_id=guest2.id, episode_id=episode1.id)
    appearance3 = Appearance(rating=3, guest_id=guest1.id, episode_id=episode2.id)
    db.session.add_all([appearance1, appearance2, appearance3])

    db.session.commit()
    print('Database seeded!') 