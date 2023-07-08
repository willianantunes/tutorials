import gevent
import requests

from django.db import connection
from django.http import HttpResponse
from django.http import JsonResponse

from django_gunicorn_gevent import settings

# This route has a delay to answer
# https://github.com/willianantunes/runner-said-no-one-ever/blob/52e30586a32a275ee2902080c0d72384db0a08b3/lib/runner_said_no_one_ever/controllers/api/v1/movies_controller.rb
runner_endpoint_movies = f"{settings.RUNNER_SAID_NO_ONE_EVER_ENDPOINT}/api/v1/movies"
# This route does not have a delay of seconds to answer
# https://github.com/willianantunes/runner-said-no-one-ever/blob/52e30586a32a275ee2902080c0d72384db0a08b3/lib/runner_said_no_one_ever/controllers/api/v1/diablo_controller.rb
runner_endpoint_diablo = f"{settings.RUNNER_SAID_NO_ONE_EVER_ENDPOINT}/api/v1/deckard-cain"


def view_http_call(request):
    response = requests.get(runner_endpoint_movies)
    assert response.status_code == 200
    return JsonResponse(response.json())


def view_do_ten_http_calls_with_gevent(request):
    jobs = [gevent.spawn(requests.get, runner_endpoint_movies) for _ in range(10)]
    gevent.joinall(jobs)
    outputs = [job.value.json() for job in jobs]
    data = {"recommendations": outputs}
    return JsonResponse(data)


def view_database_call(request):
    seconds_to_sleep = request.GET.get("seconds_to_sleep")
    seconds_to_sleep = 1 if not seconds_to_sleep else int(seconds_to_sleep)
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_sleep(%s)", [seconds_to_sleep])
    return HttpResponse(status=200)


def view_http_and_database_calls(request):
    view_http_call(request)
    return view_database_call(request)
