from flask import Blueprint, jsonify
from ..models import Activity
from flask import jsonify
from sqlalchemy import text
from ..models import db

activities_bp = Blueprint("activities", __name__)

# Get activities for a specific artist
@activities_bp.get("/artist/<int:artist_id>")
def list_activities(artist_id):
    result = db.session.execute(
        text("EXEC dbo.usp_ListActivitiesByArtist :artist_id"),
        {"artist_id": artist_id}
    )

    rows = result.fetchall()

    return jsonify([
        {
            "id": row.ActivityId,
            "date": row.ActivityDate.strftime("%Y-%m-%d") if row.ActivityDate else None,
            "title": row.Title,
            "type": row.ActivityTypeName,
            "icon": row.IconName,
            "location": row.Location,
            "externalUrl": row.ExternalUrl
        }
        for row in rows
    ])
