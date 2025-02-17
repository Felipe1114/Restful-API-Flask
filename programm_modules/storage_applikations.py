import json

class StorageApplications:
    def __init__(self, filename="../programm_storage/books.json"):
        self.filename = filename
        self._ensure_file_exists()

        print(f"StorageApplication was initialated as {self}")


    def _ensure_file_exists(self):
        """Checks, if file exists, if not, creates new file"""
        try:
            with open(self.filename, "r") as file:
                json.load(file)

            print(f"Json file {self.filename}, existss")

        except (FileNotFoundError, json.JSONDecodeError):
            with open(self.filename, "w") as file:
                json.dump([], file)
            print(f"Json file {self.filename} does not exists... Json was created as {self.filename}")


    def load_books(self):
        """Loads books form storage."""
        with open(self.filename, "r") as file:
            return json.load(file)

    def save_books(self, books):
        """Saves books to storage"""
        with open(self.filename, "w") as file:
            json.dump(books, file, indent=4)

    def get_all_books(self):
        """returns all books"""
        return self.load_books()

    def get_book_by_id(self, book_id):
        """returns spezific book, by its id"""
        books = self.load_books()
        return next((book for book in books if book["id"] == book_id), None)

    def add_book(self, title, author):
        """Adds a book to storage"""
        books = self.load_books()
        new_id = books[-1]["id"] + 1 if books else 1
        new_book = {"id": new_id, "title": title, "author": author}
        books.append(new_book)
        self.save_books(books)
        return new_book

    def update_book(self, book_id, title=None, author=None):
        """Updates books"""
        books = self.load_books()
        for book in books:
            if book["id"] == book_id:
                if title:
                    book["title"] = title
                if author:
                    book["author"] = author
                self.save_books(books)
                return book
        return None

    def delete_book(self, book_id):
        """Deletes books"""
        books = self.load_books()
        books = [book for book in books if book["id"] != book_id]
        self.save_books(books)
        return True
