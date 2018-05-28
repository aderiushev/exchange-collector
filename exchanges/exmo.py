import requests

class Exmo:
  def getAssetPairs(self):
    try:
      response = requests.get('https://api.exmo.com/v1/ticker').json()
      result = {}

      for index, (key, item) in enumerate(response.items()):
        fromTo = key.split('_')
        result[key] = { 'from': fromTo[0].upper(), 'to': fromTo[1].upper() }

      return result

    except requests.exceptions.HTTPError as e:
      # TODO: process error
      pass

  def getFilename(self, pairs):
    if pairs:
      return 'exmo-%s' % pairs.lower().replace('/', '-')
    else:
      return 'exmo-all'

  def getTickers(self, pairs, mode):
    try:
      result = {}

      if mode == 'ticker':
        response = requests.get('https://api.exmo.com/v1/ticker').json()

        for index, (key, item) in enumerate(response.items()): 
          if key in pairs:
            result[key] = {
              'ask': {
                'value': '%.8f' % float(item['buy_price']),
                'volume': None
              },
              'bid': {
                'value': '%.8f' % float(item['sell_price']),
                'volume': None
              }
            }
      else:
        response = requests.get('https://api.exmo.com/v1/order_book', params={ 'pair': ','.join(pairs), }, verify=False).json()

        for index, (key, item) in enumerate(response.items()):
          if key in pairs:
            result[key] = {
              'ask':
                {
                  'value': '%.8f' % float(item['ask'][0][0]) if len(item['ask']) > 0 else None,
                  'volume': '%.8f' % float(item['ask'][0][1]) if len(item['ask']) > 0 else None
                },
              'bid':
                {
                  'value': '%.8f' % float(item['bid'][0][0]) if len(item['bid']) > 0 else None,
                  'volume': '%.8f' % float(item['bid'][0][1]) if len(item['bid']) > 0 else None
                }
            }

      return result

    except requests.exceptions.HTTPError as e:
      raise