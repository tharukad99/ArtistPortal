from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import check_password_hash
from sqlalchemy import text
from artistportal import db
from artistportal.models import User
from artistportal.models import User1

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("manage_artists_page"))
    return render_template("login.html")


@auth_bp.post("/login")
def login_post():
    username = (request.form.get("username") or "").strip()
    password = request.form.get("password") or ""


    sql = text("""
        SELECT UserId, Username, PasswordHash, IsActive, ArtistId, DisplayName, IsAdmin
        FROM dbo.PortalUsers
        WHERE Username = :username
    """)

    result = db.session.execute(sql, {"username": username}).fetchone()

    # 1️⃣ User not found
    if not result:
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login"))

    # 2️⃣ Password verification
    if not check_password_hash(result.PasswordHash, password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login"))

    user = User1(
        UserId=result.UserId,
        Username=result.Username,
        PasswordHash=result.PasswordHash,
        DisplayName=result.DisplayName,
        # Email=result.Email,
        IsAdmin=result.IsAdmin,
        IsActive=result.IsActive,
        ArtistId=result.ArtistId
    )
    
    # 4️⃣ Login (session creation)
    login_user(user)


    if user.IsAdmin == 1:
        return redirect(url_for("auth.manage_artists_page"))
    return redirect(url_for("manage_home_page", artist_id=user.ArtistId))


@auth_bp.get("/logout")
def logout():
    logout_user()
    # return redirect(url_for("artist_list_page"))
    return redirect(url_for("auth.login"))


@auth_bp.get("/admin/manage-artists")
@login_required
def manage_artists_page():
    # only admin
    if int(getattr(current_user, "IsAdmin", 0)) != 1:
        return redirect(url_for("auth.login"))  # or abort(403)
    return render_template("manage_artists.html")
