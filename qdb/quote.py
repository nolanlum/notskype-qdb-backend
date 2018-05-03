from random import randint

from flask import abort

from qdb.auth import slack_authenticate, fetch_slack_identity
from qdb.models import Quote


@slack_authenticate
def get(count, offset):
    return [
        quote
        for quote in Quote.objects.order_by('-id').skip(offset).limit(count)
    ]


@slack_authenticate
def get_by_id(quoteId):
    try:
        return Quote.objects.get(num=quoteId)
    except Quote.DoesNotExist:
        abort(404)


@slack_authenticate
def post(body):
    if not body.get('body'):
        abort(400)

    user = fetch_slack_identity()

    quote = Quote()
    quote.author = user.email
    quote.body = body['body']
    quote.save()

    return quote


@slack_authenticate
def find(query):
    quotes = Quote.objects.search_text(query).order_by('-id')
    return [quote for quote in quotes]


@slack_authenticate
def rand():
    max_num_quote = Quote.objects.order_by('-num').scalar('num').first()
    if not max_num_quote:
        abort(404)

    rand_num = randint(1, max_num_quote)
    rand_quote = Quote.objects(
        num__lte=rand_num,
    ).order_by('-num').first()

    return rand_quote


@slack_authenticate
def delete(quoteId):
    try:
        Quote.objects.get(num=quoteId).delete()
    except Quote.DoesNotExist:
        pass
