# SmileyCoin blockchain scraper and API

This is a simple python / django application that utilises the smileycoin-cli interface to populate a relational
database with the block chain information. A simple Twitter client is also built in.

The database can be queried using the django ORM or a web based API.

You probably need to set the directory of `smileycoin-cli` in the settings file, as with the database described below, to `SMILECOIN_CLI_LOCATION`. It defaults to `/usr/local/bin/`.

![Smiley Coin API](https://github.com/vesteinn/SmileyCoinPythonAPIBot/blob/master/api.png)

The project is a final project in the course Crypotcurrencies STÆ532M2019H. Work is done by ves4 and ava7.

## Why?

* To create an infrastructure to support quick development on top of the SmileyCoin blockchain, querying a relational database for analytics or information is much more efficient than targeting the blockchain directly.
* To create a Twitter bot that scans OP_RETURN values on transactions and posts them, maintaining a history of already posted messages and messages that do not nicely convert into ASCII.

## Prerequisites and setup

### Smileycoin server

You need to have a local `smileycoin-daemon` server running and `smileycoin-cli` setup, see https://tutor-web.info/smileycoin/download.

If you are starting it up for the first time make sure the configuration has `txindex=1` set.

### Postgres database and initialization

Setup an empty database that you can write to and configure `smileychain/local_settings.py` with the connection information.

Use a virtual environment or the like to install the packages in `requirements.txt` with `pip install -r requirements.txt`.

Migrate the database with `python manage.py migrate`, this set's up relevant tables and modifications.

Note: You may be able use a file based sqlite database but it is not recomended for anything but simple testing.

## Scraping

To populate the database with the blockchain information simply run

`python manage.py scrape FROM_BLOCK TO_BLOCK`

You can use `smileycoin-cli getblockchaininfo` to fetch the highest available block number.

## Local webserver and api

Simply run `python manage.py runserver` and open up the website mentioned in your browser (default http://127.0.0.1:8000/). This exposes a web interface for the REST api which enables navigation of some endpoints corresponding to tables in the database or models accesible through the Django ORM.

```json
{
    "blocks": "http://127.0.0.1:8000/blocks/",
    "transactions": "http://127.0.0.1:8000/transactions/",
    "vouts": "http://127.0.0.1:8000/vouts/",
    "vins": "http://127.0.0.1:8000/vins/",
    "addresses": "http://127.0.0.1:8000/addresses/",
    "op_returns": "http://127.0.0.1:8000/op_returns/"
}
```

Some of these have filter and search options built in that can be easily extended or configured as per the Django REST Framework documentation at https://www.django-rest-framework.org (see `./block/api/views.py`).

![Smiley Coin API](https://github.com/vesteinn/SmileyCoinPythonAPIBot/blob/master/search.png)

## Interactive shell

Run `python manage.py shell` or `python manage.py shell_plus` to open up the Django shell with models and modules loaded for direct and efficient interaction with the ORM and db. E.g.

```json
In [1]: OpReturn.objects.filter(message__icontains="hello").count()
Out[1]: 23

In [2]: OpReturn.objects.filter(message__icontains="hello").last().message
Out[2]: 'hello :)'
```

## Production or external use setup

A production ready configuration can be setup with e.g. nginx and gunicorn. You might want to do this with a `docker-compose` file using a pre built database/image which may be suplied at a later time.

## Twitter bot

Some simple functionality to extract OP_RETURN messages and post to Twitter (using tweepy) is included. See the the `twitter` folder for relevant code.

Use the management command `python manage.py op_return` to scrape interesting op return messages from the chain. These
can be viewed at something similar to `http://127.0.0.1:8000/op_returns/`.

To set up a twitter bot, first create a user and a new app with the keys needed. Then in the settings file or your local_settings populate 

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

### Scrape, update op_return and push

To update the database, parse incoming blocks and push to twitter, run (see `./twitter/management/command/check_and_update.py`)

`python manage.py check_and_update`

This is a good candidate for something to run in cron. To run every 10 minutes, run `crontab -e` and add:

```
*/10 * * * * /home/user/.virtualenvs/smiley/bin/python /home/user/SmileycoinAPIBot/smileychain/manage.py check_and_update >& /tmp/smly.log
```


## Future possibilities

### Web based smileycoin-cli
For educational purposes it might be of interest to setup a fully functioning web based
command line interface against the database or local SmileyCoin server using the same syntax and appearance as `smilecoin-cli`, as long as input is sanitized and wallets individualized.

### Cleaner implementation
Using the RPC interface.

