import math
from app.schema.event import  PaymentPayload
from fastapi import APIRouter
from app.core.settings import MPESA_STK_PUSH_QUERY_URL, MPESA_CALLBACK_URL, MPESA_PASSKEY, MPESA_BUSINESS_SHORTCODE, MPESA_STK_PUSH_URL, MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET, MPESA_ACCESS_TOKEN_URL
import requests
from requests.auth import  HTTPBasicAuth
import base64
import time
from datetime import datetime

router = APIRouter(
    prefix='/payments',
    tags=['payments']
)


class MpesaPaymentHandler:
    consumer_key = None
    consumer_secret = None
    access_token_url = None
    access_token = None
    access_token_expiry = None
    access_token_params = None
    headers = None
    business_shortcode = None
    stk_push_url = None
    now = None
    passkey =  None
    password = None
    timestamp = None
    callback_url = None
    stk_query_url = None

    def __init__(self):
        self.consumer_secret = MPESA_CONSUMER_SECRET
        self.consumer_key = MPESA_CONSUMER_KEY
        self.access_token_url = MPESA_ACCESS_TOKEN_URL
        self.access_token_params = {
            'grant_type': 'client_credentials'
        }
        self.now = datetime.now()
        self.passkey = MPESA_PASSKEY
        self.business_shortcode = MPESA_BUSINESS_SHORTCODE
        self.stk_push_url = MPESA_STK_PUSH_URL
        self.password = self.generate_password()
        self.callback_url = MPESA_CALLBACK_URL
        self.stk_query_url = MPESA_STK_PUSH_QUERY_URL




        try:
            self.access_token = self.get_access_token()
            if self.access_token is None:
                raise Exception('Missing access token')
            else:
                self.access_token_expiry = time.time() + 3599

        except Exception as e:
            with open('logs.txt', 'w') as f:
                f.write(f"Error obtaining access token: {str(e)}\n")


    def get_access_token(self):
       try:
           response = requests.get(self.access_token_url, auth=HTTPBasicAuth(self.consumer_key, self.consumer_secret),
                                   params=self.access_token_params)
           token = response.json()['access_token']
           self.headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
           }
           # print(f"Obtained access token: {response.json()}")
       except Exception as e:
            with open('logs.txt', 'w') as f:
                f.write(f"Error obtaining access token: {str(e)}\n")
            raise e
       return token

    def generate_password(self):
        self.timestamp = self.now.strftime('%Y%m%d%H%M%S')
        password_str = self.business_shortcode + self.passkey + self.timestamp
        password_bytes = password_str.encode('utf-8')
        return base64.b64encode(password_bytes).decode('utf-8')



    def stk_push(self, payload):
        amount = payload.amount
        phone_number = payload.phone_number
        stk_push_payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": math.ceil(amount),
            "PartyA": phone_number,
            "PartyB": self.business_shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": self.callback_url,
            "AccountReference": "Tiko",
            "TransactionDesc": "Tiko-sale"

        }

        try:
            response = requests.post(url=self.stk_push_url, json=stk_push_payload, headers=self.headers)
            return response.json()
        except Exception as e:
            with open('logs.txt', 'a') as f:
                f.write(f"Error initiating STK Push: {str(e)}\n")
            raise e


    def query_stk_push(self, checkout_request_id):
        query_payload = {
            "BusinessShortCode": self.business_shortcode,
            "Password": self.password,
            "Timestamp": self.timestamp,
            "CheckoutRequestID": checkout_request_id,
        }
        try:
            response = requests.post(url=self.stk_query_url, json=query_payload, headers=self.headers)
            print(f"The stk push  query status code {response.status_code}")
            print(f"The stk push query  response {response.json()}")
            return True
        except Exception as e:
            with open('logs.txt', 'a') as f:
                f.write(f"Error in completing stk push transaction: {str(e)}\n")
            return False

    def mpesa_callback(self):
        response = requests.get(url=self.callback_url, headers=self.headers)
        print(f'Callback response: {response}')
        call_back_response = response.json()
        if call_back_response['Body']['stkCallback']['ResultCode'] == 0:
            return True
        return False



@router.get('/mpesa-token')
async def get_mpesa_token():
    mpesa_payment = MpesaPaymentHandler()
    mpesa_payment.get_access_token()

@router.post('/test')
async def get_test(payload:PaymentPayload):
    mpesa_payment = MpesaPaymentHandler()
    response = mpesa_payment.stk_push(payload)
    print(f'Stk push response: {response}')
    if keys := response.get('ResponseCode'):
        if keys == '0':
            checkout_request_id = response['CheckoutRequestID']
            stk_push_query_response = mpesa_payment.query_stk_push(checkout_request_id)
            if stk_push_query_response:
                print("Inside the confirm payment block")
                response = mpesa_payment.mpesa_callback()
                if response:
                    return {
                        "message": "Payment completed successfully",
                        "status": "success"
                    }
                return {
                    "message": "Payment failed, please try again",
                    "status": "failed"
                }
        return {
            "message": "STK Push initiation failed",
            "status": "failed"
        }
    return {
        "message": "Invalid phone number",
        "status": "failed"
    }





