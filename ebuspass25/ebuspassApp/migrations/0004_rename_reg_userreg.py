# Generated by Django 5.1.1 on 2024-11-11 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ebuspassApp', '0003_remove_instreg_usr_con_remove_studreg_inst_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Reg',
            new_name='UserReg',
        ),
    ]
