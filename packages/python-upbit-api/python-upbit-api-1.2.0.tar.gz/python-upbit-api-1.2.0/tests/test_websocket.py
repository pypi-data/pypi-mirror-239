from upbit.websoket import BlockingWebSocket

ws = BlockingWebSocket(req=[{"ticket":"test"},{"type":"ticker","codes":["KRW-BTC"]}])