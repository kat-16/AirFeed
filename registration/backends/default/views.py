from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.http import HttpResponseRedirect
from ... import signals
from ...models import RegistrationProfile
from ...users import UserModel
from ...views import ActivationView as BaseActivationView
from ...views import RegistrationView as BaseRegistrationView
from ...views import ResendActivationView as BaseResendActivationView
import uuid
from ...models import send_email

class RegistrationView(BaseRegistrationView):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    When subclassing this view, you can set the ``SEND_ACTIVATION_EMAIL``
    class variable to False to skip sending the new user a confirmation
    email or set ``SEND_ACTIVATION_EMAIL`` to ``False``. Doing so implies
    that you will have to activate the user manually from the admin site or
    send an activation by some other method. For example, by listening for
    the ``user_registered`` signal.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.

    """
    SEND_ACTIVATION_EMAIL = getattr(settings, 'SEND_ACTIVATION_EMAIL', True)
    success_url = '/'
    registration_profile = RegistrationProfile

    def form_invalid(self, form):
        return self.register(form)

    def register(self, form):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        site = get_current_site(self.request)
        idf = form.cleaned_data['password1']
        added_by = UserModel().objects.get(idf = idf)
        form.cleaned_data['username'] = form.cleaned_data['email']
        # print(UserModel().objects.filter(username = form.cleaned_data['username']))
        user_exists = len(UserModel().objects.filter(username = form.cleaned_data['username'])) > 0
        # print(user_exists)

        # Cleaning up form
        form.cleaned_data.pop('password1')
        form.cleaned_data.pop('password2')

        if not user_exists:
            # Generating temp password
            passwd = str(uuid.uuid4())[:8]
            form.cleaned_data['password'] = passwd
            # Temporarily using passowrd as identificaiton to send password in mail.
            form.cleaned_data['idf'] = passwd
            if added_by.is_superuser:
                form.cleaned_data['is_ecoord'] = True
            if added_by.is_ecoord:
                form.cleaned_data['is_presenter'] = True

            new_user_instance = (UserModel().objects
                                .create_user(**form.cleaned_data))

            new_user = self.registration_profile.objects.create_inactive_user(
                new_user=new_user_instance,
                site=site,
                send_email=self.SEND_ACTIVATION_EMAIL,
                request=self.request,
                )
            signals.user_registered.send(sender=self.__class__,
                                    user=new_user,
                                    request=self.request)
        else:
            existing_user = UserModel().objects.filter(username = form.cleaned_data['username'])[0]
            ctx_dict = {"user": existing_user, "site": site}
            if added_by.is_superuser:
                send_email((form.cleaned_data['email'],), ctx_dict, 'registration/new_coord_added_subject.txt', 'registration/new_coord_added_email.txt',
                            'registration/new_coord_added_email.html')
            if added_by.is_ecoord:
                send_email((form.cleaned_data['email'],), ctx_dict, 'registration/new_presenter_added_subject.txt', 'registration/new_presenter_added_email.txt',
                            'registration/new_presenter_added_email.html')
        return HttpResponseRedirect("/")

        # Generating temp password
        passwd = str(uuid.uuid4())[:8]
        form.cleaned_data['password'] = passwd
        form.cleaned_data['temp'] = passwd

        new_user_instance = (UserModel().objects
                            .create_user(**form.cleaned_data))

        new_user = self.registration_profile.objects.create_inactive_user(
            new_user=new_user_instance,
            site=site,
            send_email=self.SEND_ACTIVATION_EMAIL,
            request=self.request,
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

        if not user_exists:
            # Generating temp password
            passwd = str(uuid.uuid4())[:8]
            form.cleaned_data['password'] = passwd
            # Temporarily using passowrd as identificaiton to send password in mail.
            form.cleaned_data['idf'] = passwd
            if added_by.is_superuser:
                form.cleaned_data['is_ecoord'] = True
            if added_by.is_ecoord:
                form.cleaned_data['is_presenter'] = True

            new_user_instance = (UserModel().objects
                                .create_user(**form.cleaned_data))

            new_user = self.registration_profile.objects.create_inactive_user(
                new_user=new_user_instance,
                site=site,
                send_email=self.SEND_ACTIVATION_EMAIL,
                request=self.request,
                )
            signals.user_registered.send(sender=self.__class__,
                                    user=new_user,
                                    request=self.request)
        else:
            new_user = UserModel().objects.get(username = form.cleaned_data['username'])
            ctx_dict = {user: new_user, site: site}
            if added_by.is_superuser:
                send_email(form.cleaned_data['email'], ctx_dict, 'registration/new_coord_added_subject.txt', 'registration/new_coord_added_email.txt',
                            'registration/new_coord_added_email.html')
            if added_by.is_ecoord:
                send_email(form.cleaned_data['email'], ctx_dict, 'registration/new_presenter_added_subject.txt', 'registration/new_presenter_added_email.txt',
                            'registration/new_presenter_added_email.html')

        return new_user


    def registration_allowed(self):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)


class ActivationView(BaseActivationView):

    registration_profile = RegistrationProfile

    def activate(self, *args, **kwargs):
        """
        Given an an activation key, look up and activate the user
        account corresponding to that key (if possible).

        After successful activation, the signal
        ``registration.signals.user_activated`` will be sent, with the
        newly activated ``User`` as the keyword argument ``user`` and
        the class of this backend as the sender.

        """
        activation_key = kwargs.get('activation_key', '')
        site = get_current_site(self.request)
        user, activated = self.registration_profile.objects.activate_user(
            activation_key, site)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                                        user=user,
                                        request=self.request)
        return user

    def get_success_url(self, user):
        return ('registration_activation_complete', (), {})


class ResendActivationView(BaseResendActivationView):

    registration_profile = RegistrationProfile

    def resend_activation(self, form):
        """
        Given an email, look up user by email and resend activation key
        if user is not already activated or previous activation key has
        not expired. Note that if multiple users exist with the given
        email, no emails will be sent.

        Returns True if activation key was successfully sent, False otherwise.

        """
        site = get_current_site(self.request)
        email = form.cleaned_data['email']
        return self.registration_profile.objects.resend_activation_mail(
            email, site, self.request)

    def render_form_submitted_template(self, form):
        """
        Renders resend activation complete template with the submitted email.

        """
        email = form.cleaned_data['email']
        context = {'email': email}
        return render(self.request,
                      'registration/resend_activation_complete.html',
                      context)
