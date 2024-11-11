from  flask import Flask, render_template, request, redirect, url_for
from models import db, Item

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db.init_app(app)

with app.app_context():
    db.create_all()
    
    
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        new_item = Item(name=name, description=description)
        
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.description = request.form['description']
        
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>')
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('index'))
