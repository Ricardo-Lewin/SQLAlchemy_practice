from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet."""

    __tablename__ = "pets"

    @classmethod
    def get_by_species(cls, species):
        """Get all pets matching that color."""

        return cls.query.filter_by(species=species).all()

    def __repr__(self):
        """Show info about pet."""

        p = self
        return f"<Pet id = {p.id} name = {p.name} species = {p.species} hunger = {p.hunger}>"

    def greet(self):
        """Greet using name."""

        return f"I'm {self.name} the {self.species or 'thing'}"

    def feed(self, units=10):
        """Update hunger value"""

        self.hunger -= units
        self.hunger = max(self.hunger, 0)

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)

    species = db.Column(db.String(30), nullable=True)

    hunger = db.Column(db.Integer, nullable=False, default=20)
