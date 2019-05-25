from market_maker.market_maker import *
from datetime import datetime
from market_maker.utils import log, constants, errors, math
logger = log.setup_custom_logger('root')

class MyOrderManager(OrderManager):
    def __init__(self):
        # sys.stdout.write("MyOrderManager is born!\n")
        self.ema_t = 5
        self.size_mul = 0.05 # start with 0.15 size
        self.lambda_  = 2.0 ** (-1 / self.ema_t)
        self.prev_px, self.cur_px = 0, 0
        # neg_ret and pos_ret is the past 5 min ret mean
        self.ret_t = 5
        self.neg_ret, self.pos_ret = 0, 0
        self.prev_time, self.cur_time = datetime.now(), datetime.now()
        OrderManager.__init__(self)

    def update_ret(self):
        self.cur_px, self.prev_px = self.exchange.get_ticker()['last'], self.cur_px
        self.prev_time, self.cur_time = self.cur_time, datetime.now()
        num_t = self.ret_t * 60 / (self.cur_time - self.prev_time).total_seconds()
        ret  = self.cur_px / self.prev_px - 1 if self.prev_px else 0
        ret *= num_t
        if ret > 0:
            self.pos_ret = self.pos_ret * self.lambda_ + ret * (1 -self.lambda_)
        elif ret < 0:
            self.neg_ret = self.neg_ret * self.lambda_ - ret * (1 -self.lambda_)
        print('return: {}, neg_ret: {}, pos_ret: {}'.format(ret, self.pos_ret, self.neg_ret))

    def my_place_orders(self):
        """Create order items for use in convergence."""
        fund = self.exchange.get_margin()
        ticker = self.exchange.get_ticker()
        instrument = self.exchange.get_instrument()
        tickSize = instrument['tickSize']
        # inorder to determine spread, one need to update return first
        self.update_ret()
        buy_px  = [math.toNearest(ticker["buy"]  * (1 - i * self.neg_ret) - tickSize, tickSize) for i in [1, 1.5, 2, 3, 5]]
        sell_px = [math.toNearest(ticker["sell"] * (1 + i * self.pos_ret) + tickSize, tickSize) for i in [1, 1.5, 2, 3, 5]]
        # total_available = 0
        if self.exchange.dry_run:
            total_available = fund['availableFunds'] / (self.instrument['highPrice'] * self.instrument['initMargin'])
        else:
            total_available = fund['availableMargin'] / (self.instrument['highPrice'] * self.instrument['initMargin'])
        qty_list = [1, 1.5, 2, 3, 5]
        qty_unit = math.toNearest(self.size_mul * total_available / sum(qty_list), 50)
        buy_qty  = [i*qty_unit for i in qty_list]
        sell_qty = [i*qty_unit for i in qty_list]
        buy_orders  = [{'price': price, 'orderQty': quantity, 'side': "Buy"} for price, quantity in zip(buy_px, buy_qty)]
        sell_orders = [{'price': price, 'orderQty': quantity, 'side': "Sell"} for price, quantity in zip(sell_px, sell_qty)]
        return self.converge_orders(buy_orders, sell_orders)

    def run_loop(self):
        # wait 3 mins before sending order
        wait_loop, cnt = 3 * 60 / settings.LOOP_INTERVAL, 0
        while True:
            sys.stdout.write("-----\n")
            sys.stdout.flush()
            self.check_file_change()
            sleep(settings.LOOP_INTERVAL)
            # This will restart on very short downtime, but if it's longer,
            # the MM will crash entirely as it is unable to connect to the WS on boot.
            if not self.check_connection():
                logger.error("Realtime data connection unexpectedly cself.lambbalosed, restarting.")
                self.restart()
            self.sanity_check()  # Ensures health of mm - several cut-out points here
            self.print_status()  # Print skew, delta, etc
            if(cnt < wait_loop):
                self.update_ret()
            else:
                self.my_place_orders()  # Creates desired orders and converges to existing orders
            cnt += 1
def run():
    # logger.info('BitMEX Market Maker Version: %s\n' % constants.VERSION)
    myom = MyOrderManager()
    # Try/except just keeps ctrl-c from printing an ugly stacktrace
    try:
        myom.run_loop()
    except(KeyboardInterrupt, SystemExit):
        sys.exit()
