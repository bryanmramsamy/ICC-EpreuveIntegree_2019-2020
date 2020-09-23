from django.conf import settings


def get_contact_mails(request):
    """Put the contact mails dict in the context processor."""

    contact_mails = settings.CONTACT_MAILS
    return {'contact_mails': contact_mails}
