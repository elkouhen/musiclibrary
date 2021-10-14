class Authorizer:

    def authenticate(self, token):

        if token == "mysecretpassword":
            return self.make_authorization("Allow")
        else:
            return self.make_authorization("Deny")

    def make_authorization(self, effect):
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": effect,
                        "Resource": "arn:aws:lambda:eu-west-3:*"
                    }
                ]
            }
        }
