# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 16:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("delivery", "0016_report_contact_voicemail")]

    operations = [migrations.RemoveField(model_name="report", name="autosaved")]
