from flask import Flask, jsonify, send_from_directory, request
import pyodbc 
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

app = Flask(__name__)

# Get the absolute path to the frontend directory
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend'))
print(f"Frontend directory path: {FRONTEND_DIR}")

server= os.getenv('DB_SERVER')
database = os.getenv('DB_NAME')
username = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD') 
driver= os.getenv('DB_DRIVER') 

# Connecting string 
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Encrypt=no;'

def query_db(query, params=None):
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if query.strip().upper().startswith("SELECT"):
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
        else:
            conn.commit()
            results = {'message': 'Query executed successfully'}
        conn.close()
        return results
    except Exception as e:
        return {'error': str(e)}
        
@app.route('/')
def home():
    try:
        # Use absolute path to find index.html
        if os.path.exists(os.path.join(FRONTEND_DIR, 'index.html')):
            return send_from_directory(FRONTEND_DIR, 'index.html')
        else:
            return "Frontend files not found. Check directory structure.", 404
    except Exception as e:
        print(f"Error serving index.html: {str(e)}")
        return str(e), 404

@app.route('/<path:path>')
def static_files(path):
    try:
        if os.path.exists(os.path.join(FRONTEND_DIR, path)):
            return send_from_directory(FRONTEND_DIR, path)
        else:
            return f"File {path} not found", 404
    except Exception as e:
        print(f"Error serving {path}: {str(e)}")
        return str(e), 404

# ------- Owners ---------# 

@app.route('/owners', methods=['GET'])
def get_owners():
    query = "SELECT * FROM Owners"
    return jsonify(query_db(query))

# -------- Pets --------- # 

@app.route('/pets', methods=['GET'])
def get_pets():
    query = """
    SELECT p.pet_id, p.pet_name, p.species, p.breed, 
           o.first_name + ' ' + o.last_name AS owner_name, o.email AS owner_email, o.phone_number AS owner_phone
    FROM Pets p
    JOIN Owners o ON p.owner_id = o.owner_id
"""
    return jsonify(query_db(query))
    
# --------- Vets ---------- #

@app.route('/vets', methods=['GET'])
def get_vets():
    query = "SELECT * FROM Vets"
    return jsonify(query_db(query))         

# ------- Appointments ---------#

@app.route('/appointments', methods=['GET'])
def get_appointments():
    query = """
    SELECT a.appointment_id, p.pet_name, v.first_name + ' ' + v.last_name AS vet_name,
           a.date_time, a.reason, o.first_name + ' ' + o.last_name AS owner_name, v.speciality
    FROM Appointments a
    JOIN Pets p ON a.pet_id = p.pet_id
    JOIN Vets v ON a.vet_id = v.vet_id
    JOIN Owners o ON p.owner_id = o.owner_id
    ORDER BY a.date_time DESC
    """
    return jsonify(query_db(query))

# ------- new appointment ---------#

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    query = """
    INSERT INTO Appointments (pet_id, vet_id, date_time, reason)
    VALUES (?, ?, ?, ?)
    
    """

    params = (data['pet_id'], data['vet_id'], data['date_time'], data['reason'])
    result = query_db(query, params)
    print(f"Add appointment result: {result}")
    return jsonify(result)

# -------- Prescription -------- # 

@app.route('/prescription', methods=['GET'])
def get_prescriptions():
    query = """
        SELECT pr.prescription_id, pr.item_name, pr.quantity, pr.unit_price, pr.instruction,
               m.record_id, m.diagnosis, m.treatment, p.pet_name AS pet_name, 
               v.first_name + ' ' + v.last_name AS vet_name
        FROM Prescription pr
        JOIN Medical_Records m ON pr.record_id = m.record_id
        JOIN Appointments a ON m.appointment_id = a.appointment_id
        JOIN Pets p ON a.pet_id = p.pet_id
        JOIN Vets v ON a.vet_id = v.vet_id
    """
    return jsonify(query_db(query))

@app.route('/prescription', methods=['POST'])
def add_prescription():
    data = request.json
    query = """
    INSERT INTO Prescription (record_id, item_name, quantity, unit_price, instruction)
    VALUES (?, ?, ?, ?)
    """
    params = (data['record_id'], data['item_name'], data['quantity'], data['unit_price'], data['instruction'])
    return jsonify(query_db(query, params))


# --------- Medical Records ----------------- # 

@app.route('/medical-records', methods=['GET'])
def get_medical_records():
    query = """
    SELECT m.record_id, m.diagnosis, m.treatment, m.notes, m.billing_amount,
           a.appointment_id, a.reason,
           p.pet_name AS pet_name, v.first_name + ' ' + v.last_name AS vet_name
    FROM Medical_Records m
    JOIN Appointments a ON m.appointment_id = a.appointment_id
    JOIN Pets p ON a.pet_id = p.pet_id
    JOIN Vets v ON a.vet_id = v.vet_id
    """
    return jsonify(query_db(query))

@app.route('/medical-records', methods=['POST'])
def add_medical_record():
    data = request.json
    query = """
    INSERT INTO Medical_Records (appointment_id, diagnosis, treatment, notes, billing_amount)
    VALUES (?, ?, ?, ?, ?)
    """
    params = (data['appointment_id'], data['diagnosis'], data['treatment'], data['notes'], data['billing_amount'])
    return jsonify(query_db(query, params))

# --------- Search Appointments --------- 
 
@app.route('/appointments/search')
def search_appointments():
    try:
        pet_name = request.args.get('pet_name', '')
        
        # Query database for matching appointments by pet name
        query = """
        SELECT a.appointment_id, p.pet_name, v.first_name + ' ' + v.last_name AS vet_name,
               a.date_time, a.reason, o.first_name + ' ' + o.last_name AS owner_name, v.speciality
        FROM Appointments a
        JOIN Pets p ON a.pet_id = p.pet_id
        JOIN Vets v ON a.vet_id = v.vet_id
        JOIN Owners o ON p.owner_id = o.owner_id
        WHERE p.pet_name LIKE ?
        ORDER BY a.date_time DESC
        """
        params = [f"%{pet_name}%"]
            
        return jsonify(query_db(query, params))
    except Exception as e:
        return jsonify({'error': str(e)})

# --- health check ----- # 

@app.route('/health')
def health():
    return jsonify({'status': 'OK', "db": database}) 


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 
    
    