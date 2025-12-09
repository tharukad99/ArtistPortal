# artistportal/routes/artists.py
from flask import Blueprint, jsonify
from ..models import Artist

artists_bp = Blueprint("artists", __name__)

@artists_bp.get("/")
def list_artists():
    artists = Artist.query.filter_by(IsActive=True).all()
    return jsonify([
        {
            "id": a.ArtistId,
            "stageName": a.StageName,
            "profileImageUrl": a.ProfileImageUrl,
        } for a in artists
    ])


from flask import Blueprint, jsonify, abort
from ..models import Artist, ArtistSource

@artists_bp.get("/<int:artist_id>")
def get_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)

    return jsonify({
        "id": artist.ArtistId,
        "stageName": artist.StageName,
        "fullName": artist.FullName,
        "bio": artist.Bio,
        "profileImageUrl": artist.ProfileImageUrl,
        "country": artist.Country,
        "primaryGenre": artist.PrimaryGenre,
        "websiteUrl": artist.WebsiteUrl
    })


@artists_bp.get("/<int:artist_id>/sources")
def get_artist_sources(artist_id):
    Artist.query.get_or_404(artist_id)

    sources = ArtistSource.query.filter_by(ArtistId=artist_id).all()
    return jsonify([
        {
            "id": s.ArtistSourceId,
            "type": s.source_type.Name,
            "typeCode": s.source_type.Code,
            "url": s.Url,
            "handle": s.Handle,
            "isPrimary": s.IsPrimary
        } for s in sources
    ])


