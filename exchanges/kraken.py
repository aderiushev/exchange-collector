import requests

class Kraken:
  def getAssetPairs():

    try:
      response = requests.get('https://api.kraken.com/0/public/AssetPairs', verify=False).json()

      if response['error']:
        # TODO: process error
        pass
      else:
        result = {}
        for index, (key, item) in enumerate(response['result'].items()):
          result[key] = { 'from': item['base'], 'to': item['quote'] }
        return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

  def getFilename(pairs):
    return 'kraken-%s' % pairs.lower()

  def getTickers(pairs):

    try:
      response = requests.get('https://api.kraken.com/0/public/Ticker', params={ 'pair': pairs, }, verify=False).json()
      if response['error']:
        # TODO: process error
        pass
      else:
        result = {}
        for index, (key, item) in enumerate(response['result'].items()):
          result[key] = { 'ask': '%.8f' % float(item['a'][0]), 'bid': '%.8f' % float(item['b'][0]), 'volume': '%.8f' % float(item['v'][0]) }
        return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass