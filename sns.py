
import boto.sns as sns
import access_file
import json

ACCESS = access_file.access_key_ID
SECRET = access_file.secret_access_key
DisplayName = AwesomeAaron

class  SNSTopicShell:
    def fail(self, reason):
        print (reason)

    def complete(self, result):
        print (result)

class SNSTopicCreator(SNSTopicShell):
    def _create_topic(self, sns_client):
        t = sns_client.create_topic('SNS_testing_topic')
        print (t)
        topic_arn = t['CreateTopicResponse']['CreateTopicResult']['TopicArn']

    if topic_arn:
                sns_client.set_topic_attributes(topic_arn, DisplayName, 'SNSSample')
    else:
        self.fail(reason=json.dumps({"reason", "Couldn't create SNS topic", "detail", "" }))
        return False, "Couldn't create SNS topic"
    return True, topic_arn

if __name__ == '__main__':
    st = SNSTopicCreator()
