#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# bts_tools - Tools to easily manage the bitshares client
# Copyright (c) 2014 Nicolas Wack <wackou@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from . import core
from collections import deque
import threading
import requests
import logging

log = logging.getLogger(__name__)

feeds = {}
nfeed_checked = 0
cfg = None
history_len = None
price_history = None


def load_feeds():
    global cfg, history_len, price_history
    cfg = core.config['monitoring']['feeds']
    history_len = int(cfg['median_time_span'] / cfg['check_time_interval'])
    price_history = {cur: deque(maxlen=history_len) for cur in {'USD', 'BTC', 'CNY', 'GOLD', 'EUR'}}


def get_from_yahoo(asset_list, base):
    asset_list = [asset.upper() for asset in asset_list]
    base = base.upper()
    query_string = ','.join('%s%s=X' % (asset, base) for asset in asset_list)
    r = requests.get('http://download.finance.yahoo.com/d/quotes.csv',
                     timeout=60,
                     params={'s': query_string, 'f': 'l1', 'e': 'csv'})

    asset_prices = map(float, r.text.split())
    return dict(zip(asset_list, asset_prices))


def get_from_bter(cur, base):
    log.debug('Getting from bter: %s %s' % (cur, base))
    r = requests.get('http://data.bter.com/api/1/ticker/%s_%s' % (cur.lower(), base.lower()),
                     timeout=60).json()
    price = float(r['last']) or ((float(r['sell']) + float(r['buy'])) / 2)
    volume = float(r['vol_%s' % cur.lower()])
    return price, volume


def get_from_btc38(cur, base):
    log.debug('Getting from btc38: %s %s' % (cur, base))
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    r = requests.get('http://api.btc38.com/v1/ticker.php',
                     timeout=60,
                     params={'c': cur.lower(), 'mk_type': base.lower()},
                     headers=headers).json()
    price = float(r['ticker']['last']) # TODO: (bid + ask) / 2 ?
    volume = float(r['ticker']['last']) * float(r['ticker']['vol'])
    return price, volume


def weighted_mean(l):
    """return the weighted mean of a list of [(value, weight)]"""
    return sum(v[0]*v[1] for v in l) / sum(v[1] for v in l)


def adjust(v, r):
    return v[0]*r, v[1]*r


def get_feed_prices():
    # first get rate conversion between USD/CNY from yahoo and CNY/BTC from
    # bter and btc38 (use CNY and not USD as the market is bigger)
    yahoo_prices = get_from_yahoo(['CNY', 'XAU', 'EUR'], 'USD')
    cny_usd = yahoo_prices['CNY']
    gld_usd = yahoo_prices['XAU']

    btc_cny = weighted_mean([get_from_btc38('BTC', 'CNY'),
                             get_from_bter('BTC', 'CNY')])
    cny_btc = 1 / btc_cny

    # then get the weighted price in btc for the most important markets
    btc_price = weighted_mean([get_from_btc38('BTSX', 'BTC'),
                               get_from_bter('BTS', 'BTC'),
                               adjust(get_from_btc38('BTSX', 'CNY'), cny_btc),
                               adjust(get_from_bter('BTS', 'CNY'), cny_btc)])

    cny_price = btc_price * btc_cny
    usd_price = cny_price * cny_usd
    gld_price = usd_price / gld_usd
    eur_price = usd_price / yahoo_prices['EUR']

    feeds['USD'] = usd_price
    feeds['BTC'] = btc_price
    feeds['CNY'] = cny_price
    feeds['GOLD'] = gld_price
    feeds['EUR'] = eur_price

    for cur, price in feeds.items():
        price_history[cur].append(price)


def median(cur):
    return sorted(price_history[cur])[len(price_history[cur])//2]


def check_feeds(nodes):
    # TODO: update according to: https://bitsharestalk.org/index.php?topic=9348.0;all
    global nfeed_checked
    feed_period = int(cfg['publish_time_interval'] / cfg['check_time_interval'])

    try:
        get_feed_prices()
        nfeed_checked += 1

        log.debug('Got feeds: %f USD, %g BTC, %f CNY, %g GOLD, %f EUR  [%d/%d]' %
                  (feeds['USD'], feeds['BTC'], feeds['CNY'], feeds['GOLD'], feeds['EUR'],
                   nfeed_checked, feed_period))


        for node in nodes:
            # if an exception occurs during publishing feeds for a delegate (eg: standby delegate),
            # then we should still go on for the other nodes (and not let exceptions propagate)
            try:
                # only publish feeds if we're running a delegate node
                # we also require rpc_host == 'localhost', we don't want to publish on remote
                # nodes (while checking on them, for instance)
                # TODO: do we really want to ignore rpc_host != 'localhost', or should we just do what is asked?
                if node.type == 'delegate' and node.rpc_host == 'localhost' and 'feeds' in node.monitoring:
                    if nfeed_checked % feed_period == 0:
                        # publish median value of the price, not latest one
                        usd, btc, cny, gld, eur = median('USD'), median('BTC'), median('CNY'), median('GOLD'), median('EUR')
                        log.info('Node %s publishing feeds: %f USD, %g BTC, %f CNY, %g GOLD, %f EUR' % (node.name, usd, btc, cny, gld, eur))
                        node.wallet_publish_feeds(node.name, [['USD', usd], ['BTC', btc], ['CNY', cny], ['GOLD', gld], ['EUR', eur]])
            except Exception as e:
                log.exception(e)

    except Exception as e:
        log.exception(e)

    threading.Timer(cfg['check_time_interval'], check_feeds, args=(nodes,)).start()
