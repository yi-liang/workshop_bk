import os
import support
from flask import Flask, request, jsonify
from pymongo import MongoClient
app = Flask(__name__)

class SupportApp():
    """
    Update the DB when receive the notification from sensor value updates
    """
    def __init__(self):
        self.config = {}
        self.db_collection = None

    def start(self):
        self.read_config()
        self.db_connect()
        self.subscribe()

    def db_connect(self):
        """
        connect to db and set collection
        """
        client = MongoClient(self.config["DB_URI"])
        db = client[self.config["DB_NAME"]]
        self.db_collection = db[self.config["DB_COLLECTION"]]

    def subscribe(self):
        steps_dictionary = [("clients", "client_new"), ("ObjectTypeID", "3201"), ("InstanceID", "0")]
        #TODO update object/instance id
        testdata = {
            "SubscriptionType":"Observation",
            "Url":self.config["APP_URL"]
        }
        support.request(self.config["CREATOR_ACCESS_KEY"], self.config["CREATOR_ACCESS_SECRET"], \
                method="post", steps=steps_dictionary, data=testdata)
        #TODO handle subscribe failed

    def read_config(self, config_file="setting.conf"):
        """
        read the config file
        """
        with open(config_file) as configfile:
            exec(configfile.read(), self.config)

    @app.route("/api/receive", methods=["POST"])
    def receive_msg(self):
        """
        receive the notification
        """
        content = request.json
        # TODO read the content and pass value to db
        self.update_db("testing1")

    def update_db(self, value):
        self.db_collection.insert_one({self.config["DB_KEY"]:value})

if __name__ == "__main__":
    support_app = SupportApp()
    support_app.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
