from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from rates import models
from rates.utils.forms import AddRateForm
from rates.utils.rates_api import RatesApi

from rates.utils.scheduler import refresh_rates

refresh_rates(repeat=10)


class RateView(TemplateView):
    def get(self, request, *args, **kwargs):
        user = request.user
        account = models.Account.objects.get(username=user.username)
        rates = account.saved_rates.all()

        # TODO: add serializer for this:
        rates = [{
            'base': r.base,
            'target': r.target,
            'price': '{:.2f}'.format(r.price)
        } for r in rates]

        return render(request, 'index.html', {
            'form': AddRateForm,
            'rates_list': rates,
            'user': account
        })

    def post(self, request):
        user = request.user
        account = models.Account.objects.get(username=user.username)

        data = request.POST
        base = data.get('base')
        target = data.get('target')
        if (base and target) and (base != target):
            api = RatesApi()
            price = api.get_ticker_pair_rate(base=base, target=target)
            if isinstance(price, float):
                rate, _created = models.Rate.objects.get_or_create(base=base.upper(),
                                                                   target=target.upper(),
                                                                   defaults={'price': price})
                account.saved_rates.add(rate)
                account.save()
        return HttpResponseRedirect(reverse('index'))


class Natalya(TemplateView):
    pass
