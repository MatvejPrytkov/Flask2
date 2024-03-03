from author import Author
from schema import AuthorSchema


author = Author(1, "Alex", "alex5@mail.ru")

author_schema = AuthorSchema()

result = author_schema.dump(author)
print(type(result))
print(result)


authors = [Author("1", "Alex"), Author("1", "Ivan"), Author("1", "Tom")]
# Variant 1 в качестве ответа -> список словарей
result_one = author_schema.dump(authors, many=True)
print(repr(result_one), type(result_one))

# Variant 2 в качестве ответа -> список из JSON строк
authors_schema = AuthorSchema(many=True)
result_two = authors_schema.dumps(authors)
print(repr(result_two), type(result_two))
