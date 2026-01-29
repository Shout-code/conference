from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ("attendees", "0002_attendeechange"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendeechange",
            name="changed_fields",
            field=models.JSONField(null=True, blank=True, help_text="List of changed fields for edit actions."),
        ),
    ]
