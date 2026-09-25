from django.db import migrations


def add_whatsapp_social_link(apps, schema_editor):
    SocialLink = apps.get_model("core", "SocialLink")
    SocialLink.objects.update_or_create(
        platform="whatsapp",
        defaults={
            "label": "WhatsApp",
            "url": "https://wa.me/254792389675",
            "icon_class": "bi-whatsapp",
            "is_active": True,
            "order": 5,
        },
    )


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_sociallink_platform"),
    ]

    operations = [
        migrations.RunPython(add_whatsapp_social_link, migrations.RunPython.noop),
    ]
