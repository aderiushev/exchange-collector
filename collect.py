import requests
import click
import os, sys
from daemonize import Daemonize
import time
import logging
from time import gmtime, strftime

from exchanges.kraken import Kraken 
from exchanges.yobit import Yobit
from exchanges.livecoin import Livecoin
from exchanges.poloniex import Poloniex

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def getExchange(name):
  if name == 'kraken':
    return Kraken
  if name == 'yobit':
    return Yobit
  if name == 'livecoin':
    return Livecoin
  if name == 'poloniex':
    return Poloniex

def getFormattedTime():
  return strftime("%d.%m.%Y %H:%M:%S", gmtime())

def getAssetPairs(exchange):
  return getExchange(exchange).getAssetPairs()

def getTickers(exchange, pairs):
  return getExchange(exchange).getTickers(pairs)

def getFilename(exchange, pairs):
  return getExchange(exchange).getFilename(pairs)

@click.option('--exchange', required=True)
@click.option('--pairs', nargs=1, required=True)
@click.command(name='daemon-stop', short_help='Stops daemon')
def daemon_stop(exchange, pairs):
  name = getFilename(exchange, pairs)
  fh = logging.FileHandler('%s.log' % name, "a")
  logger.addHandler(fh)
  logger.info('INFO [%s]: Daemon stopped' % getFormattedTime())
  pid_filename = './%s.pid' % name
  try:
    with open(pid_filename, "r") as pid_file:
      pid = pid_file.read()
      os.system("kill -9 %d" % int(pid))
      os.remove(pid_filename)
      click.echo(click.style('Daemon stopped', fg='yellow'))
  except FileNotFoundError:
    click.echo(click.style('There is no such daemon started', fg='red'))

@click.option('--exchange', required=True)
@click.option('--pairs', nargs=1, required=True)
@click.option('--timeout', nargs=1, default=15)
@click.option('--shout/--no-shout', default=False)
@click.command(name='daemon-start', short_help='Starts daemon on exact exchange & pairs list (delimited by comma)')
def daemon_start(exchange, pairs, timeout, shout):
  def run_daemon():
    while True:
      try:
        tickers = getTickers(exchange, pairs)
        requests.post('http://127.0.0.1:8080/collect/ticker/%s' % exchange, json={ 'tickers': tickers })
        if shout:
          logger.info('INFO [%s]: SENT %s' % (getFormattedTime(), tickers))
      except Exception as e:
        logger.error('ERROR [%s]: %s' % (getFormattedTime(), e))

      time.sleep(timeout)

  name = getFilename(exchange, pairs)
  pid_filename='./%s.pid' % name
  fh = logging.FileHandler('%s.log' % name, "a")
  logger.addHandler(fh)
  keep_fds = [fh.stream.fileno()]
  daemon = Daemonize(app=name, pid=pid_filename, action=run_daemon, keep_fds=keep_fds)
  logger.info('INFO [%s]: Daemon started' % getFormattedTime())
  click.echo(click.style('Daemon started, you\'re good :)', fg='green'))

  daemon.start()

@click.option('--exchange', required=True)
@click.command(name='list', short_help='Lists all the possible pairs on the concrete exchange to operate with', help='You can use the pair sysname (like XETHZUSD) in the other commands')
def list(exchange):
  pairs = getAssetPairs(exchange)
  for index, (key, item) in enumerate(pairs.items()):
    print('%s. %s (%s <-> %s)' % (index + 1, key, item['from'], item['to']))

@click.option('--exchange', required=True)
@click.option('--pairs', nargs=1, required=True)
@click.command(name='ticker', short_help='Fetches the ticker by pairs list (delimited by comma)')
def ticker(exchange, pairs):
  tickers = getTickers(exchange, pairs)
  for index, (key, item) in enumerate(tickers.items()):
    print('=== %s === ' % key)
    print('ask: %s\nbid: %s\nvolume: %s' % (item['ask'], item['bid'], item['volume']))

@click.command(name='exchange-list', short_help='List of all the possible exchanges to work on')
def exchange_list():
  for index, filename in enumerate([file for file in os.listdir('./exchanges') if file.endswith('.py') and not file.startswith('__')]):
    print('%s. %s' % (index + 1, filename.split('.')[0]))

@click.group()
def cli():
  pass
cli.add_command(list)
cli.add_command(ticker)
cli.add_command(daemon_start)
cli.add_command(daemon_stop)
cli.add_command(exchange_list)

if __name__ == '__main__':
  cli()