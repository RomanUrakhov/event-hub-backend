from flask import Flask, request, jsonify
import requests
import config

app = Flask(__name__)


@app.route('/api/auth/twitch', methods=['POST'])
def twitch_auth():
    data = request.get_json()
    code = data.get('code')

    if not code:
        return jsonify({'error': 'Missing authorization code'}), 400

    payload = {
        'client_id': config.TWITCH_CLIENT_ID,
        'client_secret': config.TWITCH_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': config.TWITCH_REDIRECT_URI,
    }

    try:
        response = requests.post('https://id.twitch.tv/oauth2/token', data=payload)
        response.raise_for_status()
        auth_data = response.json()

        # Extract user information from the id_token
        id_token = auth_data.get('id_token')
        if not id_token:
            return jsonify({'error': 'id_token not found in Twitch response'}), 400

        import jwt
        decoded_token = jwt.decode(id_token, options={'verify_signature': False})
        user_avatar = decoded_token.get('picture')
        user_username = decoded_token.get('preferred_username')

        # Return the tokens and user information to the frontend
        response_data = {
            'accessToken': id_token,
            'refreshToken': auth_data.get('refresh_token'),
            'userAvatar': user_avatar,
            'userName': user_username,
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000, debug=True)
