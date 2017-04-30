from flask import abort

from qdb.models import Quote


def get(count, offset):
    return [
        quote.json()
        for quote in Quote.objects.order_by('-id').skip(offset).limit(count)
    ]


def get_by_id(quoteId):
    try:
        return Quote.objects.get(num=quoteId).json()
    except Quote.DoesNotExist:
        abort(404)


def post(body):
    if not body.get('body'):
        abort(400)

    quote = Quote()
    quote.author = 'test@test.com'
    quote.body = body['body']
    quote.save()

    return quote.json()


def find(query):
    quotes = Quote.objects.search_text(query)
    return [quote.json() for quote in quotes]


def delete(quoteId):
    try:
        Quote.objects.get(num=quoteId).delete()
    except Quote.DoesNotExist:
        pass
