from p2pool.bitcoin import networks
from p2pool.util import math

# CHAIN_LENGTH = number of shares back client keeps
# REAL_CHAIN_LENGTH = maximum number of shares back client uses to compute payout
# REAL_CHAIN_LENGTH must always be <= CHAIN_LENGTH
# REAL_CHAIN_LENGTH must be changed in sync with all other clients
# changes can be done by changing one, then the other

nets = dict(
    milancoin=math.Object(
        PARENT=networks.nets['milancoin'],
        SHARE_PERIOD=10, # seconds  How often should P2Pool generate a new share (rule of thumb: 1/5 - 1/10 of the block period)
        CHAIN_LENGTH=24*60*60//10, # shares
        REAL_CHAIN_LENGTH=24*60*60//10, # shares  CHAIN_LENGTH & REAL_CHAIN_LENGTH are set up to allow for 3 Hour PPLNS.
        TARGET_LOOKBEHIND=30, # shares is set to 30 (shares) giving a 300 second (5min) difficulty adjustment.
        SPREAD=15, # blocks  because bitcoin's SPREAD=3 block every 600 seconds and litecoin's  SPREAD=12 block every 150 seconds 600/150=4 4x3=12
        IDENTIFIER='fbc8b7dcfbc8b7dc'.decode('hex'),  #some random s-it (I think its used to identify others p2pool's mining this coin)
        PREFIX='fbc8b7dcfbc8b7dd'.decode('hex'),  #IDENTIFIER & PREFIX: P2Pool will only sync with other nodes who have Identifier and Prefix matching yours (and using same p2p port).. if any of the above values change, a new identifier & prefix need to be created in order to prevent problems.
        P2P_PORT=8669,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=8668,
        BOOTSTRAP_ADDRS='67.23.234.59,'.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt-milancoin',
        VERSION_CHECK=lambda v: v >= 60004,
    ),

    milancoin_testnet=math.Object(
        PARENT=networks.nets['milancoin_testnet'],
        SHARE_PERIOD=3, # seconds
        CHAIN_LENGTH=20*60//3, # shares
        REAL_CHAIN_LENGTH=20*60//3, # shares
        TARGET_LOOKBEHIND=200, # shares
        SPREAD=12, # blocks
        IDENTIFIER='e037d5b8c7923510'.decode('hex'),
        PREFIX='7208c1a54ef649b0'.decode('hex'),
        P2P_PORT=19777,
        MIN_TARGET=0,
        MAX_TARGET=2**256//2**20 - 1,
        PERSIST=False,
        WORKER_PORT=18336,
        BOOTSTRAP_ADDRS=' '.split(' '),
        ANNOUNCE_CHANNEL='#p2pool-alt',
        VERSION_CHECK=lambda v: v >= 60004,
    ),
)
for net_name, net in nets.iteritems():
    net.NAME = net_name
