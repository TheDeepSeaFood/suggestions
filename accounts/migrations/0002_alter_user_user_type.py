# Generated by Django 5.1.3 on 2025-01-31 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('DSF', 'Deep Seafood'), ('ROF', 'Royal Future'), ('QAR', 'Qatar'), ('AIN', 'Al-Ain'), ('ABD', 'Abu Dhabi')], max_length=10),
        ),
    ]
