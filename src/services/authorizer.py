class Authorizer:

    def authenticate(self, token):

        if token == "mysecretpassword":
            return make_authorization("Allow")
        else:
            return make_authorization("Deny")

    def make_authorization(self, effect):
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": effect,
                        "Resource": "arn:aws:execute-api:eu-west-3:*"
                    }
                ]
            }
        }
