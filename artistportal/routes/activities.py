# artistportal/routes/activities.py
from flask import Blueprint, jsonify
from ..models import Activity

activities_bp = Blueprint("activities", __name__)

@activities_bp.get("/artist/<int:artist_id>")
def list_activities(artist_id):
    activities = (
        Activity.query
        .filter_by(ArtistId=artist_id)
        .order_by(Activity.ActivityDate.desc())
        .all()
    )

    return jsonify([
        {
            "id": a.ActivityId,
            "date": a.ActivityDate.strftime("%Y-%m-%d"),
            "title": a.Title,
            "type": a.activity_type.Name,
            "icon": a.activity_type.IconName,
            "location": a.Location,
            "externalUrl": a.ExternalUrl
        } for a in activities
    ])
