from flask import *
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import boto3
from datetime import datetime
from mysql.connector import pooling







app = Flask(__name__, static_folder="public")
load_dotenv()

dbconfig = {
    "host": os.getenv("DB_HOST"),  
    "user": os.getenv("DB_USER"),  
    "password": os.getenv("DB_PASSWORD"), 
    "database": os.getenv("DB_DATABASE"),
}
db_pool= pooling.MySQLConnectionPool(pool_name="mypool", pool_size=32, **dbconfig)

aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
region_name = os.environ.get('AWS_REGION')
bucket_name = 'messageboard-image1'
s3 = boto3.client('s3',
                 aws_access_key_id=aws_access_key_id,
                 aws_secret_access_key=aws_secret_access_key,
                 region_name=region_name)


@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    message = request.form['message']
    image = request.files['image']

    if image:
        current_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        s3_path = f'imgs/{current_time}_{secure_filename(image.filename)}'
        s3.upload_fileobj(image, bucket_name, s3_path)
        # s3_url = f'https://{bucket_name}.s3.amazonaws.com/{s3_path}'
        s3_url = f'https://d194z2ip41naor.cloudfront.net/{s3_path}'

        print("s3_path:",s3_path)
        print("s3_url:",s3_url)
        try:
            
            db_conn = db_pool.get_connection()
            cursor = db_conn.cursor()

            insert_sql = "INSERT INTO messages (message, imageurl) VALUES (%s, %s)"
            cursor.execute(insert_sql, (message, s3_url))
            db_conn.commit()

        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})

        finally:
            if db_conn:
                db_conn.close()


        return jsonify({"status": "success", "image_url": s3_url})
        
    return jsonify({"status": "error", "message": "No image uploaded"})


@app.route('/getmessages', methods=['GET'])
def get_messages():
    try:

        db_conn = db_pool.get_connection()
        cursor = db_conn.cursor()

        query = "SELECT * FROM messages ORDER BY id DESC"

        cursor.execute(query)
        messages = cursor.fetchall()
        


        cursor.close()
        db_conn.close()
        print("messages:",messages)

        return jsonify({"ok": True,"messages": messages}),200

    except Exception as e:
        
        return jsonify({"error": str(e)})






app.run(host="0.0.0.0", port=3333)














