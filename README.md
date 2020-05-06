# Currency Converter

A Python flask app that calculates whether withdrawing an amount in a target currency is possible with a balances in a multi-currency wallet, purely based on current exchange rates (i.e. no charges of any form).

Currently, it supports 3 currencies: USD, EUR and GBP. The order of withdrawal begins with the withdrawal (target) currency, followed by USD, EUR, then GBP.

This application utilises [Exchange Rates API](https://exchangeratesapi.io) to retrieve live exchange rates.

## Example Usage
Suppose you have 100 USD, 70 EUR and 50 GBP, and would like to withdraw 150 GBP from your wallet. 

Assuming the exchange rates (retrieved from the API) are:
* 1 GBP = 1.2454628992 USD
* 1 GBP = 1.1486331266 EUR


It will be possible to withdraw all 50 GBP from your wallet, convert 80.29 GBP from 100 USD, and convert 19.71 GBP from 22.64 EUR. This leaves 47.36 EUR in your wallet.