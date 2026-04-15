from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contents", "0007_alter_user_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="password",
            field=models.CharField(max_length=128),
        ),
    ]
