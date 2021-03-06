# Generated by Django 2.1.2 on 2019-01-04 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20190104_0710'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentLeadStatus',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'AgentLeadStatus',
            },
        ),
        migrations.CreateModel(
            name='AssignedAgentLead',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('leadid', models.IntegerField()),
                ('agentid', models.CharField(max_length=100)),
                ('AgentLeadStatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.AgentLeadStatus')),
            ],
            options={
                'verbose_name_plural': 'AssignedAgentLead',
            },
        ),
    ]
