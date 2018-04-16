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

      response = requests.get('https://api.livecoin.net/exchange/ticker', verify=False).json()

      result = {}
      for index, item in enumerate(response):
        if item['symbol'] in pairsArray:
          result[item['symbol']] = { 'ask': '%.8f' % item['best_ask'], 'bid': '%.8f' % item['best_bid'], 'volume': '%.8f' % item['volume'] }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

    return assetPairs