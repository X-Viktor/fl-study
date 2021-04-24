from orders.forms import ResponseForm
from orders.models import Response


def response_check(user, order):
    if order.stage == 1:
        if user == order.customer:
            responses = order.responses.all().select_related('responding')
            if responses:
                context = {
                    'responses': responses
                }
            else:
                context = {
                    'response_message': 'Откликов нет'
                }
        elif Response.objects.filter(order=order, responding=user).exists():
            context = {
                'response_message': 'Вы уже откликнулись на этот заказ'
            }
        else:
            context = {
                'response_form': ResponseForm()
            }
    else:
        context = {
            'response_message': f'Заказ выполняет <span class="text-orange">{order.performer}</span>'
        }
    return context
