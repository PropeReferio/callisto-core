# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 14:11
from __future__ import unicode_literals

from django.db import migrations

import callisto_core.wizard_builder.model_helpers


class Migration(migrations.Migration):

    dependencies = [("wizard_builder", "0042_auto_20171101_1410")]

    operations = [
        migrations.CreateModel(
            name="MultipleChoice",
            fields=[],
            options={"proxy": True, "indexes": []},
            bases=(
                callisto_core.wizard_builder.model_helpers.ProxyQuestion,
                "wizard_builder.formquestion",
            ),
        )
    ]
