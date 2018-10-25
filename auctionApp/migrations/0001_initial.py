# Generated by Django 2.1.2 on 2018-10-25 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seller_id', models.IntegerField()),
                ('seller_name', models.CharField(max_length=20)),
                ('seller_email', models.EmailField(max_length=254)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('starting_price', models.FloatField()),
                ('current_price', models.FloatField()),
                ('current_winner_id', models.IntegerField(blank=True, null=True)),
                ('current_winner_name', models.CharField(default='No bids yet.', max_length=20)),
                ('time_posted', models.DateTimeField()),
                ('time_closing', models.DateTimeField()),
                ('hash_id', models.CharField(max_length=256)),
                ('active', models.BooleanField(default=True)),
                ('banned', models.BooleanField(default=False)),
                ('resolved', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('price', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('auction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctionApp.Auction')),
            ],
        ),
        migrations.CreateModel(
            name='ExchangeRate',
            fields=[
                ('code', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('rate', models.FloatField()),
                ('last_updated', models.TimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSettings',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('currency', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
    ]
