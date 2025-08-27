import requests, os

MSG_URL = os.environ.get("MSG_URL", "http://localhost:7000/message/JohnDoe")
COUNT = int(os.environ.get("COUNT", 1000))
def genrerate_volume(count=100):
    for i in range(count):
        try:
            response = requests.get(MSG_URL)
            if response.status_code == 200:
                print(f"Message {i+1}: {response.text}")
            else:
                print(f"Failed to get message {i+1}: Status code {response.status_code}")
        except Exception as e:
            print(f"Error occurred while fetching message {i+1}: {e}")


if __name__ == "__main__":
    genrerate_volume(COUNT)
