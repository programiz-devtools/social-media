# Generated by Django 5.0.6 on 2024-06-17 12:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socual_management', '0002_remove_user_username_user_user_type_alter_user_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='socual_management.user')),
                ('liked_by', models.ManyToManyField(blank=True, related_name='liked_posts', to='socual_management.user')),
            ],
        ),
    ]
