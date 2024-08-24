from flask import Flask, render_template, url_for, jsonify, request
from mysql import connector
import sys
import logging
import threading
logging.basicConfig(filename='/home/ec2-user/network_app/aws_network_concepts.log', level=logging.INFO)

app = Flask(__name__)

# Object that will hold last connection state
connection_state = {'connected': False, 'error': "Never connected"}


def connect(connection_state=None):
    logging.info('will connect')

    host = '10.10.2.10'
    database = 'mysql'
    user = 'ec2'
    password = 'Craz1Passw0rd#'
    try:
        mydb = connector.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            connection_timeout=2
        )
        print('connected')
        mydb.close()
        print('close')
        if connection_state is not None:
            connection_state['connected'] = True
            connection_state['error'] = ""
            return connection_state
        else:
            return {'connected': True, 'error': ""}
    except:
        cls, e, tb = sys.exc_info()
        print(e)
        print(cls)
        print(tb)
        logging.info(e)
        logging.info(cls)
        logging.info(tb)
        if connection_state is not None:
            connection_state['connected'] = False
            connection_state['error'] = str(e)
            return connection_state
        else:
            return {'connected': False, 'error': str(e)}
        return connection_state


@app.route('/')
def index():
    return render_template('index.html', meta=connection_state)


@app.route('/check')
def check_mysql():
    return connect(connection_state)

## Try to connect at background when app starts
connect_thread = threading.Thread(target=connect, name="Connect", args=[connection_state])
connect_thread.start()

if __name__ == "__main__":
    app.run(debug=False)
