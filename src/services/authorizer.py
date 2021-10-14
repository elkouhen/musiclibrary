class Authorizer:

    def authenticate(self, account, token):

        if token == "mysecretpassword":
            authorization = self.make_authorization("Allow", account)
            print(authorization)
            return authorization
        else:
            authorization = self.make_authorization("Deny", account)
            print(authorization)
            return authorization

    def make_authorization(self, effect, account):

        response = {}

        response["principalId"] = "user"
        response["policyDocument"] = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "InvokeStatement",
                    "Effect": effect,
                    "Action": "execute-api:Invoke",
                    "Resource": f"arn:aws:execute-api:eu-west-3:{account}:*"
                }
            ]
        }

        return response
