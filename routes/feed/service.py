from flask import current_app
from bson import ObjectId


def get_feed_service(user):
    feeds = []
    query = current_app.db.feeds.find()
    for feed in query:
        author = current_app.db.users.find_one(
            {"_id": ObjectId(feed["userId"])})
        feed['author'] = author
        del author['password']
        vote = current_app.db.votes.find_one(
            {"userId": user["userId"], "feedId": str(feed["_id"])})
        feed['vote'] = vote
        feeds.append(feed)

    return feeds


def create_feed_service(title, content, user):
    current_app.db.feeds.insert_one({"title": title,
                                    "content": content,
                                     "userId": user["userId"]
                                     })


def create_feed_upvote_service(feedId, user):
    vote = current_app.db.votes.find_one(
        {"userId": user["userId"], "feedId": feedId})

    if (not vote):
        current_app.db.votes.insert_one({"feedId": feedId,
                                         "userId": user["userId"],
                                         "vote": "UP"
                                         })
    else:
        current_app.db.votes.update_one(
            {"feedId": feedId}, {'$set': {"vote": "UP"}})

    return f'''<div class="flex gap-4" id="vote-{feedId}">

                    <div>
                        <button
                        hx-post="feed/upvote/{feedId}"
                        hx-swap="outerHTML"
                        hx-target="#vote-{feedId}"
                        disabled


                        class="text-red-400 focus:outline-none">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                            </svg>
                        </button>
                    </div>


                    <div>
                        <button
                        hx-post="feed/downvote/{feedId}"
                        hx-swap="outerHTML"
                        hx-target="#vote-{feedId}"


                        class="text-gray-400 hover:text-gray-800 focus:outline-none">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>
                    </div>
                </div>'''


def create_downvote_service(feedId, user):
    vote = current_app.db.votes.find_one(
        {"userId": user["userId"], "feedId": feedId})

    if (not vote):
        current_app.db.votes.insert_one({"feedId": feedId,
                                         "userId": user["userId"],
                                         "vote": "DOWN"
                                         })
    else:
        current_app.db.votes.update_one(
            {"feedId": feedId}, {'$set': {"vote": "DOWN"}})

    return f'''<div class="flex gap-4" id="vote-{feedId}">

                    <div>
                        <button
                        hx-post="feed/upvote/{feedId}"
                        hx-swap="outerHTML"
                        hx-target="#vote-{feedId}"



                        class="text-gray-400 hover:text-gray-800 focus:outline-none">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7"></path>
                            </svg>
                        </button>
                    </div>


                    <div>
                        <button
                        hx-post="feed/downvote/{feedId}"
                        hx-swap="outerHTML"
                        hx-target="#vote-{feedId}"
                        disabled


                        class="text-red-400 focus:outline-none disabled">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                            </svg>
                        </button>
                    </div>
                </div>'''
