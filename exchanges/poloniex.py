import requests

class Poloniex:
  def getAssetPairs():
    try:
      response = requests.get('https://poloniex.com/public?command=returnTicker', verify=False).json()

      result = {}
      for index, (key, item) in enumerate(response.items()):
        fromTo = key.split('_')
        result[key] = { 'from': fromTo[0].upper(), 'to': fromTo[1].upper() }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

  def getFilename(pairs):
    return 'poloniex-%s' % pairs.lower().replace('_', '-')

  def getTickers(pairs):
    try:
      pairsArray = pairs.split(',')
      response = requests.get('https://poloniex.com/public?command=returnTicker', verify=False).json()

      result = {}
      for index, (key, item) in enumerate(response.items()):
        if key in pairsArray:
          result[key] = { 'ask': '%.8f' % float(item['lowestAsk']), 'bid': '%.8f' % float(item['highestBid']), 'volume': '%.8f' % float(item['baseVolume']) }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

    return assetPairs