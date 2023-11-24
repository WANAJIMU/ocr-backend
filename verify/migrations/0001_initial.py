# Generated by Django 4.2.7 on 2023-11-24 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='uploads/')),
                ('current_occupation', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('loan_amount', models.PositiveIntegerField()),
                ('purpose', models.TextField()),
                ('date_of_application', models.DateTimeField(auto_now=True)),
                ('organization_working_under', models.CharField(max_length=200)),
            ],
        ),
    ]
