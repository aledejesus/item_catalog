from catalog import db


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=True)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(
        db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category')
    app_user_id = db.Column(
        db.Integer, db.ForeignKey('app_user.id'), nullable=False)
    app_user = db.relationship('AppUser')

    def serialize(self):
        """
        Converts object to dictionary

        Arguments:
            - self(Item)

        Returns:
            - dict containing Item properties
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'category_id': self.category_id,
            'app_user_id': self.app_user_id}
