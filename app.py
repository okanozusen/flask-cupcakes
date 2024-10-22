"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template
from models import db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/cupcakes', methods=['GET'])
def get_cupcakes():
    cupcakes = Cupcake.query.all()
    return jsonify(cupcakes=[cupcake.to_dict() for cupcake in cupcakes])

@app.route('/api/cupcakes/<int:id>', methods=['GET'])
def get_cupcake(id):
    cupcake = Cupcake.query.get(id)
    if cupcake is None:
        return jsonify({"error": "Cupcake not found"}), 404
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    data = request.json
    new_cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data.get('image', 'https://tinyurl.com/demo-cupcake')
    )
    db.session.add(new_cupcake)
    db.session.commit()
    return jsonify(cupcake=new_cupcake.to_dict()), 201

@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def update_cupcake(id):
    cupcake = Cupcake.query.get(id)
    if cupcake is None:
        return jsonify({"error": "Cupcake not found"}), 404

    data = request.json
    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.image = data.get('image', cupcake.image)

    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get(id)
    if cupcake is None:
        return jsonify({"error": "Cupcake not found"}), 404

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="Deleted")

if __name__ == '__main__':
    app.run(debug=True)
