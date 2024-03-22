

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goal', '0009_alter_salary_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='start_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goal',
            name='start_time',

            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='salary',
            name='start_time',

            field=models.IntegerField(),
        ),
    ]
