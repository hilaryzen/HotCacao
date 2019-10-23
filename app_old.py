# Team Ama-goog
# Joseph Yusufov
# Mohidul Abedin
# 2019-10-04

from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import redirect
from flask import flash
from flask import url_for
import os
import csv

app = Flask(__name__)  # create instance of class Flask
app.secret_key = os.urandom(24)

CREDENTIALS = {}

"""
USERNAME and PASSWORD ARE STORED IN static/credentials.csv
"""
with open('static/credentials.csv') as csv_file:  # open CSV file
    # instantiate CSV reader object
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0  # make sure header isn't included in dictionary
    # print(csv_reader)
    for row in csv_reader:  # populate dictionary with keys and values
        if(line_count == 0):
            line_count += 1
        else:
            CREDENTIALS[row[0]] = row[1]
# print(CREDENTIALS)


@app.route('/')  # Login Page
def index():
    # load the template with the user's session info
    if session.get("user") == CREDENTIALS.get('user') and session.get("password") == CREDENTIALS.get('password'):
        return redirect('/auth')
    return render_template('landingpage.html')


@app.route("/auth")
def authentication():
    """
    This only accepts GET requests
    """
    # print("\n" + "BODY OF REQUEST :: " + str(request))
    # print("REQUEST ARGS :: " + str(request.args)+ "\n")

    if request.args.get('username'):  # if the form was filled out
        # start a session, and populate the dictionary with the given username
        session['user'] = request.args.get('username')
        session['password'] = request.args.get('password')
    if 'user' in session:  # If the session dictionary does in fact have a user in it.
        # load the template with the user's session info
        if session.get("user") == CREDENTIALS.get('user') and session.get("password") == CREDENTIALS.get('password'):
            return render_template("responsepage.html", login_info=session, method_type=request.method)
        elif session.get("user") != CREDENTIALS.get('user'):
            flash("Invalid Username")
            return redirect(url_for('index'))
        else:
            flash("Invalid Password")
            return redirect(url_for('index'))
    return redirect(url_for('index'))


# Logout removes the User's session from the dictionary stored on the server, even if the cookie still exists
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged Out Succesfully")
    return redirect(url_for("index"))


print(CREDENTIALS)
if __name__ == "__main__":
    app.debug = True
    app.run()