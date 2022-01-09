# Generated by Django 3.2.3 on 2021-06-28 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sziapp', '0003_ckmmst'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ktnmst',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('sskcd', models.CharField(db_column='SSKCD', max_length=10)),
                ('ktncd', models.CharField(db_column='KTNCD', max_length=10)),
                ('ktnname', models.CharField(db_column='KTNNAME', max_length=50)),
                ('egstrtm', models.IntegerField(db_column='EGSTRTM')),
                ('egendtm', models.IntegerField(db_column='EGENDTM')),
                ('makdt', models.DateTimeField(db_column='MAKDT')),
                ('updt', models.DateTimeField(db_column='UPDT')),
            ],
            options={
                'db_table': 'KTNMST',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Sskmst',
            fields=[
                ('id', models.IntegerField(db_column='ID', primary_key=True, serialize=False)),
                ('sskcd', models.CharField(db_column='SSKCD', max_length=10)),
                ('sskname', models.CharField(db_column='SSKNAME', max_length=50)),
                ('makdt', models.DateTimeField(db_column='MAKDT')),
                ('updt', models.DateTimeField(db_column='UPDT')),
            ],
            options={
                'db_table': 'SSKMST',
                'managed': False,
            },
        ),
    ]
