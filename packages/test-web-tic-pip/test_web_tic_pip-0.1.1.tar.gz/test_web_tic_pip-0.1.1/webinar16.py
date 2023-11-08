import json
class Book:
    def __init__(self, title="", author="") -> None:
        self.title = title
        self.author = author


    def to_dict(self):
        return self.__dict__
        # return {"title": self.title, "author": self.author}
    

    @classmethod
    def to_object(cls, book_data):
        book = Book()
        for key in book_data:
            print(hasattr(book, key))
            if hasattr(book, key):
                setattr(book, key, book_data[key])
        return book

        # return cls(title=book_data.get("title"), author=book_data.get("author"))
