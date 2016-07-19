import boto3

json_content =  [ {
        'Id': '1',
        'MessageBody': 'world'
    },
    {
        'Id': '2',
        'MessageBody': 'boto3',
        'MessageAttributes': {
            'Author': {
                'StringValue': 'Daniel',
                'DataType': 'String'
            }
        }
    }]

sqs = bot3.resource('sqs')
queue = sqs.create_queue(QueueName='Q', Attributes={'DelaySeconds':'5'})
response = queue.send_message(Entries = json_content)

print (response.get('MessageId'))

for message in queue.receive_messages(MessageAttributeNames=['Author']): # author is optional. interesting! this will retrieve all the message from queue!
    # Get the custom author message attribute if it was set
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get('Author').get('StringValue')
        if author_name:
            author_text = ' ({0})'.format(author_name)

    # Print out the body and author (if set)
    print('Hello, {0}!{1}'.format(message.body, author_text))

    # Let the queue know that the message is processed
    message.delete()
