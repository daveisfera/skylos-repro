"""Django migration module — loaded by filename, not imported."""

from django.db import migrations, models


def forwards(apps, schema_editor):
    # RunPython calls this with (apps, schema_editor). Neither is required
    # for a no-op data migration, but Django still passes both.
    pass


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Item",
            fields=[
                ("id", models.AutoField(primary_key=True)),
            ],
        ),
        migrations.RunPython(forwards, migrations.RunPython.noop),
    ]
