# InstagramFakeDetect API 👁️

## About 🌟

Machine Learning **Socketify.py** API using DescionTree Classifier to predict if a account is Fake or Not

## Technologies Used 🖥️

- Socketify.py
- Scikit-Learn
- Sql lite
- instaloader api
- Docker
- Nginx Proxy Manager

## Desciption 🤖

<ul>
<li> <b>Self Hosted</b> using <b>Docker,Docker-Compose</b> and <b>Nginx Proxy manager</b>  on <b>Home Server(Arch linux)</b></li>

<li> Uses <b>Socketify.py</b> along with <b>Scikit learn & Pandas </b> To predict wheter a account is fake or not</li>

<li> First It Uses a Jupyter Notebook to put all generated json data into a <b>SQL lite</b> database </li>

<li> Uses Attributes like <b>Followers,Following ,like etc.</b> and <b>DescionTree Classifier</b> to determine the result</li>

<li> Model is serialized into a <b>Pickle</b> file</li>

<li> The api take a get request with username ,parses data using <b>Instagrapi</b> and predicts using serialized model</li>
                
</ul>

## Detection Parameters 🐋

1. `user_media_count` - Total number of posts, an account has.
2. `user_follower_count` - Total number of followers, an account has.
3. `user_following_count` - Total number of followings, an account has.
4. `user_has_profil_pic` - Whether an account has a profil picture, or not.
5. `user_is_private` - Whether an account is a private profile, or not.
6. `user_biography_length` - Number of characters present in account biography.
7. `username_length` - Number of characters present in account username.
8. `username_digit_count` - Number of digits present in account username.
9. `is_fake` - True, if account is a spam/fake account, False otherwise

<!-- ### Live 🔗 : https://instareact.akshayk.dev/ -->

## Thank you For your time 🚀
