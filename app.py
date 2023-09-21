from decouple import config  # noqa
from flask import Flask

app = Flask(__name__)

slack_token = config('SLACK_TOKEN')


@app.route('/')
def index():
    return {'message': 'Hello, folks!'}, 200


if __name__ == '__main__':
    app.run(debug=True)
