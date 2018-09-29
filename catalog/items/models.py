from catalog import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'category_id': self.category_id}
