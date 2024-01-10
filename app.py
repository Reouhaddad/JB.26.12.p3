import sqlite3
from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # N'oubliez pas de définir une clé secrète pour la session

con = sqlite3.connect("zoo.db",check_same_thread=False)
logged =False
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
             )''')
cur.execute('''CREATE TABLE IF NOT EXISTS animals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age INTEGER,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                picture TEXT NOT NULL
             )''')
@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Insert user data into the database
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        con.commit()
        return redirect(url_for('hello'))
    return render_template("register.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        
        if user:
            logged = True
            flash('Connexion réussie!', 'success')
            return redirect(url_for('get_animals'))
        else:
            flash('Identifiants invalides. Veuillez réessayer.', 'error')
    return render_template("login.html")



# Modify your add route to handle both GET and POST requests
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        age = request.form['age']
        type = request.form['type']
        name = request.form['name']
        picture= request.form['picture']
        # Insert data into the database
        cur.execute("INSERT INTO animals (age, type, name, picture) VALUES (?, ?, ?, ?)", (age, type, name, picture))
        con.commit()
        flash('animal added successfully!')
    return render_template("add.html")


@app.route('/get_animals')
def get_animals():
    global logged  # Ajoutez cette ligne pour indiquer que vous voulez utiliser la variable globale
    
    if not logged:
        return redirect(url_for('login'))
    
    # Le reste de votre code pour récupérer et afficher les animaux

    # Fetch data from the database
    cur.execute("SELECT *,rowid FROM animals")
    animals = cur.fetchall()  # Fetch all rows
    
    # Render the template and pass the retrieved data
    return render_template("animals.html", animals=animals)


@app.route('/delete_animal/<int:animal_id>', methods=['POST'])
def delete_animal(animal_id):
    if request.method == 'POST':
        cur.execute("DELETE FROM animals WHERE rowid=?", (animal_id,))
        con.commit()
        flash('Animal supprimée avec succès!', 'success')
        return redirect(url_for('get_animals'))


if __name__ == '__main__':
    app.run(debug=True)

