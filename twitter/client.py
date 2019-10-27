import tweepy

from django.conf import settings


class TwitterClient():
    def __init__(self):
        self.auth = tweepy.OAuthHandler(
            settings.TWITTER_API_KEY,
            settings.TWITTER_API_SECRET
        )
        self.auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN,
            settings.TWITTER_ACCESS_TOKEN_SECRET
        )

    def authenticate(self):
        self.api = tweepy.API(self.auth)
        self.api.verify_credentials()

    def post(self, message):
        self.api.update_status(message)