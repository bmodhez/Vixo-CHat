from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0014_groupmessage_indexes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('mention', 'Mention'), ('reply', 'Reply'), ('ping', 'Ping'), ('follow', 'Follow')], max_length=16)),
                ('chatroom_name', models.CharField(blank=True, default='', max_length=128)),
                ('message_id', models.PositiveBigIntegerField(blank=True, null=True)),
                ('preview', models.CharField(blank=True, default='', max_length=180)),
                ('url', models.CharField(blank=True, default='', max_length=255)),
                ('is_read', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('from_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='notifications_sent', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-created']},
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', 'is_read', '-created'], name='notif_user_read_idx'),
        ),
        migrations.AddIndex(
            model_name='notification',
            index=models.Index(fields=['user', '-created'], name='notif_user_created_idx'),
        ),
    ]
