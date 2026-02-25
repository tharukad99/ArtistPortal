from datetime import datetime
from ..extensions import db

class SocialAccount(db.Model):
    __tablename__ = "SocialAccounts"
    
    Id = db.Column(db.Integer, primary_key=True)
    ArtistId = db.Column(db.Integer, db.ForeignKey("Artists.ArtistId"), nullable=False)
    Platform = db.Column(db.String(50), nullable=False) # 'facebook', 'instagram'
    PageId = db.Column(db.String(100))
    IgBusinessId = db.Column(db.String(100))
    AccessToken = db.Column(db.Text, nullable=False)
    PageName = db.Column(db.String(200))
    IgHandle = db.Column(db.String(100))
    ExpiresAt = db.Column(db.DateTime)
    LastSync = db.Column(db.DateTime)
    
    artist = db.relationship("Artist", backref=db.backref("social_accounts", lazy=True))

class SocialMetric(db.Model):
    __tablename__ = "SocialMetrics"
    
    Id = db.Column(db.Integer, primary_key=True)
    ArtistId = db.Column(db.Integer, db.ForeignKey("Artists.ArtistId"), nullable=False)
    Platform = db.Column(db.String(50), nullable=False)
    MetricName = db.Column(db.String(100), nullable=False)
    MetricDate = db.Column(db.Date, nullable=False)
    Value = db.Column(db.BigInteger, nullable=False)
    DateCreated = db.Column(db.DateTime, default=datetime.utcnow)

class SocialSyncLog(db.Model):
    __tablename__ = "SocialSyncLogs"
    
    Id = db.Column(db.Integer, primary_key=True)
    ArtistId = db.Column(db.Integer, db.ForeignKey("Artists.ArtistId"), nullable=False)
    Platform = db.Column(db.String(50))
    RunTime = db.Column(db.DateTime, default=datetime.utcnow)
    Status = db.Column(db.String(20)) # 'SUCCESS', 'ERROR'
    Message = db.Column(db.Text)
