import requests

def get_prediction(message: str):
    try:
        response = requests.post("http://localhost:5001/predict", json={"text": message})
        return response.json()
    except Exception as e:
        return {"error": str(e), "type": "error"}
