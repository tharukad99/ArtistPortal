# artistportal/routes/metrics.py
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from ..models import db, ArtistMetric, MetricType

metrics_bp = Blueprint("metrics", __name__)

# @metrics_bp.get("/summary/<int:artist_id>")
# def summary_metrics(artist_id):
#     # Metric types we care about for cards
#     codes = ["followers", "views", "streams", "tickets"]

#     metric_types = MetricType.query.filter(MetricType.Code.in_(codes)).all()
#     type_by_id = {mt.MetricTypeId: mt for mt in metric_types}

#     sub = (
#         db.session.query(
#             ArtistMetric.MetricTypeId,
#             func.max(ArtistMetric.MetricDate).label("MaxDate")
#         )
#         .filter(ArtistMetric.ArtistId == artist_id,
#                 ArtistMetric.MetricTypeId.in_(type_by_id.keys()))
#         .group_by(ArtistMetric.MetricTypeId)
#         .subquery()
#     )

#     rows = (
#         db.session.query(ArtistMetric)
#         .join(sub,
#               (ArtistMetric.MetricTypeId == sub.c.MetricTypeId) &
#               (ArtistMetric.MetricDate == sub.c.MaxDate))
#         .all()
#     )

#     data = {}
#     for r in rows:
#         code = type_by_id[r.MetricTypeId].Code
#         data[code] = float(r.Value)

#     return jsonify(data)



from flask import jsonify, current_app
from sqlalchemy import text

@metrics_bp.get("/summary/<int:artist_id>")
def summary_metrics(artist_id):
    try:
        result = db.session.execute(
            text("EXEC dbo.GetArtistSummaryMetrics :artist_id"),
            {"artist_id": artist_id}
        )

        rows = result.fetchall()   # list of tuples: (Code, Value)

        data = {}
        for code, value in rows:
            # Guard against NULLs
            data[code] = float(value) if value is not None else None

        return jsonify(data)

    except Exception as e:
        # Log the real error so you can see what SQL / driver is complaining about
        current_app.logger.exception("Error in summary_metrics")
        return jsonify({"error": "Internal Server Error"}), 500


##========================================11111111111111111111111111111111111111111

# @metrics_bp.get("/timeseries/<int:artist_id>")
# def timeseries_metrics(artist_id):
#     metric_code = request.args.get("metric", "followers")  # default
#     metric_type = MetricType.query.filter_by(Code=metric_code).first_or_404()

#     rows = (
#         ArtistMetric.query
#         .filter_by(ArtistId=artist_id, MetricTypeId=metric_type.MetricTypeId)
#         .order_by(ArtistMetric.MetricDate)
#         .all()
#     )

#     return jsonify([
#         {
#             "date": r.MetricDate.strftime("%Y-%m-%d"),
#             "value": float(r.Value)
#         } for r in rows
#     ])


from flask import request, jsonify, current_app
from sqlalchemy import text

@metrics_bp.get("/timeseries/<int:artist_id>")
def timeseries_metrics(artist_id):
    # default metric is still picked in backend; the *data logic* is in SQL
    metric_code = request.args.get("metric", "followers")

    try:
        result = db.session.execute(
            text("""
                EXEC dbo.GetArtistMetricTimeSeries 
                    @ArtistId = :artist_id,
                    @MetricCode = :metric_code
            """),
            {
                "artist_id": artist_id,
                "metric_code": metric_code
            }
        )

        rows = result.fetchall()   # list of tuples: (MetricDate, Value)

        data = []
        for metric_date, value in rows:
            # metric_date is a datetime/date object from SQLAlchemy
            data.append({
                "date": metric_date.strftime("%Y-%m-%d"),
                "value": float(value) if value is not None else None
            })

        return jsonify(data)

    except Exception as e:
        current_app.logger.exception("Error in timeseries_metrics")
        return jsonify({"error": "Internal Server Error"}), 500
