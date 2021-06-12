# This is the main module containing the webapp code.

from flask import Flask, render_template, request, session, copy_current_request_context
from threading import Thread
from letters import search4letters
from DBcm import UseDatabase, ConnectionError, CredentialsError, SQLError
from checker import check_logged_in

app = Flask(__name__)
app.secret_key = 'HxKLo1H$0ghAv76$=^'
# Information for the database connector
app.config['dbconfig'] = {
        'host': '127.0.0.1',
        'user': 'vsearch',
        'password': 'vsearchpasswd',
        'database': 'vsearchlogDB'
    }


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':

    @copy_current_request_context
    # ^ This makes sure that variables in this scope will be copied for the Thread.
    # That means that if logging data to the database will take 30 seconds, the data that is required 
    # for the function below will be securely saved for that time and there will be no error.
    def log_request(req: 'flask_request', res: str) -> None:
        # Writes request and response data to the database.
        try:
            with UseDatabase(app.config['dbconfig']) as cursor:
                _SQL = """insert into log (phrase, letters, ip, browser_string, results)
                    values (%s, %s, %s, %s, %s);"""
                cursor.execute(_SQL, (
                    req.form['phrase'],
                    req.form['letters'],
                    req.remote_addr,
                    req.user_agent.browser,
                    res
                ))
        except CredentialsError as err:
            print('*** Invalid username/password. Error: ', err)
        except SQLError as err:
            print('*** Invalid SQL syntax. Error: ', err)

    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    try:
        # Log the request in the database using a Thread, so the user doesn't have to wait for the results
        t = Thread(target=log_request, args=(request, results))
        t.start()
    except ConnectionError as err:
        print('*** Is your database switched on? Error: ', err)
    except Exception as err:
        print('*** Cannot log the request into the database. Error: ', err)
    return render_template(
        'results.html',
        the_title='Results:',
        the_phrase=phrase,
        the_letters=letters,
        the_results=results
    )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template(
        'entry.html', 
        the_title='Welcome to search4letters on the web!'
    )

@app.route('/viewlog')
@check_logged_in    # <- The access is restricted only for a logged in user
def view_log() -> 'html':
    # Shows the database's log of request and response data
    try:
        with UseDatabase(app.config['dbconfig']) as cursor:
            _SQL = """select phrase, letters, ip, browser_string, results from log;"""
            cursor.execute(_SQL)
            contents =  cursor.fetchall()
    except CredentialsError as err:
        print('*** Invalid username/password. Error: ', err)
    except SQLError as err:
        print('*** Invalid SQL syntax. Error: ', err)


    return render_template(
        'viewlog.html',
        the_title='View Log',
        row_titles=('Phrase', 'Letters', 'IP Address', 'User Agent', 'Response'),
        the_data=contents
    )

# Simple simulation of login and logout mechanism
@app.route('/login')
def do_login() -> str:
    session['logged_in'] = True
    return 'You are now logged in.'

@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out.'

if __name__ == '__main__':
    app.run(debug=True)