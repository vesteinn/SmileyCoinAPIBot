import json
import subprocess

from django.conf import settings

location = getattr(settings, 'SMILEYCOIN_CLI_LOCATION', '/usr/local/bin/')
GET_BLOCK_HASH = location + 'smileycoin-cli getblockhash {}'
GET_BLOCK = location + 'smileycoin-cli getblock {}'
GET_TRANS = location + 'smileycoin-cli getrawtransaction {}'
DECODE_TRANS = location + 'smileycoin-cli decoderawtransaction {}'


def cli(tag, data):
    try:
        ret  = subprocess.check_output(
            tag.format(data).split(),
            stderr=subprocess.DEVNULL
        )
    except ValueError:
        ret = '{}'
    return ret


def c(v):
    return str(v)[2:-3]

def co(v):
    return json.loads(v.replace('\\n',''))


def get_block_hash(data):
    return c(cli(GET_BLOCK_HASH, data))


def get_block(data):
    d = c(cli(GET_BLOCK, data))
    return co(d)


def decode_trans(data):
    return cli(DECODE_TRANS, data)


def get_transaction(data):
    d = c(decode_trans(c(cli(GET_TRANS, data))))
    return co(d)
