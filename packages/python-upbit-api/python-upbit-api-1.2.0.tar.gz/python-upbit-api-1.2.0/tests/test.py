import logging
import pprint
import time

from upbit import Upbit

# upbit = Upbit('lxioiqBwiW9HiMAE9F65HweqGB1qzIxRazE8q557', 'RTe81YmsW1C01XT7tMvYPw9wx8NDf9FlhpGt1UNx')
# res = upbit.get_deposits(currency='KRW')
# res = upbit.get_deposits(txids=['307176bd3a81e4d9ca5a9dd1f5fa70b1dd3de567901b5419fab17471633e5555'])
# res = upbit.get_wallet_status()
# res = upbit.create_coin_address('BTC', net_type='BTC')
# pprint.pprint(res.json())


from upbit.websoket import BlockingWebSocket, BackgroundWebSocket
import asyncio


def on_msg(ws, data):
    print(data)
    # ws.close()
#
#
# ws = BlockingWebSocket([{"type": "trade", "codes": ["KRW-BTC"]}, {"type": "orderbook", "codes": ["KRW-ETH"]}],
#                     on_message=on_msg)
#
# ws.start()


async def main():
    ws = BackgroundWebSocket([{"type": "trade", "codes": ["KRW-BTC"]}, {"type": "orderbook", "codes": ["KRW-ETH"]}],
                             on_message=on_msg)
    ws.start()
    print(1)
    # time.sleep(10)
    # ws.close()

# async def main():
#     for i in range(6):
#         ws = BackgroundWebSocket([{"type": "trade", "codes": ["KRW-BTC"]}, {"type": "orderbook", "codes": ["KRW-ETH"]}],
#                              on_message=on_msg)
#         ws.start()
#         print(i)


if __name__ == '__main__':
    print(0)
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(threadName)20s | %(name)25s | %(levelname)7s | %(message)s (%(filename)s:%(lineno)d %(funcName)s())")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    print(2)
    loop.run_forever()
    print(3)
