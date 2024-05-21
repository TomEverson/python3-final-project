from flask import Flask
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

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
