# Generated by Django 5.0.2 on 2024-03-25 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_bid_listing_comment_listing_alter_bid_bid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='bid_count',
            field=models.IntegerField(default=0),
        ),
    ]
