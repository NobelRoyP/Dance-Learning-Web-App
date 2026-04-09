from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('danceapp', '0016_costumebooking_quantity.py'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='phone',
            field=models.models.CharField(),
        ),
    ]
