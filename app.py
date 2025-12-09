from artistportal import create_app
from flask import render_template

app = create_app()

# NEW: artist list page (first page)
@app.route("/")
def artist_list_page():
    return render_template("artists_list.html")


# DASHBOARD for a specific artist  ← this MUST be named home_page
@app.route("/artist/<int:artist_id>")
def home_page(artist_id):
    return render_template("home.html", artist_id=artist_id)

# Activities page for that artist (optional, but handy)
@app.route("/artist/<int:artist_id>/activities")
def activities_page(artist_id):
    return render_template("activities.html", artist_id=artist_id)

if __name__ == "__main__":
    app.run(debug=True)
