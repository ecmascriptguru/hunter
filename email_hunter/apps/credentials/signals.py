from fieldsignals import pre_save_changed, post_save_changed
from django.dispatch import receiver
from .models import Credential, CREDENTIAL_STATE
from .tasks import send_mail_to_admins


@receiver(post_save_changed, sender=Credential, fields=['state'])
def credential_state_signal(sender, instance, changed_fields, **kwargs):
    for field, (old, new) in changed_fields.items():
        if field == Credential.state.field and new == CREDENTIAL_STATE.hold:
            # Should send notification
            send_mail_to_admins.delay("Credential Hold Notification",
                instance.block_notification_email_plain_text_template_name,
                context={'credential': instance.to_json(True)},
                html_template=instance.block_notification_email_html_template_name)