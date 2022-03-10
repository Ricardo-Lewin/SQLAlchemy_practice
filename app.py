from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_shop_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "apple"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def show_pets():
    """Show All Pets"""
    pets = Pet.query.all()
    return render_template('list.html', pets=pets)


@app.route('/', methods=["POST"])
def add_pet():
    """Submits Form Data and adds to database"""
    name = request.form['name']
    species = request.form['species']
    hunger = request.form['hunger']
    hunger = int(hunger) if hunger else None

    pet = Pet(name=name, species=species, hunger=hunger)
    db.session.add(pet)
    db.session.commit()
    return redirect(f'/{pet.id}')


@app.route('/<int:pet_id>')
def show_details(pet_id):
    """Show pet details"""
    pet = Pet.query.get_or_404(pet_id)
    return render_template('details.html', pet=pet)


@app.route('/species/<species_id>')
def show_pets_by_species(species_id):
    """Show pets by species"""
    pets = Pet.get_by_species(species_id)
    return render_template('species.html', pets=pets, species=species_id)
