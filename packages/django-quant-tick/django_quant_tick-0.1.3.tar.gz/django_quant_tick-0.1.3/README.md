# What?

Django Quant Tick downloads and aggregate candlesticks from tick data.

<img src="https://raw.githubusercontent.com/globophobe/django-quant-tick/main/docs/assets/volume-candles.png" />

# Why?

Candlesticks aggregated by `django-quant-tick` are informationally dense. Such data can be useful for analyzing financial markets. As an example, refer to ["Low-Frequency Traders in a High-Frequency World: A Survival Guide"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2150876) and ["The Volume Clock: Insights into the High Frequency Paradigm"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2034858). Lopez de Prado recommends volume bars, however they are are computationally expensive to generate.

By aggregating and filtering raw ticks, they can be computed faster, with little loss in precision.

This optional aggregation is by equal symbol, timestamp, nanoseconds and tick rule. As described in the accompanying project [cryptofeed-werks](https://github.com/globophobe/cryptofeed-werks), aggregating trades in this way can increase information, as they are either orders of size or stop loss cascades.

As well, the number of rows can be reduced by 30-50%

By filtering aggregated rows, for example only writing a row when an aggregated trade is greater than `significant_trade_filter >= 1000`, the number of rows can be reduced more.

# How?

Whenever possible, data is downloaded from the exchange's AWS S3 repositories. Otherwise, it is downloaded using their REST APIs. 

A database, preferably PostgreSQL, is required. Data is saved to the database after aggregation and filtering. 

Candles are aggregated at 1 minute intervals, and validated with the exchange's historical candle API.

[Notes](https://github.com/globophobe/django-quant-tick/blob/main/NOTES.md).

Supported exchanges
-------------------

:white_medium_square: Binance REST API (requires API key, which requires KYC)
* <em style="font-size: 0.9em">Other exchanges validate trade data downloaded from exchanges using candle data provided by exchanges. However, I did not complete KYC, and as a resident of Japan am not currently able to do so. Support is incomplete. Pull requests are welcome.</em>

:white_check_mark: Bitfinex REST API

:white_check_mark: BitMEX REST API, and [S3](https://public.bitmex.com/) repository

:white_check_mark: Bybit [S3](https://public.bybit.com/) repository. 
* <em style="font-size: 0.9em">The REST API is no longer paginated, so data may be delayed 24 hours or more.</em>

:white_check_mark: Coinbase Pro REST API

Note: Exchanges without paginated REST APIs or an S3 repository, will never be supported.

Installation
------------

For convenience, `django-quant-tick` can be installed from PyPI:

```
pip install django-quant-tick
```

Deployment
----------

For deployment, there are Dockerfiles. As well, there are invoke tasks for deployment to Google Cloud Run. Just as easily, the demo could be deployed to a VPS or AWS.

If using GCP, it is recommended to use the Cloud SQL Auth proxy, and run the management commands to collect data from your local machine. Django Quant Tick will upload the trade data to the cloud.

```
cd demo
invoke start-proxy
python proxy.py trades
```

Then, configure a Cloud Workflow to collect data in the cloud. There is an example workflow in the [invoke tasks](https://github.com/globophobe/django-quant-tick/blob/main/demo/tasks.py).

Environment
-----------

To use the scripts or deploy to GCP, rename `.env.sample` to `.env`, and add the required settings.
