# Generated by Django 3.2.3 on 2022-05-20 02:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0006_post_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='General', max_length=100)),
                ('description', models.CharField(default='', max_length=300)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='categories', to='post.post')),
            ],
        ),
    ]
