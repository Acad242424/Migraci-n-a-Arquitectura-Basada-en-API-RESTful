from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    db_url = os.getenv('DATABASE_URL', 'sqlite:///books.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/books', methods=['GET'])
    def list_books():
        books = Book.query.all()
        return jsonify([b.to_dict() for b in books]), 200

    @app.route('/books/<int:book_id>', methods=['GET'])
    def get_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error':'Not found'}), 404
        return jsonify(book.to_dict()), 200

    @app.route('/books', methods=['POST'])
    def create_book():
        data = request.get_json() or {}
        title = data.get('title')
        author = data.get('author')
        if not title:
            return jsonify({'error':'title is required'}), 400
        book = Book(title=title, author=author)
        db.session.add(book)
        db.session.commit()
        return jsonify(book.to_dict()), 201

    @app.route('/books/<int:book_id>', methods=['PUT'])
    def update_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error':'Not found'}), 404
        data = request.get_json() or {}
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        db.session.commit()
        return jsonify(book.to_dict()), 200

    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error':'Not found'}), 404
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message':'deleted'}), 200

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status':'ok'}), 200

    return app

db = SQLAlchemy()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'author': self.author}

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host=os.getenv('API_HOST','0.0.0.0'), port=int(os.getenv('API_PORT',5001)))
