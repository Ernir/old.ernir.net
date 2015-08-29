This is Eiríkur Ernir Þorsteinsson's personal webpage. Done in Django 1.8.

A live version can be found at [eirikur.ernir.net](http://eirikur.ernir.net/), hosted with [Heroku](http://heroku.com/).

Setup notes: a few config vars and other externals need to be set.

    SECRET_KEY - App secret key
    DEBUG_MODE - Boolean

Several variables for social authentication, see docs for respective providers:

    ERNIRNET_FB_APP_ID
    ERNIRNET_FB_APP_SECRET
    ERNIRNET_GOOGLE_APP_ID
    ERNIRNET_GOOGLE_APP_SECRET
    ERNIRNET_TWITTER_APP_ID
    ERNIRNET_TWITTER_APP_SECRET

And a Postgres DB connection URL:

    ERNIRNET_DB_URL
