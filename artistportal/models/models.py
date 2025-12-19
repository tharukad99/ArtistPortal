# # artistportal/models.py
# from ..routes import db
# from datetime import datetime

# class Artist(db.Model):
#     __tablename__ = "Artists"

#     ArtistId = db.Column(db.Integer, primary_key=True)
#     StageName = db.Column(db.String(150), nullable=False)
#     FullName = db.Column(db.String(200))
#     Bio = db.Column(db.Text)
#     ProfileImageUrl = db.Column(db.String(500))
#     Country = db.Column(db.String(100))
#     PrimaryGenre = db.Column(db.String(100))
#     WebsiteUrl = db.Column(db.String(500))
#     DateCreated = db.Column(db.DateTime, default=datetime.utcnow)
#     IsActive = db.Column(db.Boolean, default=True)
#     SourcesCount = db.Column(db.Integer)

#     sources = db.relationship("ArtistSource", backref="artist", lazy=True)
#     activities = db.relationship("Activity", backref="artist", lazy=True)
#     metrics = db.relationship("ArtistMetric", backref="artist", lazy=True)


# class SourceType(db.Model):
#     __tablename__ = "SourceTypes"

#     SourceTypeId = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Code = db.Column(db.String(50), nullable=False, unique=True)
#     IconName = db.Column(db.String(100))

#     artist_sources = db.relationship("ArtistSource", backref="source_type", lazy=True)


# class ArtistSource(db.Model):
#     __tablename__ = "ArtistSources"

#     ArtistSourceId = db.Column(db.Integer, primary_key=True)
#     ArtistId = db.Column(db.Integer, db.ForeignKey("Artists.ArtistId"), nullable=False)
#     SourceTypeId = db.Column(db.Integer, db.ForeignKey("SourceTypes.SourceTypeId"), nullable=False)
#     DisplayName = db.Column(db.String(150))
#     Url = db.Column(db.String(500), nullable=False)
#     Handle = db.Column(db.String(150))
#     IsPrimary = db.Column(db.Boolean, default=False)
#     DateAdded = db.Column(db.DateTime, default=datetime.utcnow)


# class ActivityType(db.Model):
#     __tablename__ = "ActivityTypes"

#     ActivityTypeId = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     IconName = db.Column(db.String(100))


# class Activity(db.Model):
#     __tablename__ = "Activities"

#     ActivityId = db.Column(db.Integer, primary_key=True)
#     ArtistId = db.Column(db.Integer, db.ForeignKey("Artists.ArtistId"), nullable=False)
#     ActivityTypeId = db.Column(db.Integer, db.ForeignKey("ActivityTypes.ActivityTypeId"), nullable=False)
#     Title = db.Column(db.String(200), nullable=False)
#     Location = db.Column(db.String(200))
#     ActivityDate = db.Column(db.Date, nullable=False)
#     Description = db.Column(db.Text)
#     ExternalUrl = db.Column(db.String(500))
#     DateCreated = db.Column(db.DateTime, default=datetime.utcnow)

#     activity_type = db.relationship("ActivityType")


# class MetricType(db.Model):
#     __tablename__ = "MetricTypes"

#     MetricTypeId = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Code = db.Column(db.String(50), nullable=False, unique=True)
#     GroupName = db.Column(db.String(50), nullable=False)
#     Unit = db.Column(db.String(50))


# class Platform(db.Model):
#     __tablename__ = "Platforms"

#     PlatformId = db.Column(db.Integer, primary_key=True)
#     Name = db.Column(db.String(100), nullable=False)
#     Code = db.Column(db.String(50), nullable=False, unique=True)


# class ArtistMetric(db.Model):
#     __tablename__ = "ArtistMetrics"

#     ArtistMetricId = db.Column(db.Integer, primary_key=True)
#     ArtistId = db.Column(db.Integer, db.ForeignKey("Artists.ArtistId"), nullable=False)
#     MetricTypeId = db.Column(db.Integer, db.ForeignKey("MetricTypes.MetricTypeId"), nullable=False)
#     PlatformId = db.Column(db.Integer, db.ForeignKey("Platforms.PlatformId"))
#     MetricDate = db.Column(db.Date, nullable=False)
#     Value = db.Column(db.Numeric(18, 2), nullable=False)
#     DateCreated = db.Column(db.DateTime, default=datetime.utcnow)

#     metric_type = db.relationship("MetricType")
#     platform = db.relationship("Platform")
