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
            response_text = "Handled message event"
        else:
            response_text = "Not supported event"

        response = {
            'text': response_text
        }
        return jsonify(response)

    else:
        return '', 200


@app.route('/slack/command', methods=['POST'])
def slack_command():
    data = request.form.to_dict()

    command = data.get('command')

    if command == '/slack_command':
        response_text = "The command of '/slack_command' executed"
    else:
        response_text = "Not supported command"

    response = {
        'response_type': 'in_channel',
        'text': response_text
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
