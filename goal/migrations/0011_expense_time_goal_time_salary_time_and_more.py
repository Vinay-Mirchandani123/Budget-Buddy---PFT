from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0010_alter_expense_start_time_alter_goal_start_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='goal',
            name='time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='salary',
            name='time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='expense',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='goal',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='start_time',
            field=models.DateField(blank=True, null=True),
        ),
    ]
