# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# This file is part of the Lino-Welfare project.
# Lino-Welfare is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# Lino-Welfare is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with Lino-Welfare; if not, see <http://www.gnu.org/licenses/>.

"""
The demo fixture for :mod:`welfare.aids`.
"""

import datetime

from django.utils.translation import ugettext_lazy as _
from lino.dd import resolve_model
from lino.utils import Cycler, ONE_DAY
from lino.utils import mti
from lino import dd, rt


def objects():
    Granting = rt.modules.aids.Granting
    AidType = rt.modules.aids.AidType
    Person = rt.modules.contacts.Person
    Client = rt.modules.pcsw.Client
    ClientStates = rt.modules.pcsw.ClientStates
    ClientContactType = rt.modules.pcsw.ClientContactType
    Board = rt.modules.boards.Board
    ExcerptType = rt.modules.excerpts.ExcerptType

    Project = resolve_model('pcsw.Client')
    qs = Project.objects.filter(client_state=ClientStates.coached)
    # if qs.count() > 10:
    #     qs = qs[:10]
    PROJECTS = Cycler(qs)

    l = []
    qs = ClientContactType.objects.filter(can_refund=True)
    for cct in qs:
        qs2 = Person.objects.filter(client_contact_type=cct)
        if qs2.count():
            i = (cct, Cycler(qs2))
            l.append(i)
    PARTNERS = Cycler(l)

    BOARDS = Cycler(Board.objects.all())

    DURATIONS = Cycler(None, 1, 1, 30, 0, None, 365)

    fkw = dd.str2kw('name', _("Pharmacy"))  # Apotheke
    pharmacy_type = rt.modules.pcsw.ClientContactType.objects.get(**fkw)
    PHARMACIES = Cycler(rt.modules.contacts.Company.objects.filter(
        client_contact_type=pharmacy_type))

    for i, at in enumerate(AidType.objects.all()):
        for j in range(2):
            sd = dd.demo_date(days=i)
            kw = dict(start_date=sd,
                      board=BOARDS.pop(),
                      decision_date=dd.demo_date(days=i-1),
                      aid_type=at)

            kw.update(client=PROJECTS.pop())
            duration = DURATIONS.pop()
            if duration is not None:
                kw.update(end_date=sd+datetime.timedelta(days=duration))
            g = Granting(**kw)
            g.after_ui_create(None)
            yield g

    # ConfirmationTypes = rt.modules.aids.ConfirmationTypes
    RefundConfirmation = rt.modules.aids.RefundConfirmation
    IncomeConfirmation = rt.modules.aids.IncomeConfirmation
    ClientContact = rt.modules.pcsw.ClientContact

    COACHES = Cycler(rt.modules.users.User.objects.filter(
        coaching_type__isnull=False))

    AMOUNTS = Cycler(123, 234, 345, 456, 678)
    CATEGORIES = Cycler(rt.modules.aids.Category.objects.all())

    # create 1 or 2 confirmations per granting
    urgent_aid_generated = 0
    for i, g in enumerate(Granting.objects.filter(aid_type__isnull=False)):
        ct = g.aid_type.confirmation_type
        num = i % 2 + 1
        if ct.model is RefundConfirmation:
            num = 3  # always create 3 confirmations per refund granting
        if g.aid_type.pharmacy_type == pharmacy_type:
            pharmacy = PHARMACIES.pop()
            yield ClientContact(
                type=pharmacy_type,
                company=pharmacy, client=g.client)
        for j in range(num):
            kw = dict(granting=g, client=g.client)
            kw.update(user=COACHES.pop())
            kw.update(start_date=g.start_date)
            kw.update(end_date=g.end_date)
            if ct.model is IncomeConfirmation:
                kw.update(category=CATEGORIES.pop())
                kw.update(amount=AMOUNTS.pop())
            if ct.model is RefundConfirmation:
                doctor_type, doctor_cycler = PARTNERS.pop()
                doctor = doctor_cycler.pop()
                kw.update(doctor_type=doctor_type)
                kw.update(doctor=doctor)
                yield ClientContact(
                    type=doctor_type,
                    contact_person=doctor, client=g.client)
                # only the first confirmation has a pharmacy
                if g.aid_type.pharmacy_type == pharmacy_type and j == 0:
                    kw.update(pharmacy=pharmacy)
            yield ct.model(**kw)

        # for two refund grantings, create the corresponding
        # additional granting of urgent medical help
        if ct.model is RefundConfirmation and urgent_aid_generated < 2:
            kw = dict()
            kw.update(client=g.client)
            kw.update(start_date=g.start_date)
            kw.update(end_date=g.end_date)
            kw.update(aid_type=AidType.objects.get(short_name="DMH"))
            yield Granting(**kw)
            urgent_aid_generated += 1

    ses = rt.login('theresia')

    for at in rt.modules.aids.AidType.objects.exclude(confirmation_type=''):
        M = at.confirmation_type.model
        et = ExcerptType.get_for_model(M)
        qs = M.objects.filter(granting__aid_type=at)
        for obj in qs:
            ses.selected_rows = [obj]
            yield et.get_or_create_excerpt(ses)
            
    def person2client(f, l):
        obj = Person.objects.get(first_name=f, last_name=l)
        mti.insert_child(obj, Client)

    person2client("Paul", "Frisch")
    person2client("Bruno", "Braun")

    # create a clothing_refund granting and excerpt for Paul Frisch:
    ses = rt.login("alicia")
    obj = Client.objects.get(name="Frisch Paul")
    at = AidType.objects.get(
        body_template='clothing_bank.body.html')
    g = Granting(aid_type=at, client=obj)
    g.full_clean()
    yield g
    M = at.confirmation_type.model
    conf = M(client=obj, granting=g)
    conf.full_clean()
    conf.on_create(ses)
    yield conf
    et = ExcerptType.get_for_model(M)
    ses.selected_rows = [conf]
    yield et.get_or_create_excerpt(ses)

