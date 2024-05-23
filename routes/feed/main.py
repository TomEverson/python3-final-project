from flask import Blueprint, render_template, request, Response, redirect, g
from routes.auth.service import decode_jwt
from routes.feed.service import get_feed_service, create_feed_service, create_feed_upvote_service, create_downvote_service

feed = Blueprint('feed', __name__, url_prefix="/feeds")


@feed.before_request
def check_auth():
    cookie = request.cookies.get("access_token")
    if not cookie:
        return redirect("/login")
    user = decode_jwt(cookie)
    g.user = user


@feed.route("/", methods=["GET"])
def get_feed_page():
    feeds = get_feed_service(g.user)
    return render_template("feed/index.html", feeds=feeds)


@feed.route('/create', methods=["GET"])
def get_feed_create_page():
    return render_template("feed/create.html")


@feed.route('/create', methods=["POST"])
def create_feed():
    title = request.form.get("title")
    content = request.form.get('content')

    if not title or not content:
        error_message = "Some Of The Fields Are Missing"
        return f'<div class="p-4 bg-red-100 border border-red-300 text-red-800 rounded-md">{error_message}</div>', 400

    cookie = request.cookies.get("access_token")
    user = decode_jwt(cookie)

    create_feed_service(title, content, user)

    response = Response()
    response.headers['HX-Redirect'] = "/feeds"

    return response


@feed.route('feeds/upvote/<feed_id>', methods=["POST"])
def upvote_feed(feed_id):
    feed = create_feed_upvote_service(feedId=feed_id, user=g.user)
    return feed, 200


@feed.route('feeds/downvote/<feed_id>', methods=["POST"])
def downvote_feed(feed_id):
    feed = create_downvote_service(feedId=feed_id, user=g.user)
    return feed, 200
