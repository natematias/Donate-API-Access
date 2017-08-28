Donate-API-Access

This software invites people to donate Twitter API access to a research project, storing the API access information to a text file for importing into a project that can multiplex API access to query data at larger scales than allowed by a single API key.

Based on software by @whichlight:
find a more in depth blog post here:
http://whichlight.com/blog/twitter-oauth-in-python-with-tweepy-and-flask/

If you're going to develop something based on this, you should also set up your server for HTTPS, either [within flask](http://flask.pocoo.org/snippets/111/) or [at the proxy layer](https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https).
