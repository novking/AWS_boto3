
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

    def _subscribe_topic_activity(self, task):
            activity_data = { "topic_arn": None, "email": {"endpoint" : None, "SubscriptionArn" : None}, "sms": {"endpoint" : None, "SubscriptionArn" : None} }
            if task:
                input = json.loads(task)
                activity_data["email"]["endpoint"] = input["email"]
                activity_data["sms"]["endpoint"] = input["sms"]
            else:
                self.fail(reason=json.dumps({"reason", "Didn't receive any input!", "detail", "" }))
                return False, "Didn't receive any input!"

            sns_client = sns.SNSConnection(aws_access_key_id=ACCESS, aws_secret_access_key=SECRET)

            # Create the topic and get the ARN
            result, activity_data["topic_arn"] = self._create_topic(sns_client)
            if result:
                    # Subscribe the user to the topic, using either or both endpoints.
                    for protocol in ["email", "sms"]:
                        ep = activity_data[protocol]["endpoint"]
                        if (ep):
                            print("About to subscribe protocol: " + protocol + " ep: " + ep)
                            response = sns_client.subscribe(activity_data["topic_arn"], protocol, ep)
                            print(response)
                            activity_data[protocol]["SubscriptionArn"] = response['SubscribeResponse']['SubscribeResult']["SubscriptionArn"]
                    # If at least one subscription arn is set, consider this a success.
                    if (activity_data["email"]["SubscriptionArn"] != None) or (activity_data["sms"]["SubscriptionArn"] != None):
                        self.complete(result=json.dumps(activity_data))
                        return True, json.dumps(activity_data)
                    else:
                        self.fail(reason=json.dumps({ "reason" : "Couldn't subscribe to SNS topic", "detail" : "" }))
                        return False, "Couldn't subscribe to SNS topic"
            else:
                return False, "Couldn't create SNS topic"

if __name__ == '__main__':
    st = SNSTopicCreator()
