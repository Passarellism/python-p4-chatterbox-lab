from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
# import ipdb

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
        response = make_response(
            messages,
            200
        )
        return response
    elif request.method == 'POST':
        # ipdb.set_trace()
        new_message = Message(
            body = request.get_json()['body'],
            username = request.get_json()['username']
        )
        db.session.add(new_message)
        db.session.commit()
        
        response_body = new_message.to_dict()
        response = make_response(
            jsonify(response_body), 
            201
        )
        return response

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5555, debug=True)
