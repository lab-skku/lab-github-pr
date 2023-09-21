from decouple import config  # noqa
from flask import Flask

app = Flask(__name__)

slack_token = config('SLACK_TOKEN')


@app.route('/')
def index():
    return {'message': 'Hello, folks!'}, 200


@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json

    event_type = data.get('type')

    if event_type == 'url_verification':
        challenge = data.get('challenge')
        return jsonify({'challenge': challenge})

    elif event_type == 'event_callback':
        event = data.get('event')

        if event['type'] == 'message':
            response_text = "메시지 이벤트를 처리했습니다."
        else:
            response_text = "지원하지 않는 이벤트 타입입니다."

        response = {
            'text': response_text
        }
        return jsonify(response)

    else:
        return '', 200


if __name__ == '__main__':
    app.run(debug=True)
