import datetime as dt

from yookassa import Payment

from djangoWeather.celery import app
from users.models import PaymentModel, Subscription


@app.task(bind=True)
def check_payments(self, payment_uuid: str):
    payment = PaymentModel.objects.select_related('user').get(uuid=payment_uuid)

    try:
        answer = Payment.find_one(payment_id=payment_uuid)
        if answer.status != 'succeeded':
            raise Exception('Повтор проверки статуса платежа!')
        else:
            payment.is_accepted = True
            payment.user.user_status = 'Premium'
            payment.user.save()
            payment.save()

            Subscription.objects.create(
                client=payment.user,
                order=payment,
                start_date=dt.date.today(),
                end_date=dt.date.today() + dt.timedelta(days=30)
            )
    except Exception as ex:
        print(ex)
        raise self.retry(countdown=20, max_retries=3)
