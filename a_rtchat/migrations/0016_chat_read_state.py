from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('a_rtchat', '0015_notifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatReadState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_read_message_id', models.PositiveBigIntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='read_states', to='a_rtchat.chatgroup')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_read_states', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='chatreadstate',
            constraint=models.UniqueConstraint(fields=('user', 'group'), name='unique_read_state'),
        ),
        migrations.AddIndex(
            model_name='chatreadstate',
            index=models.Index(fields=['group', 'user'], name='readstate_group_user_idx'),
        ),
    ]
