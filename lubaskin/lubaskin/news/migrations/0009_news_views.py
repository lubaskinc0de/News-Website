# Generated by Django 4.0.2 on 2022-02-15 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0008_alter_news_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='views',
            field=models.IntegerField(default=0),
        ),
    ]
