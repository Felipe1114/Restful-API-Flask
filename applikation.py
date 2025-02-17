from flask import Flask, jsonify, request
from programm_modules.storage_applikations import StorageApplications
import logging

app = Flask(__name__)
book_storage = StorageApplications()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def paginate(data, page, limit):
    start = int((page - 1) * limit)
    end = int(start + limit)

    if start >= len(data):
      return []

    return data[start:end]


@app.route('/api/books', methods=['GET'])
def get_books():
    app.logger.info("GET request recieved for /api/books")


    page = int(request.args.get('page', default=1, type=int))
    limit = int(request.args.get('limit', default=10, type=int))
    books = list(book_storage.get_all_books())

    paginated_books = paginate(books, page, limit)


    return jsonify(paginated_books)


@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    app.logger.info(f"GET request recieved for /api/books/{book_id}")

    book = book_storage.get_book_by_id(book_id)
    return jsonify(book) if book else (jsonify({"error": "Book not found"}), 404)

@app.route('/api/books/search', methods=['GET'])
def get_books_by_author():

    author = request.args.get('author')

    app.logger.info(f"GET request recieved for /api/books/search?author={author}")

    page = request.args.get('page', default=1, type=int)
    limit = request.args.get('limit', default=10, type=int)
    books = book_storage.get_all_books()

    if not author:

        return jsonify({"error": "Author query parameter is required"}), 400

    matching_books = [book for book in books if book["author"].lower() == author.lower()]

    if not matching_books:

        return jsonify({"message": "No books found for this author"}), 404

    paginated_books = paginate(matching_books, page, limit)

    return jsonify(paginated_books)


@app.route('/api/books', methods=['POST'])
def add_book():
    app.logger.info("POST request recieved for /api/books")

    data = request.get_json()

    if not data or "title" not in data or "author" not in data:

        return jsonify({"error": "Missing title or author"}), 400

    new_book = book_storage.add_book(data["title"], data["author"])

    return jsonify(new_book), 201


@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    app.logger.info(f"PUT request recieved for /api/books/{book_id}")

    data = request.get_json()

    if not data:

        return jsonify({"error": "No data provided"}), 400

    updated_book = book_storage.update_book(book_id, data.get("title"), data.get("author"))

    return jsonify(updated_book) if updated_book else (jsonify({"error": "Book not found"}), 404)


@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    app.logger.info(f"DELETE request recieved for /api/books{book_id}")

    if book_storage.delete_book(book_id):

        return jsonify({"message": "Book deleted"}), 200

    return jsonify({"error": "Book not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)



