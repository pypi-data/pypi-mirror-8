# -*- coding: UTF-8 -*-
# Copyright 2012-2013 Luc Saffre
# License: BSD (see file COPYING for details)

import decimal
from dateutil.relativedelta import relativedelta
ONE_DAY = relativedelta(days=1)

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext as _


from lino.utils import i2d
from lino.utils.instantiator import Instantiator
from lino.core.dbutils import resolve_model
from lino.utils import Cycler

from lino.modlib.accounts.utils import AccountTypes


def n2dec(v):
    return decimal.Decimal("%.2d" % v)


def objects():

    User = resolve_model('users.User')
    kerstin = User(username="kerstin",
                   first_name="Kerstin", last_name=u"Kerres",
                   profile='300')
        #~ level=UserLevel.user,
        #~ debts_level=UserLevel.user)
    yield kerstin

    Household = resolve_model('households.Household')
    Budget = resolve_model('debts.Budget')
    Actor = resolve_model('debts.Actor')
    for hh in Household.objects.all():
        b = Budget(partner_id=hh.id, user=kerstin)
        b.fill_defaults(None)
        yield b

    Budget = resolve_model('debts.Budget')
    Entry = resolve_model('debts.Entry')
    Account = resolve_model('accounts.Account')
    Company = resolve_model('contacts.Company')
    INCOME_AMOUNTS = Cycler([i * 200 for i in range(8)])
    EXPENSE_AMOUNTS = Cycler([i * 5.24 for i in range(10)])
    DEBT_AMOUNTS = Cycler([(i + 1) * 300 for i in range(5)])
    PARTNERS = Cycler(Company.objects.all())
    LIABILITIES = Cycler(Account.objects.filter(type=AccountTypes.liabilities))
    EXPENSE_REMARKS = Cycler(_("Shopping"), _("Cinema"), _("Seminar"))

    for b in Budget.objects.all():
        #~ n = min(3,b.actor_set.count())
        for e in b.entry_set.all():
            #~ for i in range(n):
            if e.account.type == AccountTypes.incomes:
                amount = INCOME_AMOUNTS.pop()
            elif e.account.type == AccountTypes.expenses:
                amount = EXPENSE_AMOUNTS.pop()
                if e.account.ref in ('3030', '3071'):
                    e.remark = EXPENSE_REMARKS.pop()
            if e.account.required_for_household:
                e.amount = n2dec(amount)
            if e.account.required_for_person:
                for a in b.actor_set.all():
                    e.amount = n2dec(amount)
                    e.actor = a
            # ~ e.account_changed(None) # set description
            e.save()
        ACTORS = Cycler(None, *[a for a in b.actor_set.all()])
        for i in range(4):
            amount = int(DEBT_AMOUNTS.pop())
            kw = dict(budget=b,
                      account=LIABILITIES.pop(),
                      partner=PARTNERS.pop(),
                      amount=amount,
                      actor=ACTORS.pop())
            if amount > 600:
                kw.update(distribute=True)
            else:
                kw.update(monthly_rate=n2dec(amount / 20))
            e = Entry(**kw)
            e.account_changed(None)  # set description
            yield e

    ses = settings.SITE.login("kerstin")
    for e in Entry.objects.filter(account__ref='3030'):
        new = e.duplicate.run_from_code(ses)
        new.remark = EXPENSE_REMARKS.pop()
        yield new

    settings.SITE.site_config.master_budget = Budget.objects.get(id=1)
    yield settings.SITE.site_config
