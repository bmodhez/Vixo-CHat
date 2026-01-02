from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0013_seed_default_groupchats'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='groupmessage',
            index=models.Index(fields=['group', '-created'], name='gm_group_created_idx'),
        ),
        migrations.AddIndex(
            model_name='groupmessage',
            index=models.Index(fields=['author', '-created'], name='gm_author_created_idx'),
        ),
    ]
