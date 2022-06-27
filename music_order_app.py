from flask import Flask, request, jsonify, render_template
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return "Home Page"


@app.route('/new_order')
def new_order():
    return render_template('order.html')


@app.route('/create_order', methods=['POST'])
def create_order():
    con = sql.connect("music_record.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute('''
                      CREATE TABLE IF NOT EXISTS music_records
                      ([firstName] TEXT, [lastName] TEXT, [orderType] TEXT, [budget] INTEGER, [deadline] DATE)
                      ''')

    try:
        app.logger.info(request.form)
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        orderType = request.form['orderType']
        budget = request.form['budget']
        deadline = request.form['deadline']

        with sql.connect("music_record.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO music_records (firstName,lastName,orderType,budget,deadline) VALUES(?, ?, ?, ?, ?)", (firstName, lastName, orderType, budget, "date("+deadline+")"))
                con.commit()
                app.logger.info('Record successfully added')
    except:
        con.rollback()
        app.logger.info('Error in insert operation')

    cur.close()
    con.close()
    return 'Order created'


@app.route('/get_orders', methods=['GET'])
def get_orders():
    con = sql.connect("music_record.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    rows = cur.execute("select * from music_records")
    return render_template('order_list.html', rows=rows)
