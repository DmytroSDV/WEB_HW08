
from conn_modd.models import Author, Quote
import conn_modd.connect


authors = Author.objects(fullname__iregex="Steve Martin")
result = {}
for a in authors:
    quotes = Quote.objects(author=a)
    result[a.fullname] = [q.quote for q in quotes]

print(result)