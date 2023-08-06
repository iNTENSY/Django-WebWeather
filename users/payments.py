import uuid

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views import generic
from yookassa import Payment
from .models import PaymentModel
from users.tasks import check_payments


class PaymentView(LoginRequiredMixin, generic.RedirectView):
    def get(self, *args, **kwargs):
        payment = self.get_payment_object()
        self.create_payment_model(payment['id'])
        self.payment_handler(payment['id'])
        return HttpResponseRedirect(payment['confirmation']['confirmation_url'])

    def get_payment_object(self) -> dict:
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
        }, str(uuid.uuid4())))
        return payment

    def create_payment_model(self, uid) -> None:
        """
        Данный класс создает объект PaymentModel в базе данных.
        :param uid: Уникальный идентификатор для объекта.
        """
        record = PaymentModel(
            user=self.request.user,
            uuid=uid
        )
        record.save()
        print(f'Создан объект с uuid: {record.uuid}')

    @staticmethod
    def payment_handler(payment_id):
        check_payments.delay(payment_id)
