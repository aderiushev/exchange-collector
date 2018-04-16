import requests

class Yobit:
  def getAssetPairs(self):
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

  def getFilename(self, pairs):
    if pairs:
      return 'yobit-%s' % pairs.lower().replace('_', '-')
    else:
      return 'yobit-all'

  def getTickers(self, pairs):
    try:
      if pairs:
        formattedPairs = pairs
      else:
        # crunch gets only first 50 pairs
        formattedPairs = ','.join(list(self.getAssetPairs().keys())[0:50])

      response = requests.get('https://yobit.net/api/3/ticker/%s' % '-'.join(formattedPairs.split(',')), verify=False).json()

      result = {}
      for index, (key, item) in enumerate(response.items()):
        result[key] = { 'ask': '%.8f' % item['sell'], 'bid': '%.8f' % item['buy'], 'volume': '%.8f' % item['vol'] }
      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

    return assetPairs