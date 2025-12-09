# from artistportal import create_app

# app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)


# from artistportal import create_app
# from flask import render_template

# app = create_app()

# @app.route("/")
# def home_page():
#     # For now, hard-code artist_id = 1 (Martin Green)
#     return render_template("home.html", artist_id=1)

# @app.route("/activities")
# def activities_page():
#     return render_template("activities.html", artist_id=1)

# if __name__ == "__main__":
#     app.run(debug=True)

#----------------------------------------------------------
# from artistportal import create_app
# from flask import render_template

# app = create_app()

# @app.route("/")
# def home_page():
#     # temp: hardcode artist 1
#     return render_template("home.html", artist_id=1)

# @app.route("/activities")
# def activities_page():
#     return render_template("activities.html", artist_id=1)

# if __name__ == "__main__":
#     app.run(debug=True)

#----------------------------------------------------------

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
