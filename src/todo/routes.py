from flask import jsonify
from flask import request
from todo import app
from todo import Db as db

@app.route('/', methods=['GET'])
def index():
  db.create_task_table()
  return jsonify({ 'hello': 'world' })

@app.route('/tasks', methods=['POST'])
def add():
  out_put = db.add_task(request.form)
  return jsonify(out_put)

@app.route('/tasks', methods=['GET'])
def get():
  out_put = db.get_all_tasks()
  return jsonify(out_put)

@app.route('/tasks', methods=['DELETE'])
def delete():
  out_put = db.delete_task(request.form)
  return jsonify(out_put)

@app.route('/tasks/all', methods=['DELETE'])
def delete_all():
  db.delete_all_tasks()
  return jsonify('success')

@app.route('/tasks/name', methods=['GET'])
def get_in_name():
  out_put = db.get_in_name(request.form)
  return jsonify(out_put)

@app.route('/tasks/tag', methods=['GET'])
def get_in_tag():
  out_put = db.get_in_tag(request.form)
  return jsonify(out_put)