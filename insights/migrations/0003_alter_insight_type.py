# Generated by Django 5.1.3 on 2025-01-31 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insights', '0002_branch_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insight',
            name='type',
            field=models.CharField(choices=[('DSF', 'Deep Seafood'), ('ROF', 'Royal Future'), ('QAR', 'Qatar'), ('AIN', 'Al-Ain'), ('ABD', 'Abu Dhabi')], default='DSF', max_length=255),
        ),
    ]
