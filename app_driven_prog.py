from flask import Flask, request, jsonify
import cx_Oracle

userpwd = "APIMPINVANTARIO###2022" # Obtain password string from a user prompt or environment variable

connection = cx_Oracle.connect(user="API_MP_INVENTARIO", password=userpwd,
                               dsn="orarac-hlg-db-scan.dc.nova:1521/had04",
                               encoding="UTF-8")

app = Flask(__name__)


@app.route('/', methods=['POST'])
def login():
    data = request.get_json()
    token = data['token']
    
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
