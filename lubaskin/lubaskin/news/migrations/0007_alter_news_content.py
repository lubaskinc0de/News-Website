# Generated by Django 4.0.2 on 2022-02-14 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0006_alter_news_category_alter_news_content_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(blank=True, verbose_name='NewsPaper-text'),
        ),
    ]
