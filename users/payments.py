import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from yookassa import Payment
from .models import PaymentModel


class PaymentView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        uid, payment = self.get_payment_object()
        self.create_payment_model(uid)
        context = {
            'payment': payment
        }
        return render(self.request, 'payment/form.html', context)

    def get_payment_object(self) -> tuple:
        unique_id = uuid.uuid4()
        payment = dict(Payment.create({
            "amount": {
                "value": "1000.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": 'http://127.0.0.1:8000/user/confirmation/'
            },
            "capture": True,
            "description": f"Подписка от {self.request.user}"
        }, unique_id))
        return unique_id, payment

    def create_payment_model(self, uid) -> None:
        record = PaymentModel(
            user=self.request.user,
            uuid=uid
        )
        record.save()