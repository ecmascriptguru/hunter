from fieldsignals import pre_save_changed, post_save_changed
from django.dispatch import receiver
from .models import Target, TargetFile, TARGET_STATE, TARGET_FILE_STATE


@receiver(post_save_changed, sender=Target, fields=['state'])
def check_target_file_state(sender, instance, changed_fields, **kwargs):
    for field, (old, new) in changed_fields.items():
        if field == Target.state.field:
            print("{0} changed from {1} to {2}.".format(field.name, old, new))