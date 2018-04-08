# Generated by Django 2.0.3 on 2018-04-02 08:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20180402_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletMsgSequence',
            fields=[
                ('public_key', models.CharField(max_length=200, primary_key=True, serialize=False, verbose_name='PublicKey')),
                ('seq', models.IntegerField(default=0, verbose_name='seq')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='wallet_msg_sequence', to='api.WalletUser', verbose_name='WalletUser')),
            ],
            options={
                'verbose_name': 'WalletUserSequence',
                'verbose_name_plural': 'WalletUserSequences',
            },
        ),
        migrations.RemoveField(
            model_name='product',
            name='expired_date',
        ),
        migrations.AddField(
            model_name='product',
            name='end_date',
            field=models.DateTimeField(null=True, verbose_name='End time'),
        ),
        migrations.AddField(
            model_name='product',
            name='msg_hash',
            field=models.CharField(max_length=256, null=True, verbose_name='Msg hash(owner_address,title,description,price,created,expired)'),
        ),
        migrations.AddField(
            model_name='product',
            name='seq',
            field=models.IntegerField(default=0, verbose_name='Sequence increase'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Start time'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='signature',
            field=models.CharField(max_length=200, null=True, verbose_name='Signature created by client'),
        ),
    ]
