from datetime import datetime
from functools import wraps

from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _

from account.models import BlockUser

def unblocked_user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        request = args[0]
        if not request.user.is_superuser:
            block = BlockUser.objects.filter(user=request.user).order_by('-till_date').first()
            if block:
                if block.till_date > datetime.now():
                    return HttpResponseForbidden(_("You are blocked till %s") % block.till_date)
            block_for_ever = BlockUser.objects.filter(user=request.user, unlimited=True).exists()
            if block_for_ever:
                return HttpResponseForbidden(_("You are blocked till %s") % block.till_date)


        return fn(*args, **kwargs)

    return login_required(wrapper)