# -*- coding: utf-8 -*-
# Copyright 2012-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""This module runs a series of tests on whether Lino issues the correct SQL requests.

You can run only these tests by issuing::

  python manage.py test lino_welfare.tests.test_sql

"Regardless of the value of the DEBUG setting in your configuration
file, all Django tests run with DEBUG=False. This is to ensure that
the observed output of your code matches what will be seen in a
production setting."
(https://docs.djangoproject.com/en/dev/topics/testing)

Fortunately Django gives a possibility to override this:
`Overriding settings <https://docs.djangoproject.com/en/dev/topics/testing/#overriding-settings>`_ 

[Note1] 
Because we are applying Django's `override_settings` decorator *to the whole class*, 
we need to also set :attr:`djangosite.utils.djangotest.TestCase.defining_module`.

[Note2]
class decorators don't work with older Python versions, so we remov

"""
import logging
logger = logging.getLogger(__name__)

import datetime
from unittest import skip

NOW = datetime.datetime.now()

from django.conf import settings
from django.test.utils import override_settings

from lino.utils import i2d
from lino.core.dbutils import resolve_model

from lino.utils.instantiator import Instantiator
from lino.modlib.users.mixins import UserProfiles


#~ def create_user(*args):
    #~ user = Instantiator('users.User',
      #~ 'username email first_name last_name is_staff is_superuser',
      #~ is_active=True,last_login=NOW,date_joined=NOW).build
    #~ return user(*args)


from lino.utils.djangotest import TestCase, reset_queries

#~ @override_settings(DEBUG=True)
#~ class SqlTest(TestCase):
    # ~ defining_module = __name__  # [Note1]


class SqlTest(TestCase):

    @skip("Currently not maintained")
    @override_settings(DEBUG=True)
    def test01(self):
        """
        Test the number of SQL queries for certain requests.
        """

        """
        The first web request will trigger Lino site startup.
        During site startup Lino does some database requests.
        When running this test together with other tests, 
        the startup probably has been done already and won't execute 
        another time.
        To make sure that these db lookups don't interfere here, we 
        now call `settings.SITE.setup()` followed by `reset_queries()`.
        
        """
        settings.SITE.startup()
        reset_queries()

        #~ 'SELECT "lino_helptext"."id", [...] FROM "lino_helptext" WHERE "lino_helptext"."help_text" IS NOT NULL',
        #~ 'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
        #~ 'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
        #~ 'SELECT "lino_siteconfig"."id", [...] WHERE "lino_siteconfig"."id" = 1',
        #~ 'SELECT "pcsw_persongroup"."id", [...] WHERE "pcsw_persongroup"."ref_name" IS NOT NULL ORDER BY "pcsw_persongroup"."ref_name" ASC',

        from lino.modlib.users.models import User

        #~ user = create_user('user','user@example.com','John','Jones',False,False)
        #~ user.save()
        #~ root = create_user('root','root@example.com','Dick','Dickens',True,True)
        user = Instantiator(settings.SITE.user_model,
                            'username email first_name last_name profile').build
        root = user('root', 'root@example.com', 'Dick', 'Dickens', '900')

        root.save()

        self.check_sql_queries(
            'INSERT INTO "users_user" [...]'
            #~ 'SELECT "users_user"."id", [...] FROM "users_user" WHERE "users_user"."profile" = 900'
        )
        #~ self.check_sql_queries(
          #~ 'SELECT (1) AS "a" FROM "lino_siteconfig" [...]',
          #~ 'INSERT INTO "lino_siteconfig" [...]',
          #~ 'SELECT (1) AS "a" [...] WHERE "contacts_partner"."id" = 100  LIMIT 1',
          #~ 'INSERT INTO "contacts_partner" [...]',
          #~ 'SELECT (1) AS "a" FROM "users_user" WHERE "users_user"."partner_ptr_id" = 100  LIMIT 1',
          #~ 'INSERT INTO "users_user" [...]'
        #~ )

        url = '/api/contacts/Companies?fmt=json&limit=30&start=0'
        response = self.client.get(url, REMOTE_USER='root')

        self.check_sql_queries(
            'SELECT "users_user"."id", [...] FROM "users_user" WHERE "users_user"."username" = root',
            'SELECT "contacts_partner"."id", [...] ORDER BY "contacts_partner"."name" ASC LIMIT 30',
            'SELECT COUNT(*) FROM "contacts_company"',
        )

        url = '/api/contacts/Companies?fmt=json&limit=30&start=0'
        response = self.client.get(url, REMOTE_USER='root')

        self.check_sql_queries(
            'SELECT "users_user"."id", [...] FROM "users_user" WHERE "users_user"."username" = root',
            'SELECT "contacts_partner"."id", [...] ORDER BY "contacts_partner"."name" ASC LIMIT 30',
            'SELECT COUNT(*) FROM "contacts_company"',
        )
