import requests

class Livecoin:
  def getAssetPairs(self):
    try:
      response = requests.get('https://api.livecoin.net/exchange/ticker').json()
      result = {}
      for index, item in enumerate(response):
        fromTo = item['symbol'].split('/')
        result[item['symbol']] = { 'from': fromTo[0].upper(), 'to': fromTo[1].upper() }

      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

  def getFilename(self, pairs):
    if pairs:
      return 'livecoin-%s' % pairs.lower().replace('/', '-')
    else:
      return 'livecoin-all'

  def getTickers(self, pairs, mode):
    try:
      result = {}

      if mode == 'ticker':
        response = requests.get('https://api.livecoin.net/exchange/ticker').json()

        for index, item in enumerate(response):
          if item['symbol'] in pairs:
            result[item['symbol']] = {
              'ask': {
                'value': '%.8f' % item['best_ask'],
                'volume': None
              },
              'bid': {
                'value': '%.8f' % item['best_bid'],
                'volume': None
              }
            }
      else:
        response = requests.get('https://api.livecoin.net/exchange/all/order_book?depth=1', verify=False).json()

        for index, (key, item) in enumerate(response.items()):
          if key in pairs:
            result[key] = {
              'ask':
                {
                  'value': '%.8f' % float(item['asks'][0][0]) if len(item['asks']) > 0 else None,
                  'volume': '%.8f' % float(item['asks'][0][1]) if len(item['asks']) > 0 else None
                },
              'bid':
                {
                  'value': '%.8f' % float(item['bids'][0][0]) if len(item['bids']) > 0 else None,
                  'volume': '%.8f' % float(item['bids'][0][1]) if len(item['bids']) > 0 else None
                }
            }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass