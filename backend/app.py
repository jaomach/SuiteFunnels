from flask import Flask, request, jsonify, session, url_for, redirect, render_template, render_template_string, send_from_directory
import jwt
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
import time
import os

#jwtKey = os.environ['JWT_SECRET_KEY']
jwtKey = '123'

DELAY_BASE = 1
MAX_ATTEMPTS = 5
DELAY_MULTIPLIER = 2

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'funnels',
    'port': 3306
}

#função para conectar no banco de dados
def connect_to_db():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def generate_jwt_token(id, username):
    expiration = datetime.now(timezone.utc) + timedelta(days=30)
    
    expiration_timestamp = expiration.timestamp()

    payload = {
        'id': id,
        'username': username,
        'exp': expiration_timestamp
    }

    token = jwt.encode(payload, jwtKey, algorithm='HS256')
    return token

def verify_jwt_token(token):
    try:
        decoded_payload = jwt.decode(token, jwtKey, algorithms=['HS256'])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def generate_token_cliente(cliente):
    payload = {
        'cliente': cliente
    }
    token = jwt.encode(payload, jwtKey, algorithm='HS256')
    return token

def authorize(tokenA, tokenB):
    print(tokenA)
    print(tokenB)
    #clientes da agência
    clientes = checarClientes(tokenA['id'], True)
    print(clientes)
    finded = False

    for cliente in clientes:
            if finded == False:
                if cliente[0] == tokenB:
                    finded = True
    return finded

@app.route('/api/token_check')
def token_check():
    token = None
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]
    
    if not token:
        return jsonify({'valid': False, 'message': 'Token não fornecido'}), 403
    else:
        response = verify_jwt_token(token)
        if response:
            return jsonify({'valid': True, 'message': 'Token válido', 'username': response['username']}), 200
        else:
            return jsonify({'valid': False, 'message': 'Token invalido'}), 403

@app.route('/api/check_cliente')
def check_cliente():
    if 'Authorization' in request.headers:
        tokens = request.headers['Authorization'].split(" ")
        if len(tokens) < 2:
            return jsonify({'message': 'Token malformado'}), 400
        
        token_agencia = tokens[1]  # O token que veio do cookie
        token_cliente = tokens[2]  # O token que veio da URL
        print(token_agencia)
        print(token_cliente)
        
        try:
            connection = connect_to_db()
            if connection is not None:
                token = request.cookies.get('token')
                if token:
                    payload = jwt.decode(token_cliente, jwtKey, algorithms=['HS256'])
                    token_agencia = jwt.decode(token_agencia, jwtKey, algorithms=['HS256'])
                    cliente = payload['cliente']
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM clientes WHERE id = %s", (cliente,))
                    user = cursor.fetchone()
                    cursor.execute("SELECT nome FROM clientes WHERE id = %s", (cliente,))
                    nome = cursor.fetchone()[0]
                    print(nome)
                    authorized = authorize(token_agencia, cliente)
                    if user and authorized == True:
                        return jsonify({'valid': True, 'message': 'Token válido', 'username_cliente': nome}), 200
                    else:
                        return jsonify({'message': 'User not found'}), 404
                else:
                    return redirect(url_for('index'))
            else:
                return jsonify({'message': 'Database connection error'}), 500
        except Error as e:
            return jsonify({'message': f'Error fetching user information: {e}'}), 500
        finally:
            if connection:
                connection.close()

def checarClientes(agencia_id, decoded):
    try:
        connection = connect_to_db()
        if not connection:
            raise Exception("Failed to connect to the database")

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM clientes WHERE agencias_id = %s", (agencia_id,))
        clientes = cursor.fetchall()
    
        cursor.execute("SELECT nome FROM agencias WHERE id = %s", (agencia_id,))
        agencia = cursor.fetchone()
        agencia = agencia[0]

        clientes_modificados = []

        if decoded == True:
            for cliente in enumerate(clientes):
                cliente = list(cliente)
        else: 
            for cliente in clientes:
                cliente_lista = list(cliente)
                token_cliente = generate_token_cliente(cliente_lista[0])
                cliente_lista.insert(0, token_cliente)
                clientes_modificados.append(tuple(cliente_lista))
                retorno_final = [(0, agencia)] + clientes_modificados
                print(retorno_final)
            
        if decoded == False:
            return retorno_final
        else:
            return clientes
    except Exception as e:
        print(f"Erro ao checar clientes: {e}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # transforma a senha em um hash seguro
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    print(hashed_password)
    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM agencias WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({'message': 'E-mail já está em uso'}), 400
            else:
                cursor.execute("INSERT INTO agencias (nome, email, senha) VALUES (%s, %s, %s)", (username, email, hashed_password))
                connection.commit()
                return jsonify({'message': 'Usúario cadastrado com sucesso'}), 200
        else:
            return jsonify({'message': 'Erro de conexão com o banco de dados'}), 500
    except Error as e:
        return jsonify({'message': f'Erro ao registrar usuário: {e}'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/call_pipelines', methods=['GET'])
def call_pipeline():
    if 'Authorization' in request.headers:
        token = verify_jwt_token(request.headers['Authorization'].split(" ")[1])

        try:
            connection = connect_to_db()
            if connection is not None:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM pipeline WHERE clientes_id = %s", (token['cliente'],))
                pipelines = cursor.fetchall()
                
                return jsonify({'pipelines': pipelines})
            else:
                return jsonify({'message': f'Erro de conexão com o banco de dados'})

            cursor = connection.cursor()

        except Exception as e:
            print(f"Erro ao checar clientes: {e}")
            return []
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    delay = DELAY_BASE

    try:
        connection = connect_to_db()
        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM agencias WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                if check_password_hash(user[3], password):
                    token = generate_jwt_token(user[0], user[1])
                    time.sleep(delay)
                    return jsonify({'token': token}), 200
                else:
                    delay *= DELAY_MULTIPLIER
                    time.sleep(delay)
                    return jsonify({'message': 'Invalid email or password'}), 401
            else:
                delay *= DELAY_MULTIPLIER
                time.sleep(delay)
                return jsonify({'message': 'User not found'}), 404
        else:
            delay *= DELAY_MULTIPLIER
            time.sleep(delay)
            return jsonify({'message': 'Database connection error'}), 500
    except Error as e:
        delay *= DELAY_MULTIPLIER
        time.sleep(delay)
        return jsonify({'message': f'Error logging in: {e}'}), 500
    finally:
        if connection:
            connection.close()

@app.route('/api/call_clientes', methods=['GET'])
def call_clientes():
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(" ")[1]

    decodedToken = verify_jwt_token(token)
    clientes = checarClientes(decodedToken.get('id'), False)

    return jsonify({'clientes': clientes})



if __name__ == '__main__':
    app.run(debug=True)