from flask import Flask, request, jsonify
import cx_Oracle
from reactivex import create


userpwd = "APIMPINVANTARIO###2022" # Obtain password string from a user prompt or environment variable

connection = cx_Oracle.connect(user="API_MP_INVENTARIO", password=userpwd,
                               dsn="orarac-hlg-db-scan.dc.nova:1521/had04",
                               encoding="UTF-8")

app = Flask(__name__)


@app.route('/rx', methods=['POST'])
def rx():
    source = create(push_tokens)
    print("before")
    source.subscribe(
        on_next = lambda i: print("Received {0}".format(i)),
        on_error = lambda e: print("Error Occurred: {0}".format(e)),
        on_completed = lambda: print("Done!"),
    )

    print("after")
    return jsonify({"success": True})

def push_tokens(observer, scheduler):
    observer.on_next("1VGTeO50GN6K")
    observer.on_next("BaGQxlRcHJGduqCz")
    observer.on_next("6uvaAY1EvY84")
    observer.on_next("Ta7Woi5gxiMr")
    observer.on_next("aUpWXkHV2ogJ")
    observer.on_completed()


@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    token = data['token']
    
    return get_seller_info(token)


def get_seller_info(token):
    cursor = connection.cursor()
    sql = """
            SELECT 
                ID_SELLER, NAM_STATUS
            FROM
                API_FRONT.APIF_AUTH_TOKEN aat 
            WHERE
                ID_STORE = 'NCMP' 
            AND 
                ID_AUTH_TOKEN = :token """

    cursor.execute(sql, token=token)
    row = cursor.fetchone()

    return jsonify({'seller_id': row[0], 'status': row[1]})

if __name__ == "__main__":
    app.run(debug=True)
