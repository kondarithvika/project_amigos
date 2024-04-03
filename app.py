from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, send_file
import mysql.connector
from mysql.connector import Error
from flask_bcrypt import Bcrypt
import jwt
import datetime
from werkzeug.utils import secure_filename
from mysql.connector import Binary
import os  # Import the os module
from pydub import AudioSegment
import io
import json
import base64
import psycopg2
# from flask import Flask, render_template
from moviepy.editor import VideoFileClip, AudioFileClip

# from flask import jsonify






app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'my secret key'

current_directory = os.path.dirname(__file__)
static_folder_path = os.path.join(current_directory, 'static')
selected_img_folder_path = os.path.join(static_folder_path, 'selected_images')
app.config['UPLOAD_FOLDER'] = selected_img_folder_path  # Specify the path to your upload folder


# Additional configuration for file upload to a separate database
# db_config = {
#    'host': 'localhost',
#    'user': 'root',
#    'password': 'rithu2005',
#    'database': 'amigos_project'
# }
# def db_config():
#    conn=psycopg2.connect("postgresql://rithu:XLwR9lBbDvC7qUUArHTjcg@wide-panda-8901.8nk.gcp-asia-southeast1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")
#    return conn
def db_config():
    # Decode the base64 certificate
    cert_decoded = base64.b64decode(os.environ['ROOT_CERT_BASE64'])
    
    # Define the path to save the certificate
    cert_path = '/opt/render/.postgresql/root.crt'
    os.makedirs(os.path.dirname(cert_path), exist_ok=True)
    
    # Write the certificate to the file
    with open(cert_path, 'wb') as cert_file:
        cert_file.write(cert_decoded)
    
    # Set up the connection string with the path to the certificate
    conn = psycopg2.connect(
        "host=wide-panda-8901.8nk.gcp-asia-southeast1.cockroachlabs.cloud "
        "port=26257 dbname=defaultdb user=rithu "
        "password=XLwR9lBbDvC7qUUArHTjcg sslmode=verify-full "
        f"sslrootcert={cert_path}"
    )
    return conn

def close_connection(conn):
  #  if conn.is_connected():
      conn.close()
      print('Connection to MySQL database closed')

def connect_to_mysql():
   try:
      conn = db_config()

      print(conn)
      print('connected success')
    #   if conn.is_connected():
        #  print(f'Connected to MySQL database')
        #  return conn
   except Error as e:
      print(e)

# nvalue = 0

# def create_folder_if_not_exists(folder_path):
#     # print("hello---------------")
#     if not os.path.exists(folder_path):
#         os.makedirs(folder_path)

# # Define the paths for audio and selectedAudio folders
# # audio_folder = '/your/custom/path/audio'  # Update this with your desired path
# selected_images = 'static/'  # Update this with your desired path

# # Create the necessary folders if they don't exist
# # create_folder_if_not_exists(audio_folder)
# create_folder_if_not_exists(selected_images)

selected_images = 'selected_images'

# Function to create folder if it does not exist inside the 'static' folder
def create_folder_if_not_exists(folder_path):
    full_path = os.path.join( 'static',folder_path)
    if not os.path.exists(full_path):
        os.makedirs(full_path)

# Call the function to create 'selected_images' folder inside 'static'
# create_folder_if_not_exists(selected_images)

#########################################################
def retrieve_audio_files(output_folder):
    try:

        # connection = mysql.connector.connect(**db_config)
        # cursor = connection.cursor()
        conn = db_config()
        print("Connected to MySQL")
        cursor = conn.cursor()


        # Retrieve audio data from the database
        query = "SELECT id, audio_data FROM audio_files"
        cursor.execute(query)

        for (audio_id, audio_data) in cursor:
            # Create a filename based on the audio ID
            file_name = f"audio_{audio_id}.mp3"
            file_path = os.path.join(output_folder, file_name)

            # Write audio data to a file
            with open(file_path, 'wb') as audio_file:
                audio_file.write(audio_data)

            print(f"Audio file {file_name} saved.")

        print("Audio files retrieved and saved successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            # connection.close()
            print("Database connection closed.")

# Example: Retrieve and save audio files to a folder named 'downloaded_audios'
output_folder = 'static/downloaded_audios'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

##############################################################
# retrieve_audio_files(output_folder)  
 #####################################################  run only once when 

# def create_users_table():
#     conn = connect_to_mysql()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS users_details (
#                         userid INT AUTO_INCREMENT PRIMARY KEY,
#                         username VARCHAR(255) COLLATE utf8mb4_bin NOT NULL UNIQUE,
#                         email VARCHAR(255) UNIQUE,
#                         fullname VARCHAR(255) NOT NULL,
#                         password VARCHAR(255) NOT NULL
#                     )
#                 """)
#                 conn.commit()
#         finally:
#             close_connection(conn)
# def create_users_table():
#     conn = db_config()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS users_details (
#                         userid SERIAL PRIMARY KEY,
#                         username VARCHAR(255) NOT NULL UNIQUE,
#                         email VARCHAR(255) UNIQUE,
#                         fullname VARCHAR(255) NOT NULL,
#                         password VARCHAR(255) NOT NULL
#                     )
#                 """)
#                 conn.commit()
#                 print("Table 'users_details' created successfully.")
#         finally:
#             close_connection(conn)


# Create images table
# def create_images_table():
#     conn = connect_to_mysql()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS images_table (
#                         imageid INT AUTO_INCREMENT PRIMARY KEY,
#                         userid INT NOT NULL,
#                         image LONGBLOB
#                     )
#                 """)
#                 conn.commit()
#         finally:
#             close_connection(conn)
# def create_images_table():
#     conn = connect_to_postgresql()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS images_table (
#                         imageid SERIAL PRIMARY KEY,
#                         userid INT NOT NULL,
#                         image BYTEA
#                     )
#                 """)
#                 conn.commit()
#         finally:
#             close_connection(conn)

# def create_audio_files():
#     conn = connect_to_mysql()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS audio_files (
#                         id INT AUTO_INCREMENT PRIMARY KEY,
#                         audio_name VARCHAR(255) ,
#                         audio_data LONGBLOB
#                     )
#                 """)
#                 conn.commit()
#         finally:
#             close_connection(conn)
# def create_audio_files():
#     conn = connect_to_postgresql()
#     if conn:
#         try:
#             with conn.cursor() as cursor:
#                 cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS audio_files (
#                         id SERIAL PRIMARY KEY,
#                         audio_name VARCHAR(255),
#                         audio_data BYTEA
#                     )
#                 """)
#                 conn.commit()
#         finally:
#             close_connection(conn)


def generate_token(username):
    expiry_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    payload = {'username': username, 'exp': expiry_date}
    token = jwt.encode(payload, app.secret_key, algorithm='HS256')
    return token   

# Function to verify JWT token
def verify_token(token):
    try:
        payload = jwt.decode(token,app.secret_key, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None     


@app.route('/')
def index():
   return render_template('index.html')





def save_files_to_database(userid, file_names):
    try:
        conn = db_config()
        print("Connected to MySQL")
        cursor = conn.cursor()

        for file_name in file_names:
            with open(file_name, 'rb') as file:
                image_data = file.read()
                print(image_data)
                # Insert each image separately
                cursor.execute('''
                    INSERT INTO images_table (userid, image)
                    VALUES (%s, %s)
                ''', (userid, image_data))
                conn.commit()

        print('Files saved to the database successfully')

    except Error as e:
        print(f'Error saving files to the database: {str(e)}')

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()



def save_selected_files_to_database(userid, file_name):
    try:
        # conn = mysql.connector.connect(**db_config)
        conn = db_config()
        print("SELCETED...Connected to MySQL")
        cursor = conn.cursor()

        print(file_name)
        # for file_name in file_names:
        with open(file_name, 'rb') as file:
            image_data = file.read()
            # Insert each image separately
            cursor.execute('''
                INSERT INTO images_table (userid, selected_images)
                VALUES (%s, %s)
            ''', (userid, mysql.connector.Binary(image_data)))
            conn.commit()

        print('Files saved SELECTED to the database successfully')

    except Error as e:
        print(f'Error saving SELECTED files to the database: {str(e)}')

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'conn' in locals() and conn is not None:
            conn.close()



# @app.route('/signup', methods=['POST','GET'])
# def signup():
#     error = None
#     # error_mssg = None
#     conn = db_config()
#     # cursor = conn.cursor(dictionary=True)
#     cursor = conn.cursor()
#     if request.method == 'POST':
#         username = request.form['username']
#         email = request.form['email']
#         fullname = request.form['fullname']
#         password = request.form['password']

#         if not (username and email and fullname and password):
#             error = "All fields are required."
#             return render_template('index.html', error=error)


#         import re
#         email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
#         if not re.match(email_regex, email):
#         # import re
#         # if not re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email):
#             create_folder_if_not_exists(selected_images)
#             return render_template('index.html', error="Invalid email format. Please enter a valid email.")


#         # Check if the username or email already exists
#         cursor.execute("SELECT * FROM users_details WHERE username = %s OR email = %s", (username, email))
#         existing_user = cursor.fetchone()
#         if existing_user:
#             error = "User with this username or email already exists."
#             return render_template('index.html', error=error)  # Render the signup page with the error message
#         else:
#             # Hash the password
#             hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')



#             # Insert the new user into the database
#             insert_query = "INSERT INTO users_details (username, email, fullname, password) VALUES (%s, %s, %s, %s)"
#             user_data = (username, email, fullname, hashed_password)
#             cursor.execute(insert_query, user_data)
#             conn.commit()

#              # Fetch the newly created user to get the userid
#             cursor.execute("SELECT userid FROM users_details WHERE username = %s", (username,))
#             new_user = cursor.fetchone()
#             if new_user:
#                 session['userid'] = new_user[0]  # Set userid in session
#                 flash('User registered successfully. Please log in.', 'success')
#                 close_connection(conn)
#                 return redirect(url_for('mult_image'))  # Redirect to the index page

#             # close_connection(conn)
#             # return redirect(url_for('mult_image'))  # Redirect to the success route

#     return render_template('index.html', error=error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    conn = db_config()
    cursor = conn.cursor()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        fullname = request.form['fullname']
        password = request.form['password']

        # if not username :
        #     error = "All fields are required"
        #     return render_template('index.html', error=error)

        # if not email :
        #     error = "All fields are required"
        #     return render_template('index.html', error=error)

        # elif not fullname :
        #     error = "All fields are required"
        #     return render_template('index.html', error=error)

        # elif not password :
        #     error = "All fields are required"
        #     return render_template('index.html', error=error)

        # if not username:
        #     print('hello1.........')
        #     error = "Username is required."
        # elif not email:
        #     print('hello22.........')
        #     error = "Email is required."
        # elif not fullname:
        #     print('hello33.........')
        #     error = "Full name is required."
        # elif not password:
        #     print('hello44.........')
        #     error = "Password is required."

        # if error is not None:
        #     return render_template('index.html', error=error)






        if not (username and email and fullname and password):
            print('helloo.........')
            error = "All fields are required."
            return render_template('index.html', error=error)

        import re
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_regex, email):
            return render_template('index.html', error="Invalid email format. Please enter a valid email.")

        cursor.execute("SELECT * FROM users_details WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            error = "User with this username or email already exists."
            return render_template('index.html', error=error)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        insert_query = "INSERT INTO users_details (username, email, fullname, password) VALUES (%s, %s, %s, %s)"
        user_data = (username, email, fullname, hashed_password)
        cursor.execute(insert_query, user_data)
        conn.commit()
        # token = generate_token(username)
        # session['token']=token
        session['username']=username




        # Fetch the newly created user to get the userid
        cursor.execute("SELECT userid,username FROM users_details WHERE username = %s", (username,))
        new_user = cursor.fetchone()

        if new_user:
            session['userid'] = new_user[0]
            # session['userid'] = user[0]  # Userid is at index 0
            # session['token'] = token
            session['username'] = new_user[1]
            # session['fullname'] = new_user[3]
            flash('User registered successfully. Please log in.', 'success')
            conn.close()
            create_folder_if_not_exists(selected_images)
            return redirect(url_for('mult_image'))

    conn.close()
    return render_template('index.html', error=error)


@app.route('/value',methods=['POST', 'GET'])
def value():
    input_value = request.form['inputValue']
    # nvalue = input_value
    # print("===========",nvalue)
    session['nvalue'] = input_value
    return render_template('multImag.html')

    # value = request.form.get('username', '')




@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        conn = db_config()
        cursor = conn.cursor()

        username = request.form.get('username', '')
        password = request.form.get('password', '')

        cursor.execute("SELECT * FROM users_details WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user and bcrypt.check_password_hash(user[4], password):  # Password hash is at index 3
            # token = generate_token(username)
            session['userid'] = user[0]  # Userid is at index 0
            session['username'] = user[1]  # Username is at index 1
            # session['token'] = token  # Storing the token in the session
            flash('Login successful.', 'success')
            conn.close()
            create_folder_if_not_exists(selected_images)
            return redirect(url_for('user_profile', username=username))
        else:
            error_msg = 'Invalid username or password'
            session['error_msg'] = error_msg
            conn.close()
            return redirect(url_for('login'))
    else:
        # If error message is in session, retrieve and then delete it
        error_msg = session.pop('error_msg', None)
        return render_template('index.html', error_msg=error_msg)


@app.route('/user_profile/<username>', methods=['POST', 'GET'])
def user_profile(username):
    # token = request.args.get('token')
    # verified_username = verify_token(token)

    # if verified_username == username:
        conn = db_config()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users_details WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            userid = user[0]
            session['userid'] = user[0]
            session['username'] = user[1]
            cursor.execute("SELECT imageid, image FROM images_table WHERE userid = %s", (userid,))
            images_data = cursor.fetchall()

            current_directory = os.path.dirname(__file__)
            static_folder_path = os.path.join(current_directory, 'static')
            temp_img_folder_path = os.path.join(static_folder_path, 'images')
            os.makedirs(temp_img_folder_path, exist_ok=True)

            # Create a list to store the image file names
            image_files = []

            for image_data in images_data:
                imageid = image_data[0]
                if not imageid:  # Skip if imageid is empty or None
                    print("Skipping image with empty imageid.")
                    continue

                if image_data[1] is None:
                    print(f"Skipping image {imageid} because image data is None")
                    continue
                # if image_data[1] is None:
                #     print(f"Skipping image {image_data[0]} because image data is None")
                #     continue
                imageid = image_data[0]
                file_name = f'temp_{imageid}.jpg'
                file_path = os.path.join(temp_img_folder_path, file_name)
                try:
                    with open(file_path, 'wb') as file:
                        file.write(image_data[1])
                    image_files.append(file_name)
                except Exception as e:
                    print(f"Error saving image {file_name}: {e}")

            conn.close()

            return render_template('user_page.html', user=user, image_files=image_files)
        else:
            conn.close()
            return "User not found."
    # else:
    #     return "Unauthorized access."


# Route to serve the images from the temporary folder
@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return send_file(os.path.join(app.root_path, 'static', filename))



# @app.route('/selectedImages')
# def selectedImages():
#     username = session.get('username')

#     if not username:
#         return "User not logged in."

#     # conn = connect_to_mysql()
#     conn = db_config()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users_details WHERE username = %s", (username,))
#     user = cursor.fetchone()

#     if not user:
#         conn.close()
#         return "User not found."

#     # Retrieve all images for the logged-in user
#     userid = user[0]
#     cursor.execute("SELECT imageid, selected_image FROM images_table WHERE userid = %s", (userid,))
#     images_data = cursor.fetchall()

#     current_directory = os.path.dirname(_file_)
#     static_folder_path = os.path.join(current_directory, 'static')
#     temp_img_folder_path = os.path.join(static_folder_path, 'selected_images')
#     os.makedirs(temp_img_folder_path, exist_ok=True)

#     # Save the image data to temporary files and store their filenames in the list
#     selected_image_files = []

#     for image_data in images_data:
#         imageid = image_data['imageid']
#         file_name = f'selected_{imageid}.jpg'
#         file_path = os.path.join(temp_img_folder_path, file_name)  # Use os.path.join to create the full path
#         with open(file_path, 'wb') as file:
#             file.write(image_data['image'])
#         selected_image_files.append(file_name)

#     conn.close()

#     # Render user profile template with user's details
#     # if user:
#     #     return render_template('video.html', user=user, image_file=selected_image_files)
#     # else:
#     #     return "User not found."
#     # Return JSON response with user details and image file paths
#     if user:
#         return json.dumps({"user": user, "image_files": selected_image_files})
#     else:
#         return "User not found."


@app.route('/selectedImages')
def selectedImages():
    username = session.get('username')

    if not username:
        return "User not logged in."

    conn = db_config()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_details WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found."

    # Retrieve all images for the logged-in user
    userid = user[0]
    cursor.execute("SELECT imageid, selected_images FROM images_table WHERE userid = %s", (userid,))
    images_data = cursor.fetchall()

    current_directory = os.path.dirname(__file__)
    static_folder_path = os.path.join(current_directory, 'static')
    temp_img_folder_path = os.path.join(static_folder_path, 'selected_images')
    os.makedirs(temp_img_folder_path, exist_ok=True)

    # Save the image data to temporary files and store their filenames in the list
    selected_image_files = []

    for image_data in images_data:
        imageid = image_data[0]  # Accessing first element of the tuple
        image_blob = image_data[1]  # Accessing second element of the tuple
        file_name = f'selected_{imageid}.jpg'
        file_path = os.path.join(temp_img_folder_path, file_name)  # Use os.path.join to create the full path
        with open(file_path, 'wb') as file:
            file.write(image_blob)  # Write the binary data directly
        selected_image_files.append(file_name)

    conn.close()

    # Return JSON response with user details and image file paths
    if user:
        return json.dumps({"user": user, "image_files": selected_image_files})
    else:
        return "User not found."


# Route to serve the images from the temporary folder
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#    return send_file(os.path.join(app.root_path, 'static', filename))

# Route to serve the images from the temporary folder
@app.route('/selected_uploads/<filename>')
def selected_uploads(filename):
   return send_file(os.path.join(app.root_path, 'static','selected_images', filename))



#    return jsonify({'success': False, 'message': 'No files uploaded'})
@app.route('/upload_files', methods=['POST', 'GET'])
def upload_files():
 # Retrieve userid from the session
    print("uploading.......................................")
    userid = session.get('userid')
    if not userid:
        flash('User not logged in', 'error')
        return redirect(url_for('login'))  

    image_files = request.files.getlist('image')
    print(image_files)
    if image_files:
        file_names = []
# Initialize image_file outside the loop
        image_file = None
        for image_file in image_files:
            file_name = secure_filename(image_file.filename)
            image_file.save(file_name)
            file_names.append(file_name)
# Check if image_file is defined before accessing it
        if image_file:
            # username = request.form.get('username', '')
            # conn = connect_to_mysql()
            # token = session.get('token')
            # username = session.get('username')
            username= session['username']

            # token = generate_token(username)
            print("username ............................")
            print(username)
            # print("TOKENNN ............................")
            # print(token)

            save_files_to_database(userid, file_names)
            print('Files uploaded and saved to the database successfully', 'success')
            # return redirect(url_for('user_profile', username=username,token=token))
 # Return token along with success response
            return jsonify({'success': True, 'username': username,})

    return jsonify({'success': False, 'message': 'No files uploaded'})

@app.route('/get_selected_images', methods=['GET'])
def get_selected_images():
 # Retrieve userid from the session
   userid = session.get('userid')
   if not userid:
      flash('User not logged in', 'error')
      return redirect(url_for('login'))  

   selected_image_files = request.files.getlist('image')

   if selected_image_files:
      file_names = []

      for image_file in selected_image_files:
         file_name = secure_filename(image_file.filename)
         image_file.save(file_name)
         file_names.append(file_name)

      save_files_to_database(userid, file_names)

      flash('Files uploaded and saved to the database successfully', 'success')

   return 'Files uploaded successfully'

# @app.route('/upload_seleted_files', methods=['POST'])
# def upload_seleted_files():
#  # Retrieve userid from the session
#    userid = session.get('userid')
#    if not userid:
#       flash('User not logged in', 'error')
#       return redirect(url_for('login'))  

#    image_files = request.files.getlist('image')

#    if image_files:
#       file_names = []

#       for image_file in image_files:
#          file_name = secure_filename(image_file.filename)
#          image_file.save(file_name)
#          file_names.append(file_name)

#       save_files_to_database(userid, file_names)

#       flash('Files uploaded and saved to the database successfully', 'success')

#    return 'Files uploaded successfully'


# @app.route('/get_selected_images', methods=['GET'])
# def get_selected_images():
#  # Retrieve userid from the session
#    userid = session.get('userid')
#    if not userid:
#       flash('User not logged in', 'error')
#       return redirect(url_for('login'))  

#    selected_image_files = request.files.getlist('image')

#    if selected_image_files:
#       file_names = []

#       for image_file in selected_image_files:
#          file_name = secure_filename(image_file.filename)
#          image_file.save(file_name)
#          file_names.append(file_name)

#       save_files_to_database(userid, file_names)

#       flash('Files uploaded and saved to the database successfully', 'success')

#    return 'Files uploaded successfully'

#........................................................................

@app.route('/upload_seleted_files', methods=['POST'])
def upload_seleted_files():
    print("uploading selected images....")
 # Retrieve userid from the session
    userid = session.get('userid')
    if not userid:
        flash('User not logged in', 'error')
        return redirect(url_for('login'))  

    image_files = request.files.getlist('image')
    selected_image_ids = request.form.getlist('selected[]')

    if image_files and selected_image_ids:
        for image_file, image_id in zip(image_files, selected_image_ids):
            file_name = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
            image_file.save(file_path)
            print(".........file_path...............")
            print(file_path)
            save_selected_files_to_database(userid, file_path)

        flash('SELECTED Files uploaded and saved to the database successfully', 'success')

    return 'SELECTED Files uploaded successfully'


from moviepy.editor import ImageSequenceClip
import os
import cv2


# def create_video(user_id):   
#     try:
#         # Define the paths
#         input_image_path = "static/selected_images"
#         output_video_path = "static"  
#         output_video_name = f"out_{user_id}.mp4"  # Use the user ID in the output video name
#         output_video_full_path = os.path.join(output_video_path, output_video_name)

#         # Read the input images and sort them
#         image_files = sorted(os.listdir(input_image_path))
#         if not image_files:
#             print("No image files found in the input directory.")
#             exit()

#         # Read the first image to get its dimensions
#         first_image = cv2.imread(os.path.join(input_image_path, image_files[0]))
#         if first_image is None:
#             print("Failed to read the first image.")
#             exit()
#         height, width, _ = first_image.shape

#         # Resize images to the same dimensions
#         for img_file in image_files:
#             img_path = os.path.join(input_image_path, img_file)
#             img = cv2.imread(img_path)
#             if img is None:
#                 print(f"Failed to read image: {img_path}")
#                 continue
#             img_resized = cv2.resize(img, (width, height))
#             cv2.imwrite(img_path, img_resized)

#         # Calculate the number of frames per image to ensure at least 1 second per image
#         num_images = len(image_files)
#         fps = 25
#         duration_per_image = 8  # Set the duration per image to 8 seconds
#         num_frames_per_image = max(1, int(fps * duration_per_image / num_images))  # Ensure at least 8 seconds per image

#         # Create a list of image files where each image is repeated according to the calculated number of frames
#         image_files_expanded = [os.path.join(input_image_path, img_file) for img_file in image_files for _ in range(num_frames_per_image)]

#         # Create ImageSequenceClip from the images with the expanded list
#         clip = ImageSequenceClip(image_files_expanded, fps=fps)

#         # Write the video file
#         clip.write_videofile(output_video_full_path, codec='libx264')

#         return output_video_name  # Return the name of the created video file

#     except Exception as e:
#         print(f"Error creating video: {e}")
#         return None
# def create_video(user_id):   
#     target_width=500
#     target_height=400
#     try:
#         # Define the paths
#         input_image_path = "static\\selected_images"
#         output_video_path = "static"  
#         output_video_name = f"out_{user_id}.mp4"
#         output_video_full_path = os.path.join(output_video_path, output_video_name)

#         # Read the input images and sort them
#         image_files = sorted(os.listdir(input_image_path))
#         if not image_files:
#             print("No image files found in the input directory.")
#             exit()

#         # Read the first image to get its dimensions
#         first_image = cv2.imread(os.path.join(input_image_path, image_files[0]))
#         if first_image is None:
#             print("Failed to read the first image.")
#             exit()
#         height, width, _ = first_image.shape

#         # Calculate the new dimensions while maintaining aspect ratio
#         aspect_ratio = width / height
#         new_height = target_height
#         new_width = int(target_height * aspect_ratio)
#         if new_width > target_width:
#             new_width = target_width
#             new_height = int(target_width / aspect_ratio)

#         # Resize images to the new dimensions
#         for img_file in image_files:
#             img_path = os.path.join(input_image_path, img_file)
#             img = cv2.imread(img_path)
#             if img is None:
#                 print(f"Failed to read image: {img_path}")
#                 continue
#             img_resized = cv2.resize(img, (new_width, new_height))
#             cv2.imwrite(img_path, img_resized)

#         # Calculate the number of frames per image to ensure at least 1 second per image
#              # Calculate the total duration of the video based on image durations
#         total_duration = 0
#         if image_durations is None:
#             image_durations = {}  # If no durations provided, default to 1 second per image
#         for img_file in image_files:
#             duration = image_durations.get(img_file, 1)  # Default to 1 second if duration not specified
#             total_duration += duration

#         # Calculate the number of frames per image to maintain the specified total duration
#         # num_images = len(image_files)
#         fps = 25
#         # num_frames_per_image = max(1, int(fps * total_duration / num_images))  # Ensure total duration is maintained

#         # Create a list of image files where each image is repeated according to the calculated number of frames
#         image_files_expanded = []
#         for img_file in image_files:
#             duration = image_durations.get(img_file, 2)  # Default to 1 second if duration not specified
#             num_frames = max(1, int(fps * duration))  # Ensure at least 1 frame for each second
#             for _ in range(num_frames):
#                 image_files_expanded.append(os.path.join(input_image_path, img_file))

#         num_images = len(image_files)
#         # fps = 25
#         duration_per_image = 8
#         num_frames_per_image = max(1, int(fps * duration_per_image / num_images))

#         # # Create a list of image files where each image is repeated according to the calculated number of frames
#         image_files_expanded = [os.path.join(input_image_path, img_file) for img_file in image_files for _ in range(num_frames_per_image)]

#         # Create ImageSequenceClip from the images with the expanded list
#         clip = ImageSequenceClip(image_files_expanded, fps=fps)

#         # Write the video file
#         clip_resized = clip.resize((target_width, target_height))
#         clip_resized.write_videofile(output_video_full_path, codec='libx264', bitrate='5000k', preset='medium')

#         return output_video_name

#     except Exception as e:
#         print(f"Error creating video: {e}")
#         return None
def create_video(user_id, image_durations=None):
    try:
        target_width = 500
        target_height = 400
        input_image_path = "static/selected_images"
        output_video_path = "static"
        output_video_name = f"out_{user_id}.mp4"
        output_video_full_path = os.path.join(output_video_path, output_video_name)

        # Get a list of image files in the input directory
        image_files = sorted(os.listdir(input_image_path))

        # Create a list of readable image files and their paths
        valid_image_files = []
        valid_image_paths = []
        for img_file in image_files:
            img_path = os.path.join(input_image_path, img_file)
            img = cv2.imread(img_path)
            if img is not None:
                valid_image_files.append(img_file)
                valid_image_paths.append(img_path)
            else:
                print(f"Failed to read image: {img_path}")

        if not valid_image_files:
            print("No readable image files found in the input directory.")
            return None

        first_image = cv2.imread(valid_image_paths[0])
        if first_image is None:
            print("Failed to read the first image.")
            return None
        height, width, _ = first_image.shape

        # Resize valid images to the same dimensions
        for img_path in valid_image_paths:
            img = cv2.imread(img_path)
            img_resized = cv2.resize(img, (width, height))
            cv2.imwrite(img_path, img_resized)

        # Calculate total duration of the video based on image durations
        total_duration = 0
        if image_durations is None:
            image_durations = {}
        for img_file in valid_image_files:
            duration = image_durations.get(img_file, 1)
            total_duration += duration

        fps = 25

        # Create a list of image files where each image is repeated according to the calculated number of frames
        image_files_expanded = []
        for img_file in valid_image_files:
            duration = image_durations.get(img_file, 2)
            num_frames = max(1, int(fps * duration))
            for _ in range(num_frames):
                image_files_expanded.append(os.path.join(input_image_path, img_file))

        # Create ImageSequenceClip from the images with the expanded list
        clip = ImageSequenceClip(image_files_expanded, fps=fps)
        clip_resized = clip.resize((target_width, target_height))
        clip_resized.write_videofile(output_video_full_path, codec='libx264')

        return output_video_name

    except Exception as e:
        print(f"Error creating video: {e}")
        return None

@app.route('/video', methods=['GET'])
def video():
     # Get the user ID from the session
    # user_id = session.get('user_id')
    username = session.get('username')

    if not username:
        return "User not logged in."

    # conn = connect_to_mysql()
    conn = db_config()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users_details WHERE username = %s", (username,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return "User not found."

    # Retrieve all images for the logged-in user
    user_id = user[0]
    print("..............................................................................")
    print(user_id)
    if user_id is None:
        print("User ID not found in session.")
        # return
        return "User ID not found in session."  # Return a valid response when user ID is not found

    video_name = create_video(user_id)
    if video_name is None:
        return "Error creating video."  # Return a valid response when there's an error creating the video

    video_path = f"{video_name}"  # Update the path accordingly

    return render_template('video.html', video_path=video_path)



# @app.route('/video')
# def video():
#     create_video()
#     video_path = "out.mp4"  # Update the path accordingly
#     return render_template('video.html', video_path=video_path)
##################################################################################
# def create_video(image_files):
#     # Define the paths
#     output_video_path = "static"
#     output_video_name = "out.mp4"
#     output_video_full_path = os.path.join(output_video_path, output_video_name)

#     # Calculate the number of frames per image to ensure at least 1 second per image
#     num_images = len(image_files)
#     fps = 25
#     duration_per_image = 8  # Set the duration per image to 8 seconds
#     num_frames_per_image = max(1, int(fps * duration_per_image / num_images))

#     # Create a list of image files where each image is repeated according to the calculated number of frames
#     image_files_expanded = [img for img in image_files for _ in range(num_frames_per_image)]

#     # Create ImageSequenceClip from the images with the expanded list
#     clip = ImageSequenceClip(image_files_expanded, fps=fps)

#     # Write the video file
#     clip.write_videofile(output_video_full_path, codec='libx264')

#     # Return the path of the created video
#     return output_video_full_path

# @app.route('/video', methods=['POST'])
# def video():
#     # Get selected image filenames from the request
#     selected_images = request.json['selected_images']
#     if not selected_images:
#         return jsonify({'error': 'No images selected'}), 400

#     # Construct the paths to the selected images
#     input_image_path = "static/selected_images"
#     image_files = [os.path.join(input_image_path, img) for img in selected_images]

#     # Create the video
#     video_path = create_video(image_files)

#     # Return the path of the created video
#     return render_template('video.html', video_path=video_path)
#     # return jsonify({'video_path': video_path})



#.................................................................


def insert_audio_files(file_paths):
    try:
        # # Database connection configuration
        # db_config = {
        #     'host': 'localhost',
        #     'user': 'root',
        #     'password': 'rithu2005',
        #     'database': 'amigos_project'
        # }
        conn = db_config()
        print("Connected to MySQL")
        cursor = conn.cursor()


        # Establish a connection to the database
        # connection = mysql.connector.connect(**db_config)
        # cursor = connection.cursor()

        for file_path in file_paths:
            # Read audio file as binary data
            with open(file_path, 'rb') as audio_file:
                audio_data = audio_file.read()
              

            # Insert audio data into the database
            insert_query = "INSERT INTO audio_files (audio_data) VALUES (%s)"
            cursor.execute(insert_query, (audio_data,))

        # Commit the changes
        conn.commit()

        print("Audio files inserted successfully.")

    # except mysql.connector.Error as err:
    #     print(f"Error: {err}")

    finally:
        # Close the database connection
        if conn:
            cursor.close()
            conn.close()
            print("Database connection closed.")

# Example: Insert five audio files into the database
audio_file_paths = [
   'audio_1.mp3',
   'audio_2.mp3',
   'audio_3.mp3',
   'audio_4.mp3',
   'audio_5.mp3',
]

# insert_audio_files(audio_file_paths)


@app.route('/multImage')
def mult_image():
    return render_template('multImag.html')


# @app.route('/video')
# def video():
#     # return render_template('video.html')
#     return send_file(video_path, mimetype='video/mp4')

#######################################################################

# insert_audio_files(audio_file_paths)

##################################################### just call above one only for first time 

# Add this route to serve audio options
# @app.route('/get_audio_options')
# def get_audio_options():
#     try:
#         conn = connect_to_mysql()
#         cursor = conn.cursor(dictionary=True)

#         # Fetch audio options from the database
#         cursor.execute("SELECT filename, filepath FROM audio_files")
#         audio_options = cursor.fetchall()

#         # Close the database connection
#         cursor.close()
#         close_connection(conn)

#         return jsonify(audio_options)
#     except Exception as e:
#         return str(e)
import os

# import os

folder_path = 'static/downloaded_audios'
file_names = os.listdir(folder_path)

# Sort the files to ensure they are renamed in order
file_names.sort()

# Counter for new names starting from 1
counter = 1

for filename in file_names:
    # Create the new file name with the counter and ".mp3" extension
    new_filename = 'audio_'+str(counter) + '.mp3'  # Using zfill to pad with zeros (e.g., 001.mp3)

    # Construct the full paths
    old_path = os.path.join(folder_path, filename)
    new_path = os.path.join(folder_path, new_filename)

    # Rename the file
    os.rename(old_path, new_path)

    # Increment the counter for the next file
    counter += 1


# folder_path = 'static/downloaded_audios'
# file_names = os.listdir(folder_path)

# # Sort the files to ensure they are renamed in order
# file_names.sort()

# # Counter for new names starting from 1
# counter = 1
# file_extension = mp3
# for filename in file_names:
#     # Get the file extension
#     _, file_extension = os.path.splitext(filename)

#     # Create the new file name with the counter
#     new_filename = str(counter) + file_extension

#     # Construct the full paths
#     old_path = os.path.join(folder_path, filename)
#     new_path = os.path.join(folder_path, new_filename)

#     # Rename the file
#     os.rename(old_path, new_path)

#     # Increment the counter for the next file
#     counter += 1


import shutil
import tkinter as tk
from tkinter import messagebox

def delete_folder(folder_path):
    try:
        # Remove the directory and all its contents
        shutil.rmtree(folder_path)
        return True, f"Folder '{folder_path}' deleted successfully!"
    except FileNotFoundError:
        return False, f"Folder '{folder_path}' not found!"
    except OSError as e:
        return False, f"Error deleting folder: {e}"

# @app.route('/logout_and_delete')
# def logout_and_delete():
#     folder_path = "static/selected_images"
#     success, message = delete_folder(folder_path)

#     if success:
#         # Redirect to index.html after successful deletion
#         return redirect(url_for('index'))
#     else:
#         return f"An error occurred: {message}"
def delete_videomp3(folder_path):
    video_path = os.path.join(folder_path, "static/merged_video.mp4")
    try:
        # Remove the video file if it exists
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Video file '{video_path}' deleted successfully!")
        else:
            print(f"Video file '{video_path}' does not exist.")
    except OSError as e:
        print(f"Error deleting folder '{folder_path}': {e}")
        return False

@app.route('/logout_and_delete')
def logout_and_delete():
    folder_path = "static/selected_images"
    success, message = delete_folder(folder_path)
    mp3_path = ""
    delete_videomp3(mp3_path)
    if success:
        # Redirect to index.html after successful deletion
        return redirect(url_for('index'))
    else:
        return f"An error occurred: {message}"



@app.route('/get_audio_path', methods=['POST'])
def get_audio_path():
    userid = session.get('userid')
    video_path_f = f'static/out_{userid}.mp4'
    print(video_path_f)
    audio_path = request.json.get('audioSrc')
    print(audio_path)
    print(video_path_f)
    video_clip = VideoFileClip(video_path_f)
    audio_clip = AudioFileClip(audio_path)
    video_with_audio = video_clip.set_audio(audio_clip)
    merged_video_path = "static/merged_video.mp4"
    os.makedirs(os.path.dirname(merged_video_path), exist_ok=True)
    video_with_audio.write_videofile(merged_video_path, codec='libx264')

    # Return the path to the merged video as JSON
    return jsonify({'merged_video_path': merged_video_path})




if __name__ == '__main__':
    # create_users_table()  # Create the users table if it doesn't exist
    # create_images_table()
    # create_audio_files()

    app.run(debug=True, port=5007)
