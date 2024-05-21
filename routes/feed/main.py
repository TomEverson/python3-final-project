from flask import Blueprint, render_template, Response, request, redirect, current_app
from routes.auth.service import generate_auth_code, confirm_auth_code

feed = Blueprint('feed', __name__)


@feed.route("/feed", methods=["GET"])
def get_feed_page():
    return render_template("feed/index.html")
