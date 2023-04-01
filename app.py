from flask import Flask, request, jsonify
import pickle #for loading model
import pandas as pd
import instaloader #Instagram API for Public Info
from flask_cors import CORS

# Load the Scikit-Learn model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the Flask app
app = Flask(__name__)

CORS(app)

# Load the decision tree model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Main Production route from Client    
@app.route('/user/<username>', methods=['GET'])
def get_user_info(username):
    
    # create an instance of Instaloader class
    loader = instaloader.Instaloader()

    try:
        # get the user profile by username
        profile = instaloader.Profile.from_username(loader.context, username)

        # extract user information
        user_info = {
            "userFollowerCount": profile.followers,
            "userFollowingCount": profile.followees,
            "userBiographyLength": len(profile.biography),
            "userMediaCount": profile.mediacount,
            "userHasProfilPic": int(profile.profile_pic_url is not None),#Convet Boolean To Numerical
            "userIsPrivate": int(profile.is_private),
            "usernameDigitCount": sum(c.isdigit() for c in username),
            "usernameLength": len(username)
        }

     
        
        
        df = pd.DataFrame.from_dict(user_info, orient="index").T

        # Make a prediction
        prediction = model.predict(df)

        # Convert the prediction to a Python int // 0 for Real and 1 for Fake
        prediction = int(prediction[0])

        # Create a dictionary with the prediction result
        result = {"prediction": prediction}

      
        return result
        
        
        
        
        
        

    except instaloader.exceptions.ProfileNotExistsException:
        # handle the case when the profile doesn't exist
        return jsonify({"error": f"Profile with username {username} doesn't exist"}), 404

    except Exception as e:
        # handle any other exceptions
        return jsonify({"error": f"An error occurred while processing the request: {str(e)}"}), 500





# Define a route for the predict API
@app.route('/predict', methods=['POST'])
def predict():
     # Get the input data from the request
    data = request.get_json()

    # Convert the JSON data to a pandas DataFrame
    df = pd.DataFrame.from_dict(data, orient="index").T

    # Make a prediction
    prediction = model.predict(df)

    # Convert the prediction to a Python int
    prediction = int(prediction[0])

    # Create a dictionary with the prediction result
    result = {"prediction": prediction}

    # Return the result as a JSON response
    return jsonify(result)




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)