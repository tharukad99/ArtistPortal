from flask_login import UserMixin
from . import db  # or from ..models import db depending your structure

class PortalUser(db.Model, UserMixin):
    __tablename__ = "PortalUsers"

    UserId = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(100), unique=True, nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)
    DisplayName = db.Column(db.String(150))
    Email = db.Column(db.String(150))
    IsAdmin = db.Column(db.Boolean, default=False)
    IsActive = db.Column(db.Boolean, default=True)
    DateCreated = db.Column(db.DateTime)

    # Flask-Login expects id property
    def get_id(self):
        return str(self.UserId)

    @property
    def is_admin(self):
        return bool(self.IsAdmin)

    @property
    def is_active(self):
        return bool(self.IsActive)
