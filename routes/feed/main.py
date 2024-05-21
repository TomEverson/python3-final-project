from flask import Blueprint, render_template, request, current_app, Response, redirect
from routes.auth.service import decode_jwt
from bson import ObjectId


feed = Blueprint('feed', __name__)


@feed.route("/feed", methods=["GET"])
def get_feed_page():
    cookie = request.cookies.get("access_token")
    if not cookie:
        return redirect("/login")

    feeds = []
    query = current_app.db.feeds.find()
    for feed in query:
        user = current_app.db.users.find_one({"_id": ObjectId(feed["userId"])})
        feed['user'] = user
        del user['password']
        feeds.append(feed)

    return render_template("feed/index.html", feeds=feeds)


@feed.route('/feed/create', methods=["GET"])
def get_feed_create_page():
    return render_template("feed/create.html")


@feed.route('/feed/create', methods=["POST"])
def create_feed():
    title = request.form.get("title")
    content = request.form.get('content')

    if not title or not content:
        error_message = "Some Of The Fields Are Missing"
        return f'<div class="p-4 bg-red-100 border border-red-300 text-red-800 rounded-md">{error_message}</div>', 400

    cookie = request.cookies.get("access_token")
    user = decode_jwt(cookie)

    current_app.db.feeds.insert_one({"title": title,
                                     "content": content,
                                     "userId": user["user_id"]
                                     })

    response = Response()
    response.headers['HX-Redirect'] = "/feed"

    return response
