from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.get("/manage-artists")
@login_required
def manage_artists_page():
    # If not admin -> block
    if int(getattr(current_user, "IsAdmin", 0)) != 1:
        return redirect(url_for("auth.login"))  # or abort(403)

    return render_template("manage_artists.html")