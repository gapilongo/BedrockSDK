from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load AWS credentials from environment variables
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


# Initialize Boto3 client with environment variables
client = boto3.client(
    service_name="bedrock-agent-runtime",
    region_name='us-east-1',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
)

def retrieve_and_generate(model_arn, knowledge_base_id, query):
    config = {
        'input': {'text': query},
        'retrieveAndGenerateConfiguration': {
            'type': 'KNOWLEDGE_BASE',
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledge_base_id,
                'modelArn': model_arn,
            }
        }
    }

    response = client.retrieve_and_generate(**config)
    return response

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.json
    model_arn = data.get('model_arn')
    knowledge_base_id = data.get('knowledge_base_id')
    query = data.get('query')
    response = retrieve_and_generate(model_arn, knowledge_base_id, query)
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8084)
