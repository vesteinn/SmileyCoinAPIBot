# SmileyCoin blockchain scraper and API

This is a simple python / django application that utilises the smileycoin-cli interface to populate a relational
database with the block chain information.

The database can be queried using the django ORM or a web based API.

You probably need to set the directory of `smileycoin-cli` in the settings file, as with the database described below, to `SMILECOIN_CLI_LOCATION`. It
defaults to `/usr/local/bin/`.

A simple Twitter client is also built in.

![Smiley Coin API](https://github.com/vesteinn/SmileyCoinPythonAPIBot/blob/master/api.png)

## Prerequisites and setup

### Smileycoin server

You need to have a local `smileycoin-daemon` server running and `smileycoin-cli` setup, see https://tutor-web.info/smileycoin/download.

If you are starting it up for the first time make sure the configuration has `txindex=1` set.

### Postgres database and initialization

Setup an empty database that you can write to and configure `smileychain/local_settings.py` with the connection information.

Use a virtual environment or the like to install the packages in `requirements.txt` with `pip install -r requirements`.

Migrate the database with `python manage.py migrate`.

Note: You may be able use file based sqlite database but it is not recomended for anything but simple testing.

## Scraping

To populate the database with the blockchain information simply run

`python manage.py scrape FROM_BLOCK TO_BLOCK`

You can use `smileycoin-cli getblockchaininfo` to fetch the highest available block number.

## Local webserver and api

Simply run `python manage.py runserver` and open up the website mentioned
in your browser.

![Smiley Coin API](https://github.com/vesteinn/SmileyCoinPythonAPIBot/blob/master/search.png)

## Production or external use setup

A production ready configuration can be setup with e.g. nginx and gunicorn. You might want to do this with a `docker-compose` file using a pre built database/image which may be suplied at a later time.

## Twitter bot

Some simple functionality to extract OP_RETURN messages is included. See the the `twitter` folder for relevant code.

Use the management command `python manage.py op_return` to scrape interesting op return messages from the chain. These
can be viewed at something similar to `http://127.0.0.1:8000/op_returns/`.

To set up a twitter bot, first create a user and a new app with the keys needed. Then in the settings file or your local_settings 
populate 

```
TWITTER_API_KEY = ""
TWITTER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""
```

To post new OP_RETURN messages to your account simply run

`python manage.py update_twitter`

To see how it can look checkout https://twitter.com/return_op

![SmileyCoin Twitter](https://github.com/vesteinn/SmileyCoinPythonAPIBot/blob/master/twitter.png)

![Smiley Coin API](https://github.com/vesteinn/SmileyCoinPythonAPIBot/blob/master/opreturn.png)

## Future possibilities

### Web based smileycoin-cli
For educational purposes it might be of interest to setup a fully functioning web based
command line interface against the database or local SmileyCoin server using the same syntax and appearance as `smilecoin-cli`, as long as input is sanitized and wallets individualized.

