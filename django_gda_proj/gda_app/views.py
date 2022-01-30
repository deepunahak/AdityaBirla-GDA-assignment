import json

from django.http import JsonResponse
from gda_app.flask_app_client import FlaskClient

IFSC_CACHE = {}
IFSC_HIT_COUNT = {}
API_HIT_COUNT = {}


def cache_ifsc(ifsc, details):
    global IFSC_CACHE
    IFSC_CACHE[ifsc] = details


def incr_ifsc(ifsc):
    global IFSC_HIT_COUNT
    IFSC_HIT_COUNT[ifsc] = IFSC_HIT_COUNT.get(ifsc, 0) + 1


def incr_api_cnt(api):
    global API_HIT_COUNT
    API_HIT_COUNT[api] = API_HIT_COUNT.get(api, 0) + 1


# Views for accessing flask bank_details app
def get_ifsc_details(request):
    if request.method == "GET":
        incr_api_cnt('/ifsc_search')
        try:
            ifsc_code = request.GET.get('ifsc_code')
            if not ifsc_code:
                raise KeyError("ifsc_code is required")

            # Search in the local cache
            local_data = IFSC_CACHE.get(ifsc_code)
            if local_data:
                data = local_data
                incr_ifsc(ifsc_code)
                code = 200
            else:
                client = FlaskClient()
                resp = client.search_ifsc(ifsc_code)
                if resp.status_code == 200:
                    data = json.loads(resp.text)
                    cache_ifsc(ifsc_code, data)  # Cache IFSC details
                    incr_ifsc(ifsc_code)  # Increament IFSC hit count
                else:
                    data = resp.text
                code = resp.status_code
            return JsonResponse(data, status=code, safe=False)
        except Exception as err:
            print(str(err))
            return JsonResponse(str(err), status=500, safe=False)


def get_log_statistics_details(request):
    if request.method == "GET":
        try:
            incr_api_cnt('/statistics')
            fetchcount = request.GET.get('fetchcount')

            if fetchcount and not fetchcount.isdigit():
                raise ValueError("invalid fetch count: {}".format(fetchcount))

            sortorder = request.GET.get('sortorder', "ASC")
            if sortorder not in ('ASC', 'DESC',):
                raise Exception("Invalid sortorder: {}".format(sortorder))

            client = FlaskClient()
            resp = client.get_statistics(fetchcount=fetchcount, sortorder=sortorder)
            if resp.status_code == 200:
                data = json.loads(resp.text)
            else:
                data = resp.text
            return JsonResponse(data, status=resp.status_code, safe=False)
        except Exception as err:
            print(str(err))
            return JsonResponse(str(err), status=500, safe=False)


def get_leader_board_details(request):
    if request.method == "GET":
        try:
            incr_api_cnt('/bank_leader_board')
            fetchcount = request.GET.get('fetchcount')
            if fetchcount and not fetchcount.isdigit():
                raise ValueError("invalid fetch count: {}".format(fetchcount))

            sortorder = request.GET.get('sortorder', "DESC")
            if sortorder not in ('ASC', 'DESC',):
                raise Exception("Invalid sortorder: {}".format(sortorder))

            client = FlaskClient()
            resp = client.get_bank_leader_board(sortorder=sortorder, fetchcount=fetchcount)

            if resp.status_code == 200:
                data = json.loads(resp.text)
            else:
                data = resp.text
            code = resp.status_code
            return JsonResponse(data, status=code, safe=False)
        except Exception as err:
            print(str(err))
            return JsonResponse(str(err), status=500, safe=False)


def get_api_hit_count(request):
    if request.method == "GET":
        try:
            return JsonResponse(API_HIT_COUNT, status=200, safe=False)
        except Exception as err:
            print(str(err))
            return JsonResponse(str(err), status=500, safe=False)


def get_ifsc_hit_count(request):
    if request.method == "GET":
        try:
            return JsonResponse(IFSC_HIT_COUNT, status=200, safe=False)
        except Exception as err:
            print(str(err))
            return JsonResponse(str(err), status=500, safe=False)

