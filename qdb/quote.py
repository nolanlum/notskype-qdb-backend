from qdb.models import Quote


def get(count, offset):
    return Quote.objects.order_by('-id')[:10]


def get_by_id():
    pass


def post(body):
    quote = Quote()
    quote.author = 'test@test.com'
    quote.body = body['body']
    quote.save()

    return quote


def find():
    pass


def delete():
    pass
