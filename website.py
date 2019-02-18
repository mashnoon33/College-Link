'''
    website.py
    Mash Ibtesum, October 23, 2018
    Simple API to retrive data from the schools databse
'''

import sys
import flask

app = flask.Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def get_main_page():
    ''' This is the only route intended for human users '''
    global api_port
    return flask.render_template('index.html', api_port=api_port)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print('Usage: {0} host port api-port'.format(sys.argv[0]), file=sys.stderr)
        exit()

    host = sys.argv[1]
    port = int(sys.argv[2])
    api_port = int(sys.argv[3])
    app.run(host=host, port=port, debug=True)
