from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Order
from payment.models import Payment
from payment.serializers import PaymentSerializer
from payment.paystack import Paystack
import requests


class InitiatePaymentView(APIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get("order_id")
        order = Order.objects.get(id=order_id, user=user)
        amount = int(order.total * 100)  # Convert to kobo

        # Call Paystack API to initialize the transaction
        headers = {
            "Authorization": f"Bearer {Paystack.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": user.email,
            "amount": amount,  # Paystack expects the amount in kobo (i.e., cents)
            "reference": f"order_{order.id}_{user.id}",
            "callback_url": "https://your-domain.com/payment/callback/",  # Replace with your callback URL
        }

        response = requests.post(
            f"{Paystack.base_url}/transaction/initialize", json=data, headers=headers
        )

        if response.status_code == 200:
            response_data = response.json()
            payment = Payment.objects.create(
                user=user,
                order=order,
                amount=order.total,
                reference=response_data["data"]["reference"],
                status="pending",
            )

            return Response(
                {
                    "payment_url": response_data["data"]["authorization_url"],
                    "reference": response_data["data"]["reference"],
                }
            )

        return Response(
            {"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST
        )


class VerifyPaymentView(APIView):
    def get(self, request, *args, **kwargs):
        reference = request.query_params.get("reference")
        paystack = Paystack()

        payment = Payment.objects.get(reference=reference)
        status, result = paystack.verify_payment(reference)

        if status:
            if result["status"] == "success":
                payment.status = "success"
                payment.save()

                # Update order status to 'paid'
                payment.order.status = "paid"
                payment.order.save()

                return Response(
                    {"message": "Payment successful"}, status=status.HTTP_200_OK
                )

        payment.status = "failed"
        payment.save()
        return Response(
            {"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST
        )

class PaystackWebhookView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.data
        if payload['event'] == 'charge.success':
            reference = payload['data']['reference']
            payment = Payment.objects.get(reference=reference)
            payment.status = 'success'
            payment.save()

            # Update the order as paid
            payment.order.status = 'paid'
            payment.order.save()

            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
