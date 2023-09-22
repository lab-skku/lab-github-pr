import os

import requests
from dotenv import load_dotenv
from flask import Flask

app = Flask(__name__)

load_dotenv()

slack_token = os.getenv('SLACK_TOKEN')
github_token = os.getenv('GITHUB_TOKEN')
ngrok_token = os.getenv('NGROK_TOKEN')


@app.route('/')
def index():
    return {'message': 'Hello, Devs!'}, 200


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
            response_text = "지원하지 않는 이벤트입니다."

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

    if command == '/my_command':
        response_text = "슬래시 커맨드 '/my_command'가 실행되었습니다."
    else:
        response_text = "Not supported command"

    response = {
        'response_type': 'in_channel',
        'text': response_text
    }

    return jsonify(response)


@app.route('/github/<github_id>', methods=['GET'])
def github(github_id):
    api_url = f'https://api.github.com/repos/lab-skku/lab-github-pr/collaborators/{github_id}'
    data = {
        'permission': 'admin'
    }
    headers = {
        'Authorization': f'token {github_token}'
    }
    try:
        response = requests.put(api_url, headers=headers, json=data)

        if response.status_code == 204:
            return {'message': 'added'}, 200
        else:
            return {'message': response.status_code}, 400
    except requests.exceptions.RequestException as e:
        return {'message': e}, 500


if __name__ == '__main__':
    app.run(debug=True)
