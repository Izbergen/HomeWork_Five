# Generated by Django 5.1.6 on 2025-03-13 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_comment_author_item_author_alter_comment_item_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='items/'),
        ),
    ]
