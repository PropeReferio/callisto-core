# Generated by Django 2.0.4 on 2018-04-11 21:12
from hashlib import sha256
import logging

import bcrypt
from django.db import migrations, models
from callisto_core.accounts.auth import index

logger = logging.getLogger(__name__)


def encrypt_user_data(apps, schema_editor):
    Account = apps.get_model("accounts.Account")
    for account in Account.objects.all():
        username = account.user.username

        # sha256 + bcrypt matches our current state of the art in other
        # platforms.
        userhash = sha256(username.encode('utf-8')).hexdigest()
        usercrypt = bcrypt.hashpw(userhash.encode('utf-8'), bcrypt.gensalt())
        userindex = index(userhash)

        account.encrypted_username = usercrypt.decode()
        account.username_index = userindex

        email = account.user.email
        if email:
            # sha256 + bcrypt matches our current state of the art in other
            # platforms.
            emailhash = sha256(email.encode('utf-8')).hexdigest()
            emailcrypt = bcrypt.hashpw(emailhash.encode('utf-8'), bcrypt.gensalt())
            emailindex = index(emailhash)

            account.encrypted_email = emailcrypt.decode()
            account.email_index = emailindex

        account.save()


class Migration(migrations.Migration):

    dependencies = [("accounts", "0003_auto_20190607_1540")]

    operations = [
        migrations.RunPython(
            encrypt_user_data, reverse_code=migrations.RunPython.noop
        )
    ]
