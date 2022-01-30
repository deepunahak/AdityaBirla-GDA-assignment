"""
Description: This file does below tasks
            1. load all the IFSC Data into the memory
               (Data Structure - Dict<IFSC, IFSCObject>) from the  excel file.
            2. IFSC object load into memory
            3. Data Structure [Bank LeaderBoard] - Dict <BANK, count_of_bank> and compute from the base data and load.
            4. Data Structure [Statistics] - List <IFSC, Timestamp> to hold the search history (only  valid ifsc code
               to enter this list, and the timestamp of the request>
            5. API endpoints
                - IFSC Search :: input parameter: ifsc_code (mandatory)
                                 output -> object, handle null, empty, invalid data etc; ifsc not found, return 404
                                 header
                - Bank LeaderBoard :: input parameter -> (NONE); output -> Top 10 descending
                                   :: input parameter -> sortorder (DESC|ASC); default value DESC
                                   :: input parameter -> fetchcount (1..225); default value - 10
                - Statistics :: input parameter -> (NONE); output -> ALL in the list ASC
                             :: input parameter -> sortorder (DESC|ASC); default value ASC
                             :: input parameter -> fetchcount (1..10000); default value - ALL (entire list)

Author: Deepu Ranjan Nahak
Created Date: 28-01-2022
"""
# import statements
import json
from flask import (Flask, request, Response)
import pandas as pd
from ifsc import Ifsc
import config
from datetime import datetime
from collections import OrderedDict

# app
app = Flask(__name__)

IFSC = {}
BANK_LEADERBOARD = OrderedDict()
STATISTICS = []


def log(msg):
    print("{}: {}".format(datetime.now(), msg))


# load all the IFSC Data into the memory (Data Structure - Dict<IFSC, IFSCObject>)
def load_data(data_path):
    try:
        global BANK_LEADERBOARD
        global IFSC
        log("START UP - load IFSC data into cache -")
        df = pd.read_excel(data_path)
        # adding data into cache
        for index, row in df.iterrows():
            ifsc_obj = Ifsc(row['BANK'],
                            row['IFSC'],
                            row['MICR CODE'],
                            row['BRANCH'],
                            row['ADDRESS'],
                            row['STD CODE'],
                            row['CITY'],
                            row['DISTRICT'],
                            row['STATE'])
            IFSC[row['IFSC']] = ifsc_obj
        log("IFSC OBJECTS - loaded successfully -")

        # Load data for leader board
        leaderboard_df = df[['BANK', 'IFSC']].groupby(['BANK']).agg(['count'])
        temp_leader_board = {str(bank): int(row['count']) for bank, row in leaderboard_df['IFSC'].iterrows()}
        BANK_LEADERBOARD = OrderedDict(sorted(temp_leader_board.items(), key=lambda x: x[1], reverse=True))
        log("BANK LEADER BOARD - loaded successfully -")

    except Exception as err:
        log(f"{err}: can't load IFSC!!")


# Data Structure [Statistics] - List <IFSC, Timestamp> to hold the search history
# (only  valid ifsc code to enter this list, and the timestamp of the request)
def log_statistics(IFSC):
    try:
        global STATISTICS
        STATISTICS.append((IFSC, str(datetime.now())))
    except Exception as err:
        log(f"{err}: can't load statics!!")


@app.route('/ifsc_search', methods=['GET'])
def find_ifsc():
    try:
        ifsc_code = request.args.get('ifsc_code')
        log("Searching IFSC : " + str(ifsc_code))

        details = IFSC.get(ifsc_code)
        if not details:
            return Response("Details not found for IFSC " + ifsc_code,
                            status=404, mimetype="application/json")

        log("FOUND IFSC details")
        log(details)
        log_statistics(ifsc_code)
        return Response(json.dumps(details.__dict__), status=200, mimetype="application/json")
    except Exception as err:
        import traceback
        traceback.print_tb(err.__traceback__)
        return Response(str(err), status=500, mimetype="application/json")


@app.route('/bank_leader_board', methods=['GET'])
def get_bank_leader_board():

    try:

        sortorder = request.args.get('sortorder', default='DESC')
        fetchcount = int(request.args.get('fetchcount', default=10))

        result_dict = OrderedDict()
        for i, (bank, count) in enumerate(BANK_LEADERBOARD.items()):
            if i >= fetchcount:
                break
            result_dict[bank] = count

        if sortorder == "ASC":
            result_board = OrderedDict(sorted(result_dict.items(), key=lambda x: x[1], reverse=False))
        else:
            result_board = result_dict

        return Response(json.dumps(result_board), status=200, mimetype="application/json")

    except Exception as err:
        import traceback
        traceback.print_tb(err.__traceback__)
        return Response(str(err), status=500, mimetype="application/json")


@app.route('/statistics', methods=['GET'])
def statistics():
    try:
        sortorder = request.args.get('sortorder', default='ASC')
        fetchcount = int(request.args.get('fetchcount', default=len(STATISTICS)))
        temp_statistics_data_list = STATISTICS[0:fetchcount]
        if sortorder == 'DESC':
            temp_statistics_data_list = temp_statistics_data_list[::-1]

        result_statistics_data = [ [detail[0], detail[1]] for detail in temp_statistics_data_list]
        return Response(json.dumps(result_statistics_data), status=200, mimetype="application/json")

    except Exception as err:
        import traceback
        traceback.print_tb(err.__traceback__)
        return Response(str(err), status=500, mimetype="application/json")


# Press the green button in the gutter to run the script if you are running in Pycharm.
# Driver Code
if __name__ == '__main__':
    load_data(config.path)
    app.run()
