# rest api for controlling application

from flask import Flask, request
from flask_restful import Resource, Api

class API:

    app = Flask(__name__)
    api = Api(app)

    def __init__(self):
        print("api initialization start")
        self.api.add_resource(self.FooBar, '/foobar')
        print("__name__: "+__name__)
        if __name__ == '__main__':
            self.app.run(port='1337')
            print("api initialized")

    class FooBar(Resource):
        def get(self):
            return "ping"