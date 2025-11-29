from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Patient, Consultation, Document
from .audit import log_audit


def serialize_instance(instance):
    data = {}
    for field in instance._meta.fields:
        name = field.name
        data[name] = getattr(instance, name, None)
    return data


@receiver(pre_save, sender=Patient)
def audit_patient_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_data = serialize_instance(Patient.objects.get(pk=instance.pk))
        except Patient.DoesNotExist:
            instance._old_data = None


@receiver(post_save, sender=Patient)
def audit_patient_post_save(sender, instance, created, **kwargs):
    if created:
        log_audit("create_patient", instance.user, target=instance, new_value=serialize_instance(instance))
    else:
        old = getattr(instance, "_old_data", None)
        new = serialize_instance(instance)
        if old != new:
            log_audit("update_patient", instance.user, target=instance, old_value=old, new_value=new)


@receiver(pre_save, sender=Consultation)
def audit_consultation_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_data = serialize_instance(Consultation.objects.get(pk=instance.pk))
        except Consultation.DoesNotExist:
            instance._old_data = None


@receiver(post_save, sender=Consultation)
def audit_consultation_post_save(sender, instance, created, **kwargs):
    if created:
        log_audit("consultation_start", instance.doctor.user if instance.doctor else None, target=instance, new_value=serialize_instance(instance))
    else:
        old = getattr(instance, "_old_data", None)
        new = serialize_instance(instance)
        if old != new:
            log_audit("record_update", instance.doctor.user if instance.doctor else None, target=instance, old_value=old, new_value=new)


@receiver(pre_save, sender=Document)
def audit_document_pre_save(sender, instance, **kwargs):
    if instance.pk:
        try:
            instance._old_data = serialize_instance(Document.objects.get(pk=instance.pk))
        except Document.DoesNotExist:
            instance._old_data = None


@receiver(post_save, sender=Document)
def audit_document_post_save(sender, instance, created, **kwargs):
    if created:
        log_audit("document_update", instance.consultation.doctor.user if instance.consultation and instance.consultation.doctor else None, target=instance, new_value=serialize_instance(instance))
    else:
        old = getattr(instance, "_old_data", None)
        new = serialize_instance(instance)
        if old != new:
            log_audit("document_update", instance.consultation.doctor.user if instance.consultation and instance.consultation.doctor else None, target=instance, old_value=old, new_value=new)
