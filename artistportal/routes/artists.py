from flask import Blueprint, jsonify
from ..models import Artist
from ..models import db
from sqlalchemy import text

artists_bp = Blueprint("artists", __name__)

# Get list of active artists
@artists_bp.get("/")
def list_artists():
    sql = text("EXEC dbo.ListActiveArtists")
    rows = db.session.execute(sql).mappings().all()

    return jsonify([
        {
            "id": r["ArtistId"],
            "stageName": r["StageName"],
            "profileImageUrl": r["ProfileImageUrl"]
        }
        for r in rows
    ])

# Get details of a specific artist
@artists_bp.get("/<int:artist_id>")
def get_artist(artist_id):
    sql = text("EXEC dbo.sp_GetArtistById @ArtistId=:artist_id")
    row = db.session.execute(sql, {"artist_id": artist_id}).mappings().first()

    if not row:
        return jsonify({"error": "Artist not found"}), 404

    return jsonify({
        "id": row["ArtistId"],
        "stageName": row["StageName"],
        "fullName": row["FullName"],
        "bio": row["Bio"],
        "profileImageUrl": row["ProfileImageUrl"],
        "country": row["Country"],
        "primaryGenre": row["PrimaryGenre"],
        "websiteUrl": row["WebsiteUrl"],
        "sourcesCount": int(row["SourcesCount"] or 0)
    })

# Get photos of a specific artist
@artists_bp.get("/<int:artist_id>/photos")
def get_artist_photos(artist_id):
    sql = """
        SELECT
            PhotoUrl,
            Caption
        FROM ArtistPhotos
        WHERE ArtistId = :artist_id
        ORDER BY SortOrder ASC, DateCreated DESC;
    """
    rows = db.session.execute(
        text(sql),
        {"artist_id": artist_id}
    ).mappings().all()

    result = []
    for r in rows:
        result.append({
            "url": r["PhotoUrl"],
            "caption": r["Caption"]
        })

    return jsonify(result)