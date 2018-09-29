from catalog import db


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=True)
    items = db.relationship('Item', order_by='Item.id')
