from flask import Flask, jsonify
from models import Base, Transaction, engine, create_connection
from datetime import datetime, timedelta


app = Flask(__name__)

Base.metadata.create_all(engine)

AMOUNT_LIMITS_CONFIG = {10: 1000, 60: 3000, 3600: 20000}


@app.route('/request/<int:amount>', methods=['GET'])
def index(amount):
    max_limit = max(AMOUNT_LIMITS_CONFIG.keys())
    now = datetime.now()

    connection, session = create_connection()

    query = session.query(Transaction).filter(Transaction.time >= (now - timedelta(seconds=max_limit))).all()

    if query:
        for interval, limit in AMOUNT_LIMITS_CONFIG.items():
            if sum([t.amount for t in query if t.time >= (now - timedelta(seconds=interval))]) + amount > limit:
                session.commit()
                connection.close()
                return jsonify({"error": "amount limit exeeded ({limit}/{interval}sec)".format(limit=limit,
                                                                                               interval=interval)})

    session.add(Transaction(amount))
    session.commit()
    connection.close()

    return jsonify({"result": "OK"})


if __name__ == '__main__':
    app.run()
