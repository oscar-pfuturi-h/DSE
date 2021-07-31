from flask import Flask,render_template,request,redirect
from models import db,EmployeeModel
from flask_language import Language, current_language
from flask import jsonify
import datetime

app = Flask(__name__)
lang = Language()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['LANGUAGE_COOKIE_TIMEOUT'] = 2
app.config['LANGUAGE_COOKIE_NAME'] = 'lang_server'
db.init_app(app)
lang.init_app(app)


@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/create' , methods = ['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        employee_id = request.form['employee_id']
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        employee = EmployeeModel(employee_id=employee_id, name=name, age=age, position = position)
        db.session.add(employee)
        db.session.commit()
        return redirect('/data')

 
@app.route('/data')
def RetrieveList():
    employees = EmployeeModel.query.all()
    return render_template('datalist.html',employees = employees)

 
@app.route('/data/<int:id>')
def RetrieveEmployee(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if employee:
        return render_template('data.html', employee = employee)
    return f"Employee with id ={id} Doesnt exist"


@app.route('/data/<int:id>/update',methods = ['GET','POST'])
def update(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            name = request.form['name']
            age = request.form['age']
            position = request.form['position']
            employee = EmployeeModel(employee_id=id, name=name, age=age, position = position)
            db.session.add(employee)
            db.session.commit()
            return redirect(f'/data/{id}')
        return f"Employee with id = {id} Does not exist"
 
    return render_template('update.html', employee = employee)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    employee = EmployeeModel.query.filter_by(employee_id=id).first()
    if request.method == 'POST':
        if employee:
            db.session.delete(employee)
            db.session.commit()
            return redirect('/data')


    return render_template('delete.html')


@lang.allowed_languages
def get_allowed_languages():
    return ['en', 'es']

@lang.default_language
def get_default_language():
    return 'es'

@app.route('/api/language')
def get_language():
    return jsonify({
        'language': str(current_language),
    })

@app.route('/api/language', methods=['POST'])
def set_language():
    req = request.get_json()
    language = req.get('language', None)

    lang.change_language(language)
    return jsonify({
        'language': str(current_language),
    })

app.run(debug=True, host='localhost', port=5000)
