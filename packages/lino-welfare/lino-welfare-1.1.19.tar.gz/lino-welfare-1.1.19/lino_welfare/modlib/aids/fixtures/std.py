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

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from lino.dd import babel_values
from lino.utils.instantiator import Instantiator
from lino import dd, rt


def objects():

    IncomeConfirmation = rt.modules.aids.IncomeConfirmation
    RefundConfirmation = rt.modules.aids.RefundConfirmation
    SimpleConfirmation = rt.modules.aids.SimpleConfirmation
    ConfirmationTypes = rt.modules.aids.ConfirmationTypes

    aidType = Instantiator(
        'aids.AidType',
        confirmation_type=ConfirmationTypes.get_for_model(
            IncomeConfirmation)).build
    kw = dd.babelkw(
        'name',
        de="Eingliederungseinkommen",
        en="Eingliederungseinkommen",
        fr="Revenu d'intégration")
    kw.update(short_name="EiEi")
    kw.update(is_integ_duty=True)
    kw.update(body_template='integ_income.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Ausländerbeihilfe",
        en="Ausländerbeihilfe",
        fr="Aide aux immigrants")
    kw.update(body_template='foreigner_income.body.html')
    kw.update(is_integ_duty=True)
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Feste Beihilfe",
        en="Feste Beihilfe",
        fr="Revenu fixe")
    kw.update(body_template='fixed_income.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(
            SimpleConfirmation)).build
    kw = dd.babelkw(
        'name',
        de="Erstattung",
        en="Erstattung",
        fr="Remboursement")
    kw.update(body_template='certificate.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)
    kw = dd.babelkw(
        'name',
        de="Übernahmeschein",
        en="Übernahmeschein",
        fr="Übernahmeschein")
    kw.update(body_template='certificate.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(
            RefundConfirmation)).build

    kw = dd.babelkw(
        'name',
        de="Übernahme von Arzt- und/oder Medikamentenkosten",
        en="Medical costs",
        fr="Remboursement de frais médicaux")
    kw.update(short_name="AMK")
    fkw = dd.str2kw('name', _("Pharmacy"))  # Apotheke
    cct_pharmacy = rt.modules.pcsw.ClientContactType.objects.get(**fkw)
    kw.update(pharmacy_type=cct_pharmacy)
    kw.update(body_template='medical_refund.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Dringende Medizinische Hilfe",
        nl="Dringende medische Hulp",
        en="Urgent Medical Care",
        fr="Aide Médicale Urgente")
    kw.update(short_name="DMH")
    kw.update(is_urgent=True)
    kw.update(body_template='urgent_medical_care.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    aidType = Instantiator(
        'aids.AidType', "name",
        confirmation_type=ConfirmationTypes.get_for_model(
            SimpleConfirmation)).build
    kw = dd.babelkw(
        'name',
        de="Möbellager",
        en="Furniture",
        fr="Mobilier")
    kw.update(body_template='furniture.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Heizkosten",
        en="Heating costs",
        fr="Frais de chauffage")
    kw.update(body_template='heating_refund.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    croix_rouge = rt.modules.contacts.Company(name="Belgisches Rotes Kreuz")
    yield croix_rouge

    kw = dd.babelkw(
        'name',
        de="Lebensmittelbank",
        en="Food bank",
        fr="Banque alimentaire")
    kw.update(confirmed_by_primary_coach=False)
    kw.update(company=croix_rouge)
    kw.update(body_template='food_bank.body.html')
    kw.update(dd.str2kw('excerpt_title', _("Attestation")))
    yield aidType(**kw)

    kw = dd.babelkw(
        'name',
        de="Kleiderkammer",
        en="Clothes bank",
        fr="Banque aux vêtements")
    kw.update(body_template='clothing_bank.body.html')
    kw.update(company=croix_rouge)
    kw.update(dd.str2kw('excerpt_title', _("Clothing costs transfer")))
    yield aidType(**kw)

    ## Categories

    Category = dd.resolve_model('aids.Category')
    yield Category(**babel_values(
        'name',
        en="Living together",
        de="Zusammenlebend",
        fr="Cohabitant"))
    yield Category(**babel_values(
        'name',
        en="Living alone",
        de="Alleinstehend",
        fr="Persone isolée"))
    yield Category(**babel_values(
        'name',
        en="Person with family at charge",
        de="Person mit Familienlasten",
        fr="Personne qui cohabite avec une famille à sa charge"))

    Decider = dd.resolve_model('boards.Board')
    yield Decider(**dd.str2kw(
        'name', _("Social Board (SB)")))  # "Sozialhilferat (SHR)"
    yield Decider(**dd.str2kw(
        'name', _("Social Commission (SC)")))  # Sozialhilfeausschuss (SAS)
    yield Decider(**dd.str2kw(
        'name', _("Permanent Board (PB)")))  # Ständiges Präsidium (SP)

