class Authorizer:

    def authenticate(self, account, token):

        if token == "mysecretpassword":
            authorization = self.make_authorization("Allow")
            print(authorization)
            return authorization
        else:
            authorization = self.make_authorization("Deny")
            print(authorization)
            return authorization

    def make_authorization(self, effect):
        return {
            "principalId": "user",
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": effect,
                        "Action": "execute-api:Invoke",
                        "Resource": "arn:aws:lambda:eu-west-3:*"
                    }
                ]
            }
        }
