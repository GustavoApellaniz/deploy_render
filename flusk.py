import mysql.connector
from flask import Flask, jsonify, request
from dotenv import load_dotenv, dotenv_values
import os

load_dotenv()

app = Flask(__name__)

con = mysql.connector.connect(
    host = os.getenv('host'), 
    database = os.getenv('database'), 
    user = os.getenv('user'),                                                          
    password = os.getenv('password'),
    ssl_disabled=False)

@app.route('/post_student', methods = ['POST'])
def post_student():
    data = request.get_json()
    name = data.get('nome')
    stats = data.get('stats')
    cur = con.cursor()
    query = 'insert into shadows(nome , stats) values ( %s, %s )'
    cur.execute(query, (name, stats))
    con.commit()
    cur.close()
    return jsonify({'message':'posted'}), 200


@app.route('/get_student', methods = ['GET'])
def get_student():
    cur = con.cursor(dictionary=True)
    cur.execute('select * from shadows')
    row = cur.fetchall()
    cur.close
    return jsonify(row)


@app.route('/idshare/<int:id>', methods = ['GET'])
def id_get(id):
    cur = con.cursor(dictionary=True)
    cur.execute('select * from shadows where id =  %s',(id,))
    row = cur.fetchone()
    cur.close
    return jsonify(row)

@app.route('/upd_name', methods = ["PUT"])
def upd_name():
    data = request.get_json()
    id = data.get('id') 
    nome = data.get('nome') 
    stats = data.get('stats') 
    cur = con.cursor()
    query = 'update shadows set nome = %s, stats = %s where id = %s '
    cur.execute(query, (nome, stats, id))
    con.commit()
    cur.close()
    return jsonify({'update' : 'done'})

@app.route('/deleteid/<int:id>', methods = ['DELETE'] )
def deleteid(id):
    cur = con.cursor()
    query = 'delete from shadows where id = %s'
    cur.execute(query, (id,))
    con.commit()
    cur.close()
    return jsonify({'message' : 'delete'}), 200


@app.route('/postlist', methods = ['POST'])
def post_list():
    reqData =request.json
    cursor = con.cursor()
    query = "INSERT INTO shadows (nome, stats) VALUES (%s, %s)"
    for student in reqData:
        name = student.get('nome')
        mark = student.get('stats')
        cursor.execute(query, (name, mark))
    con.commit()
    cursor.close()
    return jsonify({'kill':"myself"})

@app.route('/')
def index():
    return 'hello world'


if __name__ == '__main__':
    app.run(debugger = True, port = 8090)

