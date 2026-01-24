# app.py
from artistportal import create_app
from flask import render_template

app = create_app()

# NEW: artist list page (first page)
@app.route("/")
def auth():
    return render_template("login.html")

@app.route("/artistslist")
def artist_list_page():
    return render_template("artists_list.html")

# DASHBOARD for a specific artist  ← this MUST be named home_page
@app.route("/artist/<int:artist_id>")
def home_page(artist_id):
    return render_template("home.html", artist_id=artist_id)


# Activities page for that artist
@app.route("/artist/<int:artist_id>/activities")
def activities_page(artist_id):
    return render_template("activities.html", artist_id=artist_id)


# Social Media details page for that artist
@app.route("/artist/<int:artist_id>/social")
def social_media_page(artist_id):
    return render_template("social_media.html", artist_id=artist_id)


# Optional: simple 403 page
# @app.errorhandler(403)
# def forbidden(_):
#     return render_template("403.html"), 403


# @app.route("/artists/list")
# def artists_list_page():
#     # show artists
#     return render_template("artists_list.html")

# ✅ NEW: Manage Artists page
@app.route("/admin/manage-artists")
# @admin_required
def manage_artists_page():
    return render_template("manage_artists.html")


# @app.route("/manage-home")
# # @admin_required
# def manage_home_page():
#     return render_template("home_edit.html")

# @app.route("/artistq/<int:artist_id>")
# def manage_home_page(artist_id):
#     return render_template("home_edit.html", artist_id=artist_id)

@app.route("/edit-home/<int:artist_id>")
def manage_home_page(artist_id):
    return render_template("homepageEdit.html", artist_id=artist_id)



@app.errorhandler(403)
def forbidden(_):
    return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
