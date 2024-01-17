from django.db import models
from phone_field import PhoneField
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver


# model for Personal Contacts of User
class Contact(models.Model):
    # name of the contact
    name = models.CharField(max_length=100, blank=True, default="")
    # number, unique is not set to True because different users might save the same unregistered number using different names
    number = PhoneField()
    # email, optional
    email = models.EmailField(blank=True, null=True)
    # number of spam reports for the contact
    spam_reports = models.IntegerField(default=0)
    # whether the contact is a spam number or not, spam_reports > 10 means spammer
    is_spam = models.BooleanField(default=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # if a contact is already registered, then use the name and email provided during registration
        user = RegisteredUser.objects.filter(number=self.number).first()
        if user:
            self.name = user.name
            user.email = user.email

        super().save(force_insert, force_update, using, update_fields)


# class for Registered User
class RegisteredUser(models.Model):
    # name
    name = models.CharField(max_length=100)
    # number, this time unique is set to True as 2 users can't register with the same number
    number = PhoneField(unique=True)
    # email, optional
    email = models.EmailField(blank=True, null=True)
    # hashed password for user
    hashed_password = models.CharField(max_length=255)
    # personal contacts list, may be registered or unregistered on SafeCaller
    personal_contacts = models.ManyToManyField(Contact, blank=True)
    # logged in or logged out status
    is_logged_in = models.BooleanField(default=False)


@receiver(post_save, sender=RegisteredUser)
def create_or_update_contact(sender, instance, created, **kwargs):
    contact, contact_created = Contact.objects.get_or_create(
        number=instance.number,
        defaults={'name': instance.name, 'email': instance.email}
    )

    # If the contact already exists, update its values
    if not contact_created:
        contact.name = instance.name
        contact.email = instance.email

    contact.save()


# class for Reports
class SpamReport(models.Model):
    # number being reported
    reported_number = PhoneField()
    # user reporting the number
    reporter = models.ForeignKey(RegisteredUser, on_delete=models.CASCADE)
    # time of report
    reported_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=SpamReport)
def update_spam_status(sender, instance, created, **kwargs):
    if created:
        contact, _ = Contact.objects.get_or_create(
            number=instance.reported_number)

        # retrieve the corresponding RegisteredUser
        user = RegisteredUser.objects.filter(number=contact.number).first()

        # update contact fields using the registered user's information if it exists
        if user:
            print("User found")
            contact.name = user.name
            contact.email = user.email
        print("User Not found")
        # update spam-related fields
        contact.spam_reports += 1
        if contact.spam_reports > 10:
            contact.is_spam = True

        contact.save()
