from flask import Flask,render_template,request,redirect,make_response
from models import db,PersonModel
from flask_language import Language, current_language
from flask import jsonify
from simplexml import dumps
from flask_restful import Api, Resource

app = Flask(__name__)
lang = Language()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['LANGUAGE_COOKIE_TIMEOUT'] = 2
app.config['LANGUAGE_COOKIE_NAME'] = 'lang_server'
db.init_app(app)
lang.init_app(app)

def output_xml(data,code,headers=None):
    """Makes a Flask response with a XML encoded body"""
    resp = make_response(dumps({'response': data}), code)
    resp.headers.extend(headers or {})
    return resp

api = Api(app,default_mediatype='application/xml')
api.representations['application/xml']=output_xml
@api.representation('application/xml')

@app.before_first_request
def create_table():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data/create', methods=['GET','POST'])
def create():
    if request.method == 'GET':
        return render_template('createpage.html')

    if request.method == 'POST':
        dni = request.form['dni']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        age = request.form['age']
        cellphone = request.form['cellphone']
        address = request.form['address']
        person = PersonModel(dni=dni, first_name=first_name, last_name=last_name, age=age, cellphone=cellphone, address=address)
        db.session.add(person)
        db.session.commit()
        return redirect('/data')

 
@app.route('/data', methods=['GET'])
def RetrieveList():
    #people = PersonModel.query.all()
    #return render_template('datalist.html',people=people)
    people = [person.json() for person in PersonModel.query.all()]
    return jsonify({'people': people})

 
@app.route('/data/<int:id>', methods=['GET'])
def Retrieveperson(id):
    person = PersonModel.query.filter_by(id=id).first()
    if person:
        #return render_template('data.html', person=person)
        return jsonify({'person': person.json()})
    return f"person with ID = {id} Doesnt exist"


@app.route('/data/<int:id>/update', methods=['GET','POST'])
def update(id):
    person = PersonModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if person:
            db.session.delete(person)
            db.session.commit()
            dni = request.form['dni']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            age = request.form['age']
            cellphone = request.form['cellphone']
            address = request.form['address']
            person = PersonModel(dni=dni, first_name=first_name, last_name=last_name, age=age, cellphone=cellphone, address=address)
            db.session.add(person)
            db.session.commit()
            return redirect(f'/data/{person.id}')
        return f"person with ID = {person.id} Does not exist"
 
    return render_template('update.html', person=person)


@app.route('/data/<int:id>/delete', methods=['GET','POST'])
def delete(id):
    person = PersonModel.query.filter_by(id=id).first()
    if request.method == 'POST':
        if person:
            db.session.delete(person)
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

class call(Resource):
    
    def get(self):
        people = [person.json() for person in PersonModel.query.all()]
        return {'people': people}
    #def get(self, entry):
    #    return {'hello': entry}

api.add_resource(call,'/api')

if __name__=='__main__':
    app.run(debug=True, host='localhost', port=5000)
