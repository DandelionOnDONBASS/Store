from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from products.models import Basket
from store.common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class MyLoginView(TitleMixin,LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


class UserRegistrationView(TitleMixin,SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name ='users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы усешно зарегистрировались!'
    title = 'Store - Регистрация'

    def form_valid(self, form):
        if User.objects.filter(email=form.cleaned_data['email']).exists():
            form.add_error('email', 'Такой email уже зарегистрирован.')
            return self.form_invalid(form)

        return super().form_valid(form)
    
    


# def register(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы усешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)



class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name= 'users/profile.html'
    title = 'Store - Профиль'
    
    def get_success_url(self):
        return reverse_lazy('users:profile',args=(self.object.id,))
    
    # def get_context_data(self, **kwargs):
    #     context = super(UserProfileView, self).get_context_data()
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)

#     context = {'title': 'Store - Профиль',
#                'form': form,
#                'baskets': Basket.objects.filter(user=request.user)}
#     return render(request, 'users/profile.html', context)





def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))



class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтерждение электронной почты'
    template_name = 'users/email_verification.html'
    
    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verifield_email = True
            user.save()
            return super(EmailVerificationView,self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))