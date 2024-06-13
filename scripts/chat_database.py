import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime

# Cria uma conexão com o DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ChatMessages')

def save_message(message_id, user_id, content, is_bot, chat_id):
    timestamp = datetime.utcnow().isoformat()
    table.put_item(
        Item={
            'MessageID': message_id,
            'Timestamp': timestamp,
            'UserID': user_id,
            'Content': content,
            'IsBot': is_bot,
            'ChatID': chat_id
        }
    )

def get_messages(chat_id):
    response = table.query(
        IndexName='ChatID-Timestamp-index',  # Se você tiver um índice global secundário
        KeyConditionExpression=Key('ChatID').eq(chat_id)
    )
    return response['Items']
