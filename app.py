from os import error
import pickle  # for loading model
import pandas as pd
from instagrapi import Client  # Instagram API for Public Info
import os
# Load the Scikit-Learn model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the Flask app
from socketify import App
import requests
import jwt
app = App()
# Instagram API Credentials

INSTAGRAM_USERNAME = "inq.isitives@gmail.com"
INSTAGRAM_PASSWORD = "inq.isitives@18"

CLIENT_ID = '615827887363040'
CLIENT_SECRET = '6c8c670effec415f2f78f72a5c92dfa6'
REDIRECT_URI = 'http://localhost:5000/login/authorize'
INSTAGRAM_API_BASE_URL = 'https://api.instagram.com/v1/'
# Create an Instagram client
client = Client()
client.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
def get_instagram_access_token(code):
    url = 'https://api.instagram.com/oauth/access_token'
    
    # Set the headers for form-encoded data
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': 'authorization_code'
    }

    response = requests.post(url, headers=headers, data=data)

    response_data = response.json()
    
    if 'access_token' in response_data:
        return response_data['access_token']
    else:
        return None
# Helper function to fetch user information from Instagram
def get_instagram_user_info(access_token):
    url = f'{INSTAGRAM_API_BASE_URL}users/self/?access_token={access_token}'
    response = requests.get(url)
    user_data = response.json()
    return user_data

# Helper function to generate a JWT token
def generate_jwt_token(user_info):
    # Create a JWT payload including user_info
    payload = {
        'user_info': user_info
    }
    # Use your secret key for signing the token
    jwt_token = jwt.encode(payload, 'your_jwt_secret_key', algorithm='HS256')
    return jwt_token
# Main Production route from Client

def login(res,req):
    # Redirect the user to Instagram's OAuth authorization URL
    authorization_url = f'https://api.instagram.com/oauth/authorize/?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code'
    res.redirect(authorization_url)
def authorized(res,req):
    code = req.get_query('code')
    if code:
        # Exchange the code for an access token
        access_token = get_instagram_access_token(code)

        if access_token:
            user_info = get_instagram_user_info(access_token)
            jwt_token = generate_jwt_token(user_info)
            res.cork_end(jwt_token)

    res.cork_end('Failed to authenticate with Instagram.')
def get_user_info(res,req):
    try:
        # Get the user by username
        username=req.get_parameter(0)
        user = client.user_info_by_username(username)
        
        # Extract user information
        user_info = {
            "userFollowerCount": user.follower_count,
            "userFollowingCount": user.following_count,
            "userBiographyLength": len(user.biography),
            "userMediaCount": user.media_count,
            "userHasProfilPic": int(bool(user.profile_pic_url)),  # Convert Boolean To Numerical
            "userIsPrivate": int(user.is_private),
            "usernameDigitCount": sum(c.isdigit() for c in username),
            "usernameLength": len(username)
        }

        df = pd.DataFrame.from_dict(user_info, orient="index").T

        # Make a prediction
        prediction = model.predict(df)

        # Convert the prediction to a Python int // 0 for Real and 1 for Fake
        prediction = int(prediction[0])

        # Create a dictionary with the prediction result
        result = {"prediction": prediction,"user":user_info}
        custom_headers = (
            ("Access-Control-Allow-Origin", "*"),  # CORS header to allow any origin
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),  # CORS header for allowed methods
            ("Access-Control-Allow-Headers", "Content-Type")  # CORS header for allowed headers
        )
        res.send(result, headers=custom_headers)
    except Exception as e:
        # handle any exceptions
        error_headers = (
            ("X-Rate-Limit-Remaining", "0"),  # Adjust as needed
            (b'Another-Headers', b'ErrorValue'),  # Adjust as needed
            ("Access-Control-Allow-Origin", "*"),  # CORS header to allow any origin
            ("Access-Control-Allow-Methods", "GET, POST, OPTIONS"),  # CORS header for allowed methods
            ("Access-Control-Allow-Headers", "Content-Type")  # CORS header for allowed headers
        )
        res.send( {"error": f"An error occurred while processing the request: {str(e)}"}, status="400",headers=error_headers)
app.get("/login",login)
app.get("/login/authorized",authorized)

app.get("/user/:username",get_user_info)
# Define a route for the predict API
# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get the input data from the request
#     data = request.get_json()
#
#     # Convert the JSON data to a pandas DataFrame
#     df = pd.DataFrame.from_dict(data, orient="index").T
#
#     # Make a prediction
#     prediction = model.predict(df)
#
#     # Convert the prediction to a Python int
#     prediction = int(prediction[0])
#
#     # Create a dictionary with the prediction result
#     result = {"prediction": prediction}
#
#     # Return the result as a JSON response
#     return jsonify(result)


# Run the Flask app
app.listen(5000, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))
app.run()

