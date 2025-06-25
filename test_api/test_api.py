from requests import post, get,codes
import json
STT_URL = "http://localhost:8000/transcriptions/"
API_TOKEN_URL = "http://localhost:8000/api/token/"
wav_path = "output.wav"
username = "oli19" # replace with your own username
password = "password" # replace with your own username

# Function to detect silence
def request_api_token() -> str:
    headers = {
        "Content-Type": "application/json"
    }
    response = post(
        API_TOKEN_URL,
        data=json.dumps({"username": username, "password": password}),
        headers=headers
    )

    if response.status_code == codes.ok:
        output = response.json()
        return output['access']
    else:
        return None

def get_request(params: dict = None) -> dict:
    headers = {
        'Authorization': f'Bearer {request_api_token()}'
    }
    response = get(
        STT_URL,
        headers=headers,
        params=params
    )
    output = response.json()
    
    if response.status_code == 200:
        return output
    else:
        return None

def post_request() -> str:
    with open(wav_path, 'rb') as f:
        files = {'wav_file': f}
        headers = {
            'Authorization': f'Bearer {request_api_token()}'
        }
        response = post(
            STT_URL,
            files=files,
            headers=headers,
        )

    if response.status_code == codes.created:
        output = response.json()
        return output['transcription']
    else:
        return None

def test():
    
    data = get_request()
    print(data)
    data = post_request()
    print(data)


if __name__ == "__main__":
    test()