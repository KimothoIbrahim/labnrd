#!/usr/bin/python3
""" This app builds features to provide
information on where to find critical
analytical chemistry instruments in Kenya
"""

import MySQLdb
import requests
import secrets
import os
import json
from PIL import Image
from flask_bcrypt import Bcrypt
from flask import Flask, render_template, url_for, redirect, flash, session, request, jsonify
from forms import user_registration, user_login, instrument_enlist

conn = MySQLdb.connect(host="localhost", user="labnerd_user", passwd="labn3rd", db="labnerd_db")

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = '414d09b5b79cd5230f799c811d2f28b6'

@app.route("/")
@app.route("/home")
def labnerd_home():
    """ Home page for labnerd chemical analysis solutions """
    cur = conn.cursor()
    cur.execute("""SELECT name FROM categories;""")
    res = cur.fetchall()
    cur.close()
    return render_template("home.html", categories=res, user=session.get('client_id'))

@app.route("/instruments")
def labnerd_instruments():
    cur = conn.cursor()
    cur.execute("""SELECT instruments.name, instruments.description,
                instruments.price_per_sample, instruments.price_per_day,
                instruments.price_per_week, instruments.location, clients.surname,
                instruments.id
                FROM instruments INNER JOIN clients ON instruments.client_id = clients.id;""")
    res = cur.fetchall()
    cur.close()
    return render_template("instruments.html", res=res, user=session.get('client_id'))

@app.route("/instruments/<category>")
def labnerd_instruments_catergory(category):
    """dispaly all instruments on offer"""
    if category:
        cur = conn.cursor()
        cur.execute(f"""SELECT instruments.name, instruments.description,
                instruments.price_per_sample, instruments.price_per_day,
                instruments.price_per_week, instruments.location, clients.surname,
                instruments.id
                FROM instruments INNER JOIN clients ON instruments.client_id = clients.id
                INNER JOIN categories ON instruments.category_id = categories.id
                WHERE categories.name = '{category}';""")
        res = cur.fetchall()
        cur.close()
        return render_template("instruments.html", res=res, category=category,  user=session.get('client_id'))

@app.route("/notes")
def labnerd_notes():
    """ Display informative notes on varied technologies"""
    return render_template("notes.html", user=session.get('client_id'))

@app.route("/instrument_enlist", methods=['GET', 'POST'])
def labnerd_instrument_enlist():
    """The selling-user's form to enlist new instrument"""
    instrument = instrument_enlist()

    if 'client_id'  not in session:
        return render_template("createactoenlist.html")
    print(session['client_id'])
    if instrument.validate_on_submit():
        cur = conn.cursor()
        cur.execute("""INSERT INTO instruments(name, price_per_day, price_per_week,
                    price_per_sample, category_id, client_id, description, location, instrument_image)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                    (instrument.name.data, instrument.price_per_day.data,
                    instrument.price_per_week.data, instrument.price_per_sample.data, 1,
                    session['client_id'], instrument.description.data, instrument.location.data,
                    instrument.instrument_image.data))
        conn.commit()
        return redirect(url_for('labnerd_instruments'))
    return render_template("instrument_enlist.html", form=instrument,
                           title='Enlist instrument', user=session.get('client_id'))

@app.route("/user_registration", methods=['GET', 'POST'])
def labnerd_user_registration():
    """form to signup for a labnerd account"""
    newUser = user_registration()
    
    if newUser.validate_on_submit():
        hashpee = bcrypt.generate_password_hash(newUser.password.data).decode('utf-8')
        cur = conn.cursor()
        cur.execute("""INSERT INTO clients(firstname, surname, phone,  email, password, buying_user, selling_user)
                    VALUES(%s, %s, %s, %s, %s, %s, %s );""", (newUser.firstname.data,
                    newUser.surname.data, newUser.phone.data, newUser.email.data,
                    hashpee, newUser.buying_user.data, newUser.selling_user.data))
        conn.commit()
        flash(f'Your account was created successfully! You can now login', 'lightgreen')
        return redirect(url_for('labnerd_login'))

    return render_template("user_registration.html", title='Create Account', form=newUser)

@app.route("/selling_user_dashboard")
def labnerd_selling_user_dashboard():
    """show a list of enlisted instruments, bookings  and sales"""
    return render_template("selling_user_dashboard.html", user=session.get('client_id'))

@app.route("/login", methods=['GET', 'POST'])
def labnerd_login():
    """ login to be able to buy and enlist instruments and view own dashboard """
    login = user_login()
    
    if login.validate_on_submit():
        cur = conn.cursor()
        cur.execute("SELECT id, surname, email, password FROM clients;")
        clients = cur.fetchall()
        for client_id, surname, email, password in clients:
            if email == login.email.data and bcrypt.check_password_hash(password, login.password.data):
                flash(f'Succesful Login!', 'lightgreen')
                session['client_id'] = client_id
                return redirect(url_for('labnerd_home'))
        flash(f'Incorrect email or password', 'red')
        cur.close()
    return render_template("login.html", form=login, title='Login')

@app.route("/logout")
def labnerd_logout():
    """ Log user of their account """
    session.pop('client_id', None)
    return redirect(url_for("labnerd_home"))

@app.route("/email")
def labnerd_email():
    """ send email to labnerd.com """
    pass

@app.route("/profile", methods=['GET', 'POST'])
def labnerd_profile():
    """ send email to labnerd.com """
    if not session.get('client_id'):
        flash('you must be logged in to see your account', 'rgba(255, 0, 0, .8)')
        return redirect(url_for('labnerd_login'))
    else:
        prof_pic = 'default.jpg'
        if request.method == "POST":
            hexedPicName = secrets.token_hex(8)
            if (request.files.get('prof_pic')):
                pic = request.files.get('prof_pic')
                _, file_ext = os.path.splitext(pic.filename)
                pic_path = os.path.join(app.root_path, 'static/images', f'{hexedPicName}{file_ext}')
                
                resize = (125, 125)
                pic = Image.open(pic)
                pic.thumbnail(resize)
                pic.save(pic_path)
        return render_template("profile.html", user=session.get('client_id'), prof_pic=prof_pic)

@app.route("/callback", methods=['POST'])
def callback():
    """ mpeas callback"""
    data = request.get_json()
    print(data)
    resultCode = data['Body']['stkCallback']['ResultCode']

    if resultCode != 0:
        err = data['Body']['stkCallback']['ResultDesc']
        res = {'ResultCode': resultCode, 'ResultDesc': err}
        return jsonify(res)

    datadata = data['Body']['stlCallback']['CallbackMetadata']
    amount = None
    phone = None
    for item in datadata['item']:
        if item['Name'] == 'Amount':
            amount = item['Value']
        elif item['Name'] == 'PhoneNumber':
            phone == item['Value']

    with open('mpesa.txt', 'w') as mpesa:
        mpesa.write(f'"amount":"{amount}"\n')
        mpesa.write(f'"phone":"{phone}"\n')

    res = {'ResultCode': resultcode, 'ResultDesc': 'Success'}
    return jsonify(res)


@app.route("/buy/<inst_id>/<user_id>")
def buy(inst_id, user_id):
    """ activate mpesa """
    if 'client_id' in session:
        cur = conn.cursor()
        cur.execute("""SELECT instruments.price_per_sample
                    FROM instruments
                    WHERE instruments.id = %s;""", (inst_id))
        res = cur.fetchone()
        amount = res[0]
        cur.execute("""SELECT clients.phone
                    FROM clients WHERE clients.id = %s;""", (user_id))
        res = cur.fetchone()
        cur.close()
        phone = res[0]
        from Requests import mpesa
        mpesa(amount, phone)
        return f"Prompt sent to {phone}. Confirm to complete paying {amount}"
    
    return redirect(url_for('labnerd_login'))

if __name__ == "__main__":
    """ labnerd GoLive """
    app.run(host="0.0.0.0", port=5006, debug=True)
