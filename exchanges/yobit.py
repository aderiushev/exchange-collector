import requests

class Yobit:
  def getAssetPairs():
    try:
      response = requests.get('https://yobit.net/api/3/info', verify=False).json()

      result = {}
      for index, (key, item) in enumerate(response['pairs'].items()):
        fromTo = key.split('_')
        result[key] = { 'from': fromTo[0].upper(), 'to': fromTo[1].upper() }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

  def getFilename(pairs):
    return 'yobit-%s' % pairs.lower().replace('_', '-')

  def getTickers(pairs):
    try:
      response = requests.get('https://yobit.net/api/3/ticker/%s' % '-'.join(pairs.split(',')), verify=False).json()

      result = {}
      for index, (key, item) in enumerate(response.items()):
        result[key] = { 'ask': '%.8f' % item['sell'], 'bid': '%.8f' % item['buy'], 'volume': '%.8f' % item['vol'] }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

    return assetPairs