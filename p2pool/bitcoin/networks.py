import os
import platform

from twisted.internet import defer

from . import data
from p2pool.util import math, pack
from operator import *

def get_milansubsidy(mnHeight):
    if mnHeight < 250000:     
        nSubsidy = 40
    elif mnHeight < 500000:
        nSubsidy = 25 
    elif mnHeight < 750000:
        nSubsidy = 10
    elif mnHeight < 2000000:
        nSubsidy = 5
    else:
        nSubsidy = 2

    return int(nSubsidy * 1000000)
	
def get_subsidy(nCap, nMaxSubsidy, bnTarget):
    bnLowerBound = 0.01
    bnUpperBound = bnSubsidyLimit = nMaxSubsidy
    bnTargetLimit = 0x00000fffff000000000000000000000000000000000000000000000000000000

    while bnLowerBound + 0.01 <= bnUpperBound:
        bnMidValue = (bnLowerBound + bnUpperBound) / 2
        if pow(bnMidValue, nCap) * bnTargetLimit > pow(bnSubsidyLimit, nCap) * bnTarget:
            bnUpperBound = bnMidValue
        else:
            bnLowerBound = bnMidValue

    nSubsidy = round(bnMidValue, 2)

    if nSubsidy > bnMidValue:
        nSubsidy = nSubsidy - 0.01

    return int(nSubsidy * 1000000)

def debug_block_info(dat1):
	print 'block header',  data.block_header_type.unpack(dat1)['timestamp']
	return 0

nets = dict(
    milancoin=math.Object(
        P2P_PREFIX='facbb0dc'.decode('hex'),
        P2P_PORT=8663,
        ADDRESS_VERSION=50,
        RPC_PORT=8662,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'ilancoinaddress' in (yield bitcoind.rpc_help()) and
            not (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda height: get_milansubsidy(height),
        BLOCKHASH_FUNC=lambda header: pack.IntType(256).unpack(__import__('yac_scrypt').getPoWHash(header, data.block_header_type.unpack(header)['timestamp'])),
        POW_FUNC=lambda header: pack.IntType(256).unpack(__import__('yac_scrypt').getPoWHash(header, data.block_header_type.unpack(header)['timestamp'])),
        BLOCK_PERIOD=60, # s
        SYMBOL='MLC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'milancoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/milancoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.milancoin'), 'milancoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://milancoin.org/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://milancoin.org/address/',
        SANE_TARGET_RANGE=(2**256//2**20//1000 - 1, 2**256//2**20 - 1),
    ),

    milancoin_testnet=math.Object(
        P2P_PREFIX='fbc8b7dc'.decode('hex'),
        P2P_PORT=8663,
        ADDRESS_VERSION=78,
        RPC_PORT=8662,
        RPC_CHECK=defer.inlineCallbacks(lambda bitcoind: defer.returnValue(
            'ilancoinaddress' in (yield bitcoind.rpc_help()) and
            (yield bitcoind.rpc_getinfo())['testnet']
        )),
        SUBSIDY_FUNC=lambda target: get_subsidy(6, 10, target),
        BLOCKHASH_FUNC=lambda data: pack.IntType(256).unpack(__import__('yac_scrypt').getPoWHash(data)),
        POW_FUNC=lambda data: pack.IntType(256).unpack(__import__('yac_scrypt').getPoWHash(data)),
        BLOCK_PERIOD=60, # s
        SYMBOL='MLC',
        CONF_FILE_FUNC=lambda: os.path.join(os.path.join(os.environ['APPDATA'], 'MilanCoin') if platform.system() == 'Windows' else os.path.expanduser('~/Library/Application Support/YbCoin/') if platform.system() == 'Darwin' else os.path.expanduser('~/.milancoin'), 'milancoin.conf'),
        BLOCK_EXPLORER_URL_PREFIX='http://nonexistent-milancoin-testnet-explorer/block/',
        ADDRESS_EXPLORER_URL_PREFIX='http://nonexistent-milancoin-testnet-explorer/address/',
        SANE_TARGET_RANGE=(2**256//1000000000 - 1, 2**256//1000 - 1),
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
