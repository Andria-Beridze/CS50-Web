# Generated by Django 5.0.2 on 2024-03-25 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_listing_bid_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='bid_count',
        ),
        migrations.AddField(
            model_name='comment',
            name='comment_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
