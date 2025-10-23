from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/flask_forms1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    year_published = db.Column(db.Integer, nullable=True)

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('list_books.html', books=books)

@app.route("/add-book", methods=["GET", "POST"])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        year_published = request.form['year_published']
        
        if not title or not author or not price or not year_published:
            flash('Make sure all parameters are met', 'error')
            return redirect(url_for('add_book'))
        
        try:
            new_book = Book(title=title, author=author, price=price, year_published=year_published)
            db.session.add(new_book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('list_books'))
        except Exception as e:
            flash(f'Error in adding the book: {str(e)}', 'error')
            return redirect(url_for('add_book'))
        
    return render_template('add_book.html')

@app.route("/update-book/<int:id>", methods=["GET", "POST"])
def update_book(id):
    book = Book.query.get_or_404(id)
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        price = request.form['price']
        year_published = request.form['year_published']

        if not title or not author or not price or not year_published:
            flash('Make sure all parameters are met', 'error')
            return redirect(url_for('update_book', id=id))
        
        try:
            book.title = title
            book.author = author
            book.price = price
            book.year_published = year_published
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('list_books'))
        except Exception as e:
            flash(f'Error updating your book: {str(e)}', 'error')
            return redirect(url_for('update_book', id=id))            
            
    return render_template("update_book.html", book=book)

@app.route("/delete-book/<int:id>")
def delete_book(id):
    book = Book.query.get_or_404(id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error with deleting book: {str(e)}', 'error')
    return redirect(url_for('get_books'))

@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return render_template("list_books.html", books=books)

if __name__ == '__main__':
    app.run(debug=True)
    app.run()