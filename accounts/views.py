from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group
from .forms import CustomerCreationForm, StaffCreationForm
from .models import CustomUser
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse


class CustomerSignUpView(CreateView):
    form_class = CustomerCreationForm
    template_name = 'registration/customer_signup.html'

    def post(self, request, *args, **kwargs):
        form = CustomerCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = CustomUser.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form' : form })

class StaffSignUpView(CreateView):
    form_class = StaffCreationForm
    template_name = 'registration/staff_signup.html'

    def post(self, request, *args, **kwargs):
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = CustomUser.objects.get(username=username)
            customer_group = form.cleaned_data.get('group')
            customer_group.user_set.add(signup_user)
            return redirect('login')
        else:
            return render(request, self.template_name, {'form' : form })

class UserUpdateView(UpdateView):
    model = CustomUser
    template_name = 'edit_profile.html'
    fields = ['username', 'age', 'email', 'mobile']
    success_url = reverse_lazy('cinema:all_products')
    
    def get_object(self, queryset=None):
        # Get the current user's profile
        return self.request.user
    
    def form_valid(self, form):
        # Set the user of the profile to the current user
        form.instance.user = self.request.user
        return super().form_valid(form)


def staff_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == '91759876':
            return redirect('create_admin')
    return render(request, 'registration/staff_password.html')