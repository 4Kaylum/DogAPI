from json import dumps
from sqlite3 import connect
from flask import Flask, request, g, redirect
from Utils.AllUtils import makeJson
from Utils.DatabaseFunctions import saveNewToDatabse, getRandomDogFromDatabase
from Utils.DataReturns import databaseQueryToResponse


app = Flask(__name__)
DATABASE = './DogPictures.db'


def getDatabseVariable():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect(DATABASE)
    return db


@app.teardown_appcontext
def closeDatabaseConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def mainPage():
    return 'This is the main page.'


@app.route('/api', methods=['GET', 'POST'])
def apiPage():
    if request.method == 'POST':
        return apiPagePOST()
    else:
        return apiPageGET()


@app.route('/<postID>')
def getPostInfo(postID):
    database = getDatabseVariable()
    c = database.execute('SELECT url FROM DogPictures WHERE id=?', (postID,))
    x = c.fetchall()
    return redirect(x[0][0])


@app.route('/random')
def getRandomPost():
    database = getDatabseVariable()
    c = database.execute('SELECT url FROM DogPictures ORDER BY RANDOM() LIMIT 1')
    x = c.fetchall()
    return redirect(x[0][0])


def apiPagePOST():
    database = getDatabseVariable()
    data = saveNewToDatabse(database, request.args)

    # Check for any error responses
    if data is 0:
        data = {
            'data': [],
            'count': 0
            'error': 'Not valid format. Valid formats are JPG, PNG, and GIF.'
        }
    elif data is 1:
        data = {
            'data': [],
            'count': 0
            'error': 'That image is already in the database.'
        }
    elif data is 2:
        data = {
            'data': [],
            'count': 0
            'error': 'You used an invalid JSON key. Valid keys are author and url.'
        }
    elif data is 3:
        data = {
            'data': [],
            'count': 0
            'error': 'You\'re missing the URL from your request.'
        }
    else:

        # No errors - just return data as usual
        return databaseQueryToResponse(data)

    # Return the error as is
    return makeJson(data)
    


def apiPageGET():
    database = getDatabseVariable()
    x = getRandomDogFromDatabase(database)
    return databaseQueryToResponse(x)


if __name__ == '__main__': app.run(debug=True)

