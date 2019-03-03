import itertools

from tests.conftest import Author, Book, SAMPLE_SIZE


def test_add__remove_many_books(orm):
    author = Author()
    book_list = list()
    for _ in range(SAMPLE_SIZE):
        book = Book()
        book_list.append(book)
        orm.add(book, author)

    author_books = orm.get_relation(author.books)
    assert all([book in author_books for book in book_list])
    assert all([author in orm.get_relation(book.authors) for book in book_list])

    assert len(orm.get_type(Author)) == 1
    assert len(orm.get_type(Book)) == SAMPLE_SIZE

    for book in book_list:
        orm.remove(book, author)

    author_books = orm.get_relation(author.books)
    assert all(book not in author_books for book in book_list)
    assert len(orm.get_relation(author.books)) == 0

    objects_len = sum(len(orm.get_type(x)) for x in [Book, Author])
    assert objects_len == 0


def test_add__remove_many_authors(orm):
    book = Book()
    author_list = list()
    for _ in range(SAMPLE_SIZE):
        author = Author()
        author_list.append(author)
        orm.add(author, book)

    book_authors = orm.get_relation(book.authors)
    assert all([author in book_authors for author in author_list])
    assert all([book in orm.get_relation(author.books) for author in author_list])

    assert len(orm.get_type(Book)) == 1
    assert len(orm.get_type(Author)) == SAMPLE_SIZE

    for author in author_list:
        orm.remove(author, book)

    book_authors = orm.get_relation(book.authors)
    assert all(book not in book_authors for book in author_list)
    assert len(orm.get_relation(book.authors)) == 0

    objects_len = sum(len(orm.get_type(x)) for x in [Book, Author])
    assert objects_len == 0


def test_add_remove_many_both(orm):
    author_list = {Author() for _ in range(SAMPLE_SIZE)}
    book_list = {Book() for _ in range(SAMPLE_SIZE)}
    product = list(itertools.product(author_list, book_list))

    for author, book in product:
        orm.add(author, book)

    book_relations = sum([len(orm.get_relation(x.books)) for x in author_list])
    author_relations = sum([len(orm.get_relation(x.authors)) for x in book_list])

    objects_len = sum(len(orm.get_type(x)) for x in [Book, Author])
    assert objects_len == len(author_list) + len(book_list)
    assert book_relations == pow(SAMPLE_SIZE, 2)
    assert author_relations == pow(SAMPLE_SIZE, 2)

    for author, book in product:
        assert author in orm.get_relation(book.authors)
        assert book in orm.get_relation(author.books)

    for author, book in product:
        orm.remove(author, book)

    for author, book in product:
        assert all(book not in orm.get_relation(author.books) for author in author_list)
        assert all(author not in orm.get_relation(book.authors) for book in book_list)
        assert len(orm.get_relation(book.authors)) == 0
        assert len(orm.get_relation(author.books)) == 0

    objects_len = sum(len(orm.get_type(x)) for x in [Book, Author])
    assert objects_len == 0
