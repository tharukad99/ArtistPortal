from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
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

    # ---------- RAW SQL QUERY ----------
    # sql = text("""
    #     SELECT 
    #         UserId,
    #         Username,
    #         PasswordHash,
    #         DisplayName,
    #         Email,
    #         IsAdmin,
    #         IsActive
    #     FROM [dbo].[PortalUsers]
    #     WHERE Username = :username AND IsActive = 1
    # """)

    sql = text("""
        SELECT UserId, Username, PasswordHash, IsActive, ArtistId, DisplayName
        FROM dbo.PortalUsers
        WHERE Username = :username
    """)

    result = db.session.execute(sql, {"username": username}).fetchone()


    #print(result)
    # 1️⃣ User not found
    if not result:
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login"))

    # 2️⃣ Password verification
    if not check_password_hash(result.PasswordHash, password):
        flash("Invalid username or password.", "error")
        return redirect(url_for("auth.login"))

    # 3️⃣ Convert SQL row → User object (IMPORTANT for Flask-Login)
    # user = User(
    #     UserId=result.UserId,
    #     Username=result.Username,
    #     PasswordHash=result.PasswordHash,
    #     DisplayName=result.DisplayName,
    #     Email=result.Email,
    #     IsAdmin=result.IsAdmin,
    #     IsActive=result.IsActive
    # )

    user = User1(
        UserId=result.UserId,
        Username=result.Username,
        PasswordHash=result.PasswordHash,
        DisplayName=result.DisplayName,
        # Email=result.Email,
        # IsAdmin=result.IsAdmin,
        IsActive=result.IsActive,
        ArtistId=result.ArtistId
    )
    
    # 4️⃣ Login (session creation)
    login_user(user)

    if user.ArtistId == 1:
        return redirect(url_for("manage_artists_page"))
    return redirect(url_for("artist_list_page"))


@auth_bp.get("/logout")
def logout():
    logout_user()
    return redirect(url_for("artist_list_page"))



# from flask import jsonify, request
# from sqlalchemy import text
# from werkzeug.security import check_password_hash
# from artistportal import db
# from artistportal.models import User1
# from flask_login import login_user

# from werkzeug.security import generate_password_hash, check_password_hash


# @auth_bp.post("/api/login")
# def api_login():
#     data = request.get_json(silent=True) or {}
#     username = (data.get("username") or "").strip()
#     password = data.get("password") or ""

#     print("LOGIN ATTEMPT username=", repr(username))

#     sql = text("""
#         SELECT UserId, Username, PasswordHash, DisplayName, Email, IsAdmin, IsActive
#         FROM dbo.PortalUsers
#         WHERE Username = :username
#     """)
#     row = db.session.execute(sql, {"username": username}).fetchone()
#     print("DB ROW FOUND?", bool(row))



#     if not row:
#         return jsonify({"success": False, "message": "Invalid username or password"}), 401


#     if not row.IsActive:
#         return jsonify({"success": False, "message": "User is inactive"}), 401

#     ok = check_password_hash(row.PasswordHash, password)

#     if not ok:
#         return jsonify({"success": False, "message": "Invalid username or password"}), 401

#     user = User1(
#         UserId=row.UserId,
#         Username=row.Username,
#         PasswordHash=row.PasswordHash,
#         DisplayName=row.DisplayName,
#         Email=row.Email,
#         IsAdmin=row.IsAdmin,
#         IsActive=row.IsActive
#     )
#     login_user(user)
#     return jsonify({"success": True, "message": "Logged in"})
