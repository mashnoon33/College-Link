'''
    api.py
    Mash Ibtesum, October 23, 2018
    Simple API to retrive data from the schools databse
'''

import psycopg2
import sys
import flask
import json
import ast
from config import *
from flask import request
from urllib.parse import urlparse, parse_qs

app = flask.Flask(__name__, static_folder='static')

@app.after_request
def after_request(response):
    '''
    Allows cross domain origins by adding the appropriate headers to the responses
    '''
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def hello():
    '''
    Generic response for the home page
    '''
    print("hello")
    return('Youve reached the home of the APIIII')

@app.route('/schools/',methods=['GET'])
def schools():
    '''
    Filter the list of schools using the query parameters. At any moment, multiple
    parameters are going to be used.

    RESPONSE: a list of 20 schools with the following details :
              * name
              * location
              * acceptance rate
              * SAT
              * ACT
              * Yearly Tuition
              * Diversity
              * Mid Career Income
              * SERIAL/ 8 digit unique id (OPEID)

    GET Parameters :
    Parameters  |   Required   |          Valid Options          |   DEFAULT    |     DESCRIPTION
    ------------------------------------------------------------------------------
    ownership           y            public(1), private(2), all (TXT)       all
    degree              y                 2(1), 4(2), grad(3), all (TXT)            all           2 year or 4 year colleges
    majors              n               see MAJOR_LIST (TXT)         all
    region_id           n              see REGION_ID_LIST (INT)      all
    SAT_AVG             y                   200 - 1600 (INT ARR)    [800-1600]      AVG SAT score
    ACTCMMID            y                    0-36 (INT ARR)         [15-34]          ACT midpoint
    COSTT4_A            y                 0 - 100,000 (INT ARR)   [0 - 100,000]     Avg Cost of attendace
    MD_EARN_WNE_P9      y                 0 - 300,000 (INT ARR)   [0 - 300,000]      Median earning after 9 yrs
    ADM_RATE            y                  0 - 1  (INT ARR)         [0 - 1]         Admission rate in decimals
    page                y                 1 - 1000 (INT)                1           Number of page to display
    '''
    # TODO: (Optional) implement majors as a search query
    try:
        response  = getSchools(
        ast.literal_eval(request.args.get('adm_rate')),
        ast.literal_eval(request.args.get('sat_avg')),
        ast.literal_eval(request.args.get('region_id')),
        ast.literal_eval(request.args.get('ACTCMMID'.lower())),
        ast.literal_eval(request.args.get('md_earn_wne_p10')),
        ast.literal_eval(request.args.get('COSTT4_A'.lower())),
        ast.literal_eval(request.args.get('owner')),
        ast.literal_eval(request.args.get('degree'))
        )
        return(json.dumps(response, indent=4))
    except Exception as e:
        print(e)
        return("Wrong query. Check the API doc because the example is too long")


@app.route('/school/',methods=['GET'])
def school():
    '''
    Returns detailed profile of a singular college provided the 8 digit OPID
    '''
    try:
        response = getSchool(int(request.args.get('opeid')))
        return(json.dumps(response, indent=4))
    except Exception as e:
        print(e)
        return("Wrong query. Check the console log. \nExcepted structure : /school/?opeid=[insertOpeidHere]")

@app.route('/schools/name/<name>')
def schoolsByName(name):
    '''
    Filter the list of schools using the name parameter. Ignores other parameter. The result is similar to /schools
    '''
    try:
        response = getSchoolsByName(str(name))
        return(json.dumps(response, indent=4))
    except Exception as e:
        print(e)
        return("Wrong query. Check the console log. \nExcepted structure : /schools/name/?name=[insertNameHere]")

@app.route('/states/', methods=['GET'])
def states():
    try:
        return(json.dumps(getStates(), indent=4))
    except Exception as e:
        print(e)
        return("Contact your sys admin")

# TODO: implement /major and /regions and also enum.
# TODO: Add sort (?) Looks good as is


@app.route('/regions/', methods=['GET'])
def regions():
    try:
        return(json.dumps(getRegions(), indent=4))
    except Exception as e:
        print(e)
        return("Contact your sys admin")

def getConnectection():
    '''
    Returns a connection to the database described
    in the config module. Returns None if the
    connection attempt fails.
    '''
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
        print(e)
        exit()
    return connection

def getSchools(adm_rate, sat_avg, region_id, ACTCMMID, md_earn_wne_p10, COSTT4_A, ownership, degree):
    '''
    Is called by /schools/ endpoint. Uses psycopg2 to run the command appropriate sql
    query and returns the result as an array of dicts.
    '''
    try:
        connection = getConnectection()
        cursor = connection.cursor()
        query = '''
        SELECT name, CITY, state, OPEID, ACTCMMID, ADM_RATE,  SAT_AVG, UGDS_WHITE, COSTT4_A, MD_EARN_WNE_P10, insturl, degree, owner
        FROM schools
        WHERE sat_avg >= {}
        AND sat_avg <={}
        AND md_earn_wne_p10 >= {}
        AND md_earn_wne_p10 <= {}
        AND ACTCMMID >= {}
        AND ACTCMMID <={}
        AND COSTT4_A >= {}
        AND COSTT4_A <={}
        AND adm_rate >= {}
        AND adm_rate <= {}
        '''.format(sat_avg[0],sat_avg[1],
         md_earn_wne_p10[0], md_earn_wne_p10[1],ACTCMMID[0], ACTCMMID[1],
         COSTT4_A[0],COSTT4_A[1], adm_rate[0],adm_rate[1])
        if region_id:
            query+= "\n AND region_id = " + str(region_id)
        if degree:
            query+= "\n AND degree <= " + str(degree)
        if ownership:
            query+= "\n AND owner = " + str(ownership)
        query += "\nORDER BY adm_rate ASC"
        cursor.execute(query)
        answer = []
        # header = [field[0] for field in cursor.description]
        header = ['name', 'city', 'state', 'opeid', 'actcmmid', 'adm_rate', 'sat_avg', 'ugds_white', 'costt4_a', 'md_earn_wne_p10', 'insturl', 'degree', 'owner']
        body = []

        for row in cursor:
            body.append(row)

        # Generates the dics using the provided headers.
        for school in body:
            school_dict = {}
            for i in range(0, len(header)):
                school_dict[header[i]] = school[i]
            answer.append(school_dict)
        connection.close()
        return answer

    except Exception as e:
        print(e)
        connection.close()
        return None

def getSchoolsByName(name):
    '''
    Is called by /schools/name endpoint. Uses psycopg2 to run the command appropriate sql
    query and returns the result as an array of dicts.
    '''
    try:
        connection = getConnectection()
        cursor = connection.cursor()
        query ='''
        SELECT name, CITY, state, OPEID, ACTCMMID, ADM_RATE,  SAT_AVG, UGDS_WHITE, COSTT4_A, MD_EARN_WNE_P10, insturl, degree, owner
        FROM schools
        WHERE name ilike '%{}%'
        '''.format(name)

        cursor.execute(query)
        answer = []
        # header = [field[0] for field in cursor.description]
        header = ['name', 'city', 'state', 'opeid', 'actcmmid', 'adm_rate', 'sat_avg', 'ugds_white', 'costt4_a', 'md_earn_wne_p10', 'insturl', 'degree', 'owner']
        body = []

        for row in cursor:
            body.append(row)

        for school in body:
            school_dict = {}
            for i in range(0, len(header)):
                school_dict[header[i]] = school[i]
            answer.append(school_dict)
        connection.close()
        return answer

    except Exception as e:
        connection.close()
        print(e)
        return None

def getStates():
    '''
    Is called by /staets endpoint. Uses psycopg2 to run the command appropriate sql
    query and returns the result as a specially formatted dictionary designed to cater
    to Semantic UI Framework's dropdown.
    '''
    try:
        connection = getConnectection()
        cursor = connection.cursor()
        query ='''
        SELECT name, abbr
        FROM states
        '''

        cursor.execute(query)
        answer = {}
        answer["sucess"] = True
        answer["results"] = []
        # header = [field[0] for field in cursor.description]

        for row in cursor:
            td = {}
            td["value"]= row[1]
            td["name"]= row[0]
            td["text"]= row[0]
            answer["results"].append(td)
        connection.close()
        return answer

    except Exception as e:
        print(e)
        connection.close()
        return None


def getRegions():
    '''
    Is called by /staets endpoint. Uses psycopg2 to run the command appropriate sql
    query and returns the result as a specially formatted dictionary designed to cater
    to Semantic UI Framework's dropdown.
    '''
    try:
        connection = getConnectection()
        cursor = connection.cursor()
        query ='''
        SELECT id, name
        FROM region
        '''

        cursor.execute(query)
        answer = {}
        answer["sucess"] = True
        answer["results"] = []
        # header = [field[0] for field in cursor.description]

        for row in cursor:
            td = {}
            td["value"]= row[0]
            td["name"]= row[1]
            td["text"]= row[1]
            answer["results"].append(td)
        connection.close()
        return answer

    except Exception as e:
        print(e)
        connection.close()
        return None

def getSchool(opeid):
    '''
    Is called by /school endpoint. Uses psycopg2 to run the command appropriate sql
    query and returns the result as a dict.
    '''
    try:
        connection = getConnectection()
        cursor = connection.cursor()
        query ='''
        SELECT *
        FROM schools
        WHERE opeid = {}
        '''.format(opeid)
        cursor.execute(query)
        header = [field[0] for field in cursor.description]
        body = [row for row in cursor]
        # Generates the dict, matching the header with the data
        for school in body:
            school_dict = {}
            for i in range(0, len(header)):
                school_dict[header[i]] = school[i]
        connection.close()
        return school_dict

    except Exception as e:
        connection.close()
        print(e)
        return None


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: {0} host port'.format(sys.argv[0]))
        print('  Example: {0} perlman.mathcs.carleton.edu 5101'.format(sys.argv[0]))
        exit()
    host = sys.argv[1]
    port = int(sys.argv[2])
    app.run(host=host, port=port, debug=True)
