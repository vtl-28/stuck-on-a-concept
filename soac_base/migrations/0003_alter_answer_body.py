# Generated by Django 4.2.13 on 2024-06-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soac_base', '0002_answer_delete_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='body',
            field=models.TextField(default='Write your comment here'),
            preserve_default=False,
        ),
    ]
