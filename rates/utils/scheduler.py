from background_task import background
from django.utils.timezone import now

from rates import models
from rates.utils.rates_api import RatesApi

api = RatesApi()


@background(schedule=10)
def refresh_rates():
    '''
    Background task.
    To run background tasks, run in separate terminal:

    python manage.py process_tasks

    '''
    print('Refreshing rates...')
    rates = models.Rate.objects.all()
    for rate in rates:
        price = api.get_ticker_pair_rate(rate.base, rate.target)
        if isinstance(price, float):
            rate.price = price
            rate.refreshed = now()
            rate.save()
