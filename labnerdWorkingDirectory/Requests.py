#!/usr/bin/python3
"""Do requests in python"""

def mpesa(amount, phone):
    """ make a call to mpesa """
    import requests
    import base64
    import datetime

    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    querystring = {"grant_type" : "client_credentials"}
    payload = ""

    consumer_key = "V7Xuin4dic2mp38AjAttCRtEYQBnIqeuOdlRoDlfiwxgcqGl"
    consumer_secret = "dOG5pboLpP4IzGn1LHHKjc5oX1nfFgYYOhVbHJdq5tWulBqTboVyEM5fuq4xbCgB"
    prefix = f'{consumer_key}:{consumer_secret}'
    encoded_data = base64.b64encode(prefix.encode())
    headers = { 'Authorization' : f'Basic {encoded_data.decode()}' }
    r = requests.get(url, headers=headers)
    access_token = r.json().get('access_token')

    shortcode = "174379"
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    prepassword = f'{shortcode}{passkey}{timestamp}'.encode()
    password = base64.b64encode(prepassword).decode()
    express_header = { 'Authorization' : f'Bearer {access_token}', 'Content-Type' : 'application/json' }

    payload = {
    "BusinessShortCode": shortcode,
    "Password": password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": amount,
    "PartyA":f"254{phone}",
    "PartyB": shortcode,
    "PhoneNumber": f"254{phone}",
    "CallBackURL": "https://characterize.tech/callback",
    "AccountReference": "Labnerd Kenya",
    "TransactionDesc": "Test"
    }

    Mpesa_express_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    result = requests.post(Mpesa_express_url, headers=express_header, json=payload)
    print(result.text)
