# Generated by Django 3.1.5 on 2021-08-24 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='distribucion_puertos_a_distrito',
            name='Distrito',
        ),
        migrations.AddField(
            model_name='hilos_alimentacion',
            name='Distrito',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion.distrito'),
        ),
        migrations.AlterField(
            model_name='distribucion_puertos_a_distrito',
            name='ID_Fibra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.hilos_alimentacion', unique=True),
        ),
    ]
