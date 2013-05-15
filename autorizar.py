import tweepy
consumer_key = "wz6LRrWGEj0cfOsSqNKLg"
consumer_secret = "JQUF9IFiFOpzjpTKYxsbKl5QV6o0baoD37fxFpBEE"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth_url = auth.get_authorization_url()
print auth_url
