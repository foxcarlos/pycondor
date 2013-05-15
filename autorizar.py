import tweepy
consumer_key = "wz6LRrWGEj0cfOsSqNKLg"
consumer_secret = "JQUF9IFiFOpzjpTKYxsbKl5QV6o0baoD37fxFpBEE"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth_url = auth.get_authorization_url()
print auth_url
pin = raw_input('Ingrese el PIN:')
auth.get_access_token(pin)
print "access_key = '%s'" % (auth.access_token.key)
print "access_secret = '%s'" % (auth.access_token.secret)

