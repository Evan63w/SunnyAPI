from flask import Flask, jsonify
from flask_cors import CORS
import pyodbc

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database configuration for Azure SQL Database
server = 'sunnysense2.database.windows.net'
database = 'sunnysense2'
username = 'dimitri'
password = 'password1!'
driver = '{ODBC Driver 18 for SQL Server}'

# API route to get data from the database
@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Establish a connection to the Azure SQL Database
        conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = conn.cursor()

        # Perform the SQL query
        query = "SELECT TOP 1 * from data ORDER BY EventProcessedUtcTime DESC"
        cursor.execute(query)

        # Fetch all the rows
        rows = cursor.fetchall()

        # Prepare the response as a list of dictionaries
        data = []
        for row in rows:
            record = {
                'temp': row.temperature,
                'humidity': row.humidity,
                'uvindex': row.uvIndex
                # Add more columns as needed
            }
            data.append(record)

        # Close the database cursor and connection
        cursor.close()
        conn.close()

        # Return the data as a JSON response
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/dataavg', methods=['GET'])
def get_dataavg():
    try:
        # Establish a connection to the Azure SQL Database
        conn = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
        cursor = conn.cursor()

        # Perform the SQL query
        query = "SELECT TOP 10 * from data ORDER BY EventProcessedUtcTime DESC"
        cursor.execute(query)

        # Fetch all the rows
        rows = cursor.fetchall()

        # Prepare the response as a list of dictionaries
        data = []
        le = len(rows)
        temp = 0 
        humidity = 0
        uvindex = 0
        for row in rows:
            temp += row.temperature
            humidity += row.humidity
            uvindex += row.uvIndex
        temp /= le
        humidity /= le
        uvindex /= le
        temp = round(temp, 2)
        humidity = round(humidity,1)
        uvindex = round(uvindex,1)
        record = {
                'temp': temp,
                'humidity': humidity,
                'uvindex': uvindex 
            }
        data.append(record)

        # Close the database cursor and connection
        cursor.close()
        conn.close()

        # Return the data as a JSON response
        return jsonify(data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
