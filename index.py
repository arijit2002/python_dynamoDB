import boto3
import os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask

app = Flask(__name__)

def init_db():
    dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=os.getenv("aws_access_key_id"),
    aws_secret_access_key=os.getenv("aws_secret_access_key"),
    region_name="eu-north-1"
    )

    table= dynamodb.Table('projectH_db')
    print("Table Status: ", table.table_status)

    table.put_item(
        Item={
            'id': '456',
            'name': 'Arijit',
            'msg': 'Testing2'
        }
    )

    response = table.get_item(
     Key={'id': '456'}
    )

    print(response.get('Item'))
    
@app.route('/')
def home():
    return "Welcome to the DynamoDB Flask App!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)