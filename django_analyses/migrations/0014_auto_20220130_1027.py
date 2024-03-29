# Generated by Django 3.2.6 on 2022-01-30 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('django_analyses', '0013_alter_analysisversion_fixed_run_method_kwargs'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputdefinition',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='inputdefinition',
            name='field_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
