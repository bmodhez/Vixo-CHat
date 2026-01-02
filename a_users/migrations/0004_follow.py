from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a_users', '0003_fcmtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_rel', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers_rel', to=settings.AUTH_USER_MODEL)),
            ],
            options={},
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('follower', 'following'), name='unique_follow'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['following', '-created'], name='follow_following_idx'),
        ),
        migrations.AddIndex(
            model_name='follow',
            index=models.Index(fields=['follower', '-created'], name='follow_follower_idx'),
        ),
    ]
