import requests
import json



class FlaskClient(object):
    """
    A REST client library to call the flask application apis
    """
    def __init__(self, host="localhost", port=5000):
        self.host = host
        self.port = port
        self.base_url = "http://{host}:{port}/".format(host=host, port=port)
        self.headers = {'Content-type': 'application/json'}

    def search_ifsc(self, ifsc_code):

        url = self.base_url + "ifsc_search?ifsc_code=" + ifsc_code
        return requests.get(url, headers=self.headers)

    def get_statistics(self, sortorder="ASC", fetchcount=None):
        url = self.base_url + "statistics"
        if sortorder:
            url += "?sortorder="+str(sortorder)
        if fetchcount:
            url += "&fetchcount=" + str(fetchcount)

        return requests.get(url, headers=self.headers)

    def get_bank_leader_board(self, sortorder="DESC", fetchcount=10):
        url = self.base_url + "bank_leader_board"
        if sortorder:
            url += "?sortorder=" + str(sortorder)
        if fetchcount:
            url += "&fetchcount=" + str(fetchcount)

        return requests.get(url, headers=self.headers)
