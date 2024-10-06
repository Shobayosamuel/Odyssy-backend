import requests
from django.conf import settings
from decouple import config

class Paystack:
    PAYSTACK_SECRET_KEY = config("PAYSTACK_SECRET_KEY")
    base_url = 'https://api.paystack.co'

    def verify_payment(self, reference, *args, **kwargs):
        url = f'{self.base_url}/transaction/verify/{reference}'
        headers = {
            'Authorization': f'Bearer {self.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            return response_data['status'], response_data['data']
        return False, response.json()
