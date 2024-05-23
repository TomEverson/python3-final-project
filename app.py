from flask import Flask, redirect
from module.redis import connect_redis
from module.resend import connect_resend
from module.mongo import connect_mongo


def create_app():
    app = Flask(__name__)

    #! Modules
    with app.app_context():
        app.redis = connect_redis()
        app.resend = connect_resend()
        app.db = connect_mongo()

    #! Routing
    from routes.auth.main import auth
    from routes.feed.main import feed

    app.register_blueprint(auth)
    app.register_blueprint(feed)

    @app.route("/")
    def route():
        return redirect('/feeds')

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
