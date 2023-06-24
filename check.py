import mysql.connector
from flask import Flask, render_template ,request
app = Flask(__name__)

@app.route('/')

#login
def hello_world():
    return render_template('check1.html')

@app.route('/login', methods=['POST'])
def process_text():
    t = request.form['userid']
    pwd = request.form['password']
    r = process(t,pwd)
    if r == True:
        return render_template('log_success.html')
    else:
        return "not Success"
    

def process(userid, password):

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="subashini",
        database="flight_booking"
    )
    cursor = db.cursor()
    sql = "SELECT * FROM persons WHERE userid = %s"
    values = (userid,)
    cursor.execute(sql, values)
    user = cursor.fetchone()
    if(password == user[3]):
       return True
    else:
       return False
    
#flight details available
@app.route('/f_details', methods=['POST'])
def f_details():
    d = request.form['from']
    a = request.form['destination']
    da = request.form['date']
    r = f_detailsget(d,a,da)
    heading = '<h1><b>AVAILABLE FLIGHTS</b></h1><br>'
    button = '<button>next</button>'
    if r is not None:
        return  r 
    else:
        return heading + "SORRY! NO TICKETS"


def f_detailsget(dep,arr,datee):

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="subashini",
        database="flight_booking"
    )
    cursor = db.cursor()
    sql = "SELECT t1.flight_no, t1.Airline_name, t1.departure, t1.arrival, t1.take_off, t1.duration_in_mins FROM flight t1 INNER JOIN seats t2 ON t1.flight_no = t2.flightno WHERE t1.departure = %s AND t1.arrival = %s AND t2.date = %s"
    values = (dep,arr,datee)
    cursor.execute(sql,values)
    user = cursor.fetchall()
    return render_template('flight_details.html', user = user)

#ticket generation


@app.route('/ticket_gen', methods=['POST'])
def ticket_gen():
    flight_number = request.form.get('flight_number')
    airline_name = request.form.get('airline_name')
    departure = request.form.get('departure')
    arrival = request.form.get('arrival')
    takeoff_time = request.form.get('takeoff_time')
    duration = request.form.get('duration')
    quantity = request.form.get('quantity')
    date = request.form.get('date')

    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="subashini",
        database="flight_booking"
    )
    cursor = db.cursor()
    sql1 = "SELECT * FROM seats WHERE flightno = %s AND date = %s"
    values1 = (flight_number, date)
    cursor.execute(sql1, values1)
    s = cursor.fetchone()
    if s is not None and s[2] > quantity:
        sql = "UPDATE seats SET no_of_seats = no_of_seats - %s WHERE flightno = %s AND date = %s "
        values = (quantity, flight_number, date)
        cursor.execute(sql, values)
        db.commit()
        return render_template('selected_flight.html', flight_number=flight_number, airline_name=airline_name, departure=departure, date=date, arrival=arrival, takeoff_time=takeoff_time, duration=duration)
    else:
        return render_template('selected_flight.html', flight_number=flight_number, airline_name=airline_name, departure=departure, date=date, arrival=arrival, takeoff_time=takeoff_time, duration=duration)


#db.close()
if __name__ == '__main__':
    app.run(debug=True)

