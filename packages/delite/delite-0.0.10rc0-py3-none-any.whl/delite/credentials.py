class Credentials:
    def __init__(self, access_key=None, access_secret=None, session_token=None):
        self.access_key = access_key
        self.access_secret = access_secret
        self.session_token = session_token

        if self.session_token is None and (self.access_key is None or self.access_secret is None):
            raise Exception("Access key and secret are required unless session token is provided")

    def use(self):
        if self.session_token is not None:
            return "s3_session_token={}".format(
                self.session_token)

        return "s3_access_key_id={}&s3_secret_access_key={}".format(
            self.access_key, self.access_secret)
