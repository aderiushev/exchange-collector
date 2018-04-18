import requests

class Livecoin:
  def getAssetPairs(self):
    try:
      response = requests.get('https://api.livecoin.net/exchange/ticker', verify=False).json()

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

  def getTickers(self, pairs):
    try:
      if pairs:
        pairsArray = pairs.split(',')
      else:
        pairsArray = self.getAssetPairs().keys()

      response = requests.get('https://api.livecoin.net/exchange/all/order_book?depth=1', verify=False).json()

      result = {}
      for index, (key, item) in enumerate(response.items()):
        if key in pairsArray:
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

    return assetPairs