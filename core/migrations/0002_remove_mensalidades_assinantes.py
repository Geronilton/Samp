# Generated by Django 5.1.4 on 2025-05-15 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mensalidades',
            name='assinantes',
        ),
    ]
