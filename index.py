import boto3
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
app = Flask(__name__)

dynamodb_table = None

def init_db():
    global dynamodb_table
    dynamodb = boto3.resource(
        'dynamodb',
        aws_access_key_id=os.getenv("aws_access_key_id"),
        aws_secret_access_key=os.getenv("aws_secret_access_key"),
        region_name="eu-north-1"
    )
    dynamodb_table = dynamodb.Table('projectH_db')
    print("Table Status: ", dynamodb_table.table_status)

@app.route('/')
def home():
    return "Welcome to the DynamoDB Flask App!"

@app.route('/item', methods=['POST'])
def add_item():
    data = request.json
    dynamodb_table.put_item(Item=data)
    return jsonify({"message": "Item added", "item": data}), 201

@app.route('/item/<id>', methods=['GET'])
def get_item(id):
    response = dynamodb_table.get_item(Key={'id': id})
    item = response.get('Item')
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)