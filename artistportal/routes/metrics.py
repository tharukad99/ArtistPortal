# artistportal/routes/metrics.py
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from ..models import db, ArtistMetric, MetricType
from flask import jsonify, current_app
from sqlalchemy import text

metrics_bp = Blueprint("metrics", __name__)

# Summary Metrics Endpoint
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

# Time Series Metrics Endpoint
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
