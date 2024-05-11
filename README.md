## Binance Extraction Tool

> [!NOTE]
> Work in progress, originally was uses as a service of a product which didn't make it to market. Needs some minior adjustments to get it ready.

This tool goes through your normal spot history in the range which we are able to retrieve the data via the api, until it reached the possible end and provides you all trades to the conditions they were fullfiled on the binance platform. Which can then be used to to you taxes or keep in mind to which price you purchased your coins.

### Disclamer

This tool is not related to the binance in anyway it is a third party tool provided by a financial interessed software engineer from germany, who wants to track his invenstments in his own way and dosent want to be limited by the capabilitys of the binance platform.

> [!NOTE]
> We do not collect any inforamtion about the usage as well as no api key data, it will simply run on your device.

### How to run

First you need to set some values in your enviroments, that would be 'public'(key) and 'private'(key) which can be done by:

```bash
export public=your_key_here
export private=your_key_2_here
```

Then simply run the fast-api app and ping the right endpoint.
