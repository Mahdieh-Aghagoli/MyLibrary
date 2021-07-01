from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import UpdateView
from rest_framework.generics import get_object_or_404
from rest_framework.reverse import reverse

from user.forms import UserRegisterForm, UserUpdateForm
from user.models import Account
from user.tokens import account_activation_token


class UserRegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect(reverse('send-email', args=(user.slug,)))
        return render(request, 'user/register.html', {'form': form})


class SendEmailVCode(View):
    def get(self, request, user_slug):
        user = get_object_or_404(Account, slug=user_slug)
        current_site = get_current_site(request)
        mail_subject = 'Activate SocialMedia account.'
        message = render_to_string('user/email_activation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).encode().decode(),
            'token': account_activation_token.make_token(user),
        })

        to_email = user.email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return render(request, 'user/email_waiting.html', {'user': user})


class EmailVerify(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse('login'))
        else:
            return HttpResponse('Activation link is invalid!')


class ProfileView(UpdateView):
    model = Account
    form_class = UserUpdateForm
    template_name = 'user/profile.html'

    def get_success_url(self):
        return reverse('profile')

    def get_object(self, **kwargs):
        return self.request.user
