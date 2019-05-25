from market_maker import bitmex
from market_maker.settings import settings
from time import sleep
import os
import sys
import math
# Helpers
# help(bitmex.BitMEX)
bitmex = bitmex.BitMEX(base_url  = settings.BASE_URL,
                       symbol    = settings.SYMBOL,
                       apiKey    = settings.API_KEY,
                       apiSecret = settings.API_SECRET,
                       orderIDPrefix = settings.ORDERID_PREFIX,
                       postOnly  = settings.POST_ONLY,
                       timeout   = settings.TIMEOUT)

# total position available
def print_ret():
    cur_px = bitmex.ticker_data()['last']
    pos_ret, neg_ret = 0, 0
    k = 2.0 ** (-1/5)
    while(True):
        sleep(60)
        cur_px, prev_px = bitmex.ticker_data()['last'], cur_px
        ret = (cur_px/prev_px - 1)
        if ret > 0:
            pos_ret = pos_ret * k + ret * (1 -k)
        elif ret < 0:
            neg_ret = neg_ret * k - ret * (1 -k)    
        print('return: {}, neg_ret: {}, pos_ret: {}'.format(ret, pos_ret, neg_ret))

def _test():
    try:
        print_ret()
    except(KeyboardInterrupt, SystemExit):
        sys.exit()

if __name__ == '__main__':
    _test()
