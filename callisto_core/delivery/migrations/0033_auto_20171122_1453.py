# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 14:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("delivery", "0032_auto_20171122_1453")]

    operations = [
        migrations.DeleteModel(name="ProxySentMatchReport"),
        migrations.CreateModel(
            name="SentMatchReport",
            fields=[],
            options={"proxy": True, "indexes": []},
            bases=("delivery.newsentmatchreport",),
        ),
    ]
