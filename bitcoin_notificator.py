#!/usr/bin/python


#licenced under the
#GNU General Public License v3.0


#Billy Basdras billbasdras@yahoo.gr , https://github.com/biltAtous/  
#20.09.2018


# THE PURPOSE # You set a bitcoin price and you receive an email from yourself to another address of yours


# THE STEPS 1. you pull current bitcoin price 2. you pull FOREX foreign exchange values 3. you send email iff the limit condition is satisfied

# Additional Info # You need to set an email to send the information (might need to tweak settings, for gmail https://myaccount.google.com/lesssecureapps) 

                  # You might need to go to spam to the receiving address and move the email to inbox just for the first time

                  # You might need to consider your own currencies since the variable here is in USD

	          # You might want to include the script in startup applications

		  # It runs indefinitely, every 900sec (15min)



#LIBRARIES IMPORTATION

import requests
from forex_python.converter import CurrencyRates
import smtplib
import time



#  FUNCTION TO SEND MAIL, USED IN LAST PART




# this functions was found at https://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email  # I did not write it myself

** I am not famous for my organization and clean code, if you have visual or actual improvements to propose, you are more than welcome.**
def sendemail(from_addr, to_addr_list,# cc_addr_list,
 subject, message, login, password, smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s'% from_addr
    header += 'To: %s'% ','.join(to_addr_list)
  #  header += 'Cc: %s'% ','.join(cc_addr_list)
    header += 'Subject: %s'% subject                                                        
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()



while True:                      #MAKES THE SCRIPT RUN FOREVER



#PULL BITCOIN PRICE                                            1st PART

    bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
    response = requests.get(bitcoin_api_url)
    response_json = response.json()
    type(response_json) # The API returns a list




 # Bitcoin data is the first element of the list
    response_json[0]

#list_example 
#{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC', 'rank': '1', 
# 'price_usd': '10226.7', 'price_btc': '1.0', '24h_volume_usd': '7585280000.0',
# 'market_cap_usd': '172661078165', 'available_supply': '16883362.0', 
# 'total_supply': '16883362.0', 'max_supply': '21000000.0', 
# 'percent_change_1h': '0.67', 'percent_change_24h': '0.78', 
# 'percent_change_7d': '-4.79', 'last_updated': '1519465767'}


#print (response_json[0]['price_usd'])

    bitcoin_usd=response_json[0]['price_usd']  #SAVE BITCOIN PRICE IN VAR (USD)



#print bitcoin_usd



#FOREX forex.py                                                                                    2nd PART
#PULL CURRENCY VALUES



    c = CurrencyRates()
    usd=c.get_rates('USD')   # you can directly call get_rates('USD')
    chf=c.get_rates('CHF')
    eur=c.get_rates('EUR')
#example of dictionary
#{u'IDR': 13625.0, u'BGN': 1.7433, u'ILS': 3.8794, u'GBP': 0.68641, u'DKK': 6.6289, u'CAD': 1.3106, u'JPY': 110.36, u'HUF': 282.36, u'RON': 4.0162, u'MYR': 4.081, u'SEK': 8.3419, u'SGD': 1.3815, u'HKD': 7.7673, u'AUD': 1.3833, u'CHF': 0.99144, u'KRW': 1187.3, u'CNY': 6.5475, u'TRY': 2.9839, u'HRK': 6.6731, u'NZD': 1.4777, u'THB': 35.73, u'EUR': 0.89135, u'NOK': 8.3212, u'RUB': 66.774, u'INR': 67.473, u'MXN': 18.41, u'CZK': 24.089, u'BRL': 3.5473, u'PLN': 3.94, u'PHP': 46.775, u'ZAR': 15.747}




#print "usd['CHF']:", usd['CHF']

#print "chf['EUR']: ", chf['EUR']

#print "eur['CHF']:", eur['CHF']



#print "1 EUR =", eur['CHF'],"CHF and ","1 EUR =", eur['USD'],"USD"
#print "1 CHF =", usd['CHF'],"USD"
#print "1 USD =", chf['USD'],"CHF"

    bitcoin_chf=float(bitcoin_usd)*float(usd['CHF'])    #SAVE PRICE OF BITCOIN IN CHF IN VAR #    CHOOSE THE CURRENCY OF YOUR PREFERENCE

#print bitcoin_chf

    price_usd=str(usd['CHF'])
    price_eur=str(eur['CHF'])

#Last process SEND MAIL NOTIFICATION                                                              3rd PART




#           SET UPPER or LOWER LIMIT in CHF
    limit=8000                                                            # IMPORTANT #  SET YOUR LIMIT (IT DOESNT MATTER UPPER OR LOWER) # ACTUALLY TO SET BOTH LIMITS SHOULD NOT BE A HUSTLE


    if bitcoin_chf>limit:
        sendemail(from_addr    = 'SENDER_EMAIL_HERE@gmail.com', 
            to_addr_list = ['RECIPIENT_HERE@whatever.com \n'],
  #  cc_addr_list = [''], 
            subject      = 'BITCOIN NOTIFICATION\n', 
            message      = 'Hello,\n the current Bitcoin Price is: '+str(bitcoin_chf)+' in CHF.\n'+'Also some currency information: 1CHF='+str(price_usd)+'USD'+' and 1EUR='+str(price_eur)+'CHF'+'\n\nKind Regards\n Your BITCOIN Notificator',
            login        = 'LOGIN', 
            password     = 'PASS')
    else:
 
        print "condition not satisfied Limit less than ",limit




    time.sleep(900)   #waits a quarter of an hour











