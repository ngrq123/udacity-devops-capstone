from flask import Flask, request, jsonify, render_template
from flask.logging import create_logger
import requests
import logging


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

def getRate(targetCurrency, fromCurrency):
    if targetCurrency == fromCurrency:
        return 1

    url = 'https://api.exchangeratesapi.io/latest?base=' + fromCurrency + '&symbols=' + targetCurrency
    
    tries = 3
    while tries > 0:
        result = requests.get(url)
        if result.status_code == 200:
            return result.json()['rates'][targetCurrency]
        tries -= 1
    return 1 # Arbitrary exchange rate, returns only if the API is down

def getBalances(transaction_requests):
    # Write your code here
    balances = dict()
    currencies = ['USD', 'EUR', 'GBP']
    
    for r in transaction_requests:
        prev_balances = dict()
        for k, v in balances.items():
            prev_balances[k] = v
        parts = r.split(',')
        action = parts[0]
        targetAmount = float(parts[1])
        targetCurrency = parts[2]
        if targetCurrency not in balances:
            balances[targetCurrency] = 0
        if action == 'DEPOSIT':
            balances[targetCurrency] += targetAmount
        elif action == 'WITHDRAW':
            # Assume withdraw USD
            currTargetBalance = balances[targetCurrency]
            if targetAmount <= currTargetBalance:
                # USD is enough
                balances[targetCurrency] -= targetAmount
            else:
                # USD is not enough, minus all USD balance
                currTargetBalance = targetAmount - balances[targetCurrency]
                balances[targetCurrency] = 0
                for fromCurrency in currencies:
                    LOG.info(str(balances))
                    LOG.info(fromCurrency)
                    if fromCurrency in balances:
                        # Assume currency is EUR, get USD-EUR rate
                        rate = getRate(targetCurrency, fromCurrency)
                        LOG.info('Rate: 1' + fromCurrency + ' = ' + str(rate) + targetCurrency)
                        # Get EUR needed
                        fromAmount = currTargetBalance * rate
                        if fromAmount <= balances[fromCurrency]:
                            # From EUR currency balance is enough, deduct EUR and break loop
                            balances[fromCurrency] -= fromAmount
                            currTargetBalance = 0
                            break
                        else:
                            # Deduct to EUR currency equivalent from target USD currency
                            currTargetBalance -= balances[fromCurrency] / rate
                            # Deduct all from USD currency balance
                            balances[fromCurrency] = 0
                if currTargetBalance > 0:
                    balances = prev_balances
        
    # result = list()
    # for curr, value in balances.items():
    #     if value > 0:
    #         result.append('{:.2f}'.format(value) + ' ' + curr)
    
    # return ', '.join(result)
    
    for curr, value in balances.items():
        balances[curr] = '{:.2f}'.format(value)

    return balances

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    form_dict = request.form
    # Build transaction
    transaction_requests = [
        ','.join(['DEPOSIT', form_dict['usd-amt'], 'USD']),
        ','.join(['DEPOSIT', form_dict['eur-amt'], 'EUR']),
        ','.join(['DEPOSIT', form_dict['gbp-amt'], 'GBP']),
        ','.join(['WITHDRAW', form_dict['withdrawal-amt'], form_dict['withdrawal-currency']])
    ]
    LOG.info('Transaction requests: ' + str(transaction_requests))
    # Attempt withdrawal
    balances = getBalances(transaction_requests)
    LOG.info('Balances after withdrawal: ' + str(balances))
    # Check if withdrawal is successful
    success = float(form_dict['usd-amt']) != float(balances['USD']) or \
                float(form_dict['eur-amt']) != float(balances['EUR']) or \
                float(form_dict['gbp-amt']) != float(balances['GBP'])
    return render_template('results.html', 
                            balances=balances, 
                            withdrawal_currency=form_dict['withdrawal-currency'],
                            withdrawal_amount='{:.2f}'.format(float(form_dict['withdrawal-amt'])),
                            success=success
                            )

@app.route('/test')
def test_page():
    return render_template('test.html')

if __name__=="__main__":
    app.run()