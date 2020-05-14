# Generated by Django 3.0.4 on 2020-05-14 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('index_page', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('technology', models.CharField(max_length=30)),
                ('image', models.CharField(max_length=1000)),
                ('github', models.CharField(max_length=100)),
                ('name_for_portfolios', models.CharField(default='Portfolio', max_length=100)),
                ('user_portfolio', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='index_page.Portfolios')),
            ],
        ),
    ]
