"""
Railway Reservation System - Flask Backend (FIXED VERSION)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from railwayreserve1.db import get_connection

app = Flask(__name__)
CORS(app)

# ---------------- FARE MAP ----------------
FARE_MAP = {
    'Sleeper': 300,
    'AC 3-Tier': 500,
    'AC 2-Tier': 800,
}

def calc_fare(class_type):
    return FARE_MAP.get(class_type, 300)

# ---------------- HELPERS ----------------
def success(data, code=200):
    return jsonify(data), code

def error(msg, code=400):
    return jsonify({"error": msg}), code


# ================= TRAINS =================

@app.route('/trains', methods=['GET'])
def get_trains():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT * FROM trains ORDER BY train_id")
        data = cur.fetchall()
        return success(data)
    except Exception as e:
        return error(str(e), 500)
    finally:
        cur.close()
        conn.close()


@app.route('/trains', methods=['POST'])
def add_train():
    data = request.get_json()

    required = ['train_name', 'source', 'destination', 'schedule', 'seats']
    if not data:
        return error("JSON body required")

    missing = [f for f in required if not data.get(f)]
    if missing:
        return error(f"Missing fields: {', '.join(missing)}")

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO trains (train_name, source, destination, schedule, seats)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['train_name'],
            data['source'],
            data['destination'],
            data['schedule'],
            int(data['seats'])
        ))

        conn.commit()
        return success({"message": "Train added"}, 201)

    except Exception as e:
        return error(str(e), 500)

    finally:
        cur.close()
        conn.close()


# ================= SEARCH =================

@app.route('/search', methods=['GET'])
def search():
    source = request.args.get('from')
    dest = request.args.get('to')

    if not source or not dest:
        return error("from and to required")

    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("""
            SELECT * FROM trains
            WHERE source LIKE %s AND destination LIKE %s
        """, (f"%{source}%", f"%{dest}%"))

        return success(cur.fetchall())

    except Exception as e:
        return error(str(e), 500)

    finally:
        cur.close()
        conn.close()


# ================= BOOKINGS =================

@app.route('/bookings', methods=['GET'])
def get_bookings():
    conn = get_connection()
    cur = conn.cursor(dictionary=True)

    try:
        cur.execute("SELECT * FROM bookings ORDER BY ticket_id DESC")
        data = cur.fetchall()

        for d in data:
            if d.get("journey_date"):
                d["journey_date"] = str(d["journey_date"])

        return success(data)

    except Exception as e:
        return error(str(e), 500)

    finally:
        cur.close()
        conn.close()


@app.route('/bookings', methods=['POST'])
def create_booking():
    data = request.get_json()

    if not data:
        return error("JSON body required")

    required = ['train_name', 'passenger_name', 'age', 'class', 'journey_date']
    missing = [f for f in required if not data.get(f)]

    if missing:
        return error(f"Missing fields: {', '.join(missing)}")

    try:
        age = int(data['age'])
        if age <= 0 or age > 120:
            return error("Invalid age")
    except:
        return error("Age must be number")

    class_type = data['class']
    if class_type not in FARE_MAP:
        return error("Invalid class")

    fare = calc_fare(class_type)

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO bookings
            (train_name, passenger_name, age, class, journey_date, fare, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            data['train_name'],
            data['passenger_name'],
            age,
            class_type,
            data['journey_date'],
            fare,
            "Confirmed"
        ))

        conn.commit()

        return success({
            "message": "Booking successful",
            "ticket_id": cur.lastrowid,
            "fare": fare
        }, 201)

    except Exception as e:
        return error(str(e), 500)

    finally:
        cur.close()
        conn.close()


# ================= HEALTH =================

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_connection()
        conn.close()
        return success({"status": "ok"})
    except Exception as e:
        return error(str(e), 500)


# ================= RUN =================

if __name__ == "__main__":
    print("🚆 Railway Backend Running at http://127.0.0.1:5000")
    app.run(debug=True)