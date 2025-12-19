from flask import Blueprint, jsonify
from ..models import db

sources_bp = Blueprint("sources_bp", __name__)

# Endpoint to get all sources for a specific artist
@sources_bp.get("/<int:artist_id>/sources")
def get_artist_sources(artist_id):
    # Using raw SQL (works fine with MSSQL + SQLAlchemy engine)
    sql = """
        SELECT
            s.ArtistSourceId,
            st.Name AS SourceName,
            st.Code AS SourceCode,
            s.DisplayName,
            s.Url,
            s.Handle,
            s.IsPrimary
        FROM ArtistSources s
        INNER JOIN SourceTypes st ON st.SourceTypeId = s.SourceTypeId
        WHERE s.ArtistId = :artist_id
        ORDER BY s.IsPrimary DESC, st.Name ASC;
    """

    rows = db.session.execute(db.text(sql), {"artist_id": artist_id}).mappings().all()

    result = []
    for r in rows:
        result.append({
            "id": r["ArtistSourceId"],
            "sourceName": r["SourceName"],
            "sourceCode": r["SourceCode"],
            "displayName": r["DisplayName"],
            "url": r["Url"],
            "handle": r["Handle"],
            "isPrimary": bool(r["IsPrimary"])
        })

    return jsonify(result)
