from schema import AuthorSchema
import json

json_data = """
{
   "name": "Ivan",
   "email": "ivan@mail.ru"
}
"""
json_data_as_dict = json.loads(json_data)

schema = AuthorSchema()
result = schema.load(json_data_as_dict)
print(result)

result = schema.loads(json_data)
print(result)

json_data_list = """
[
   {
       "id": 1,
       "name": "Alex",
       "email": "alex@mail.ru"
          },
   {
       "id": 2,
       "name": "Ivan",
       "email": "ivan@mail.ru"
   },
   {
       "id": 4,
       "name": "Tom",
       "email": "tom@mail.ru"
   }
]
"""
# При обработке списка, необходимо указать параметр many=True 
# либо при создании экземпляра схемы либо при вызове метода loads
# Variant 1
authors_schema = AuthorSchema(many=True)
result_one = authors_schema.loads(json_data_list)
print(result_one)

# Variant 2
result_two = schema.loads(json_data_list, many=True)
print(result_two)
