from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, ProfessionalRegistrationForm, UserUpdateForm, ProfileUserUpdateForm, \
    ProfileWorkerUpdateForm
from atYourService.models import Client, Worker
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import *
from django.contrib.auth.decorators import login_required


# Create your views here.
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('Username')
                password = form.cleaned_data.get('Password')
                validate_password(password)
                name = form.cleaned_data.get('Name')
                phoneNumber = form.cleaned_data.get('PhoneNumber')

                try:
                    if Client.objects.get(PhoneNumber=phoneNumber):
                        messages.warning(request, "Phone number already exist!")
                        return render(request, 'users/user_register.html', {'form': form, 'title': "Join"})
                except:
                    pass

                newUser = User.objects.create_user(username=username, password=password)
                newClient = Client.objects.create(Username=newUser, Name=name, PhoneNumber=phoneNumber)

                messages.success(request, f"Your account has been created!")

                return redirect('login')

            except Exception as e:
                messages.warning(request, e)
    else:
        form = UserRegisterForm()
    return render(request, 'users/user_register.html', {'form': form, 'title': "Join"})


def worker_register(request):
    if request.method == 'POST':
        form = ProfessionalRegistrationForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data.get('Username')
                password = form.cleaned_data.get('Password')
                validate_password(password)
                name = form.cleaned_data.get('Name')
                profession = form.cleaned_data.get('profession')
                yearsOfExperience = form.cleaned_data.get('yearsOfExperience')
                phoneNumber = form.cleaned_data.get('PhoneNumber')
                whatsappNumber = form.cleaned_data.get('whatsappNumber')
                location = form.cleaned_data.get('Location')

                try:
                    if Worker.objects.get(PhoneNumber=phoneNumber):
                        messages.warning(request, "Phone number already exist!")
                        return render(request, 'users/user_register.html', {'form': form, 'title': "Join"})
                except:
                    pass

                newUser = User.objects.create_user(username=username, password=password)
                newWorker = Worker.objects.create(Username=newUser, Name=name, profession=profession,
                                                  PhoneNumber=phoneNumber, whatsappNumber=whatsappNumber,
                                                  yearsOfExperience=yearsOfExperience, Location=location)

                messages.success(request, f"Your account has been created!")
                return redirect('login')

            except Exception as e:
                messages.warning(request, e)

    else:
        form = ProfessionalRegistrationForm()
    return render(request, 'users/professional_register.html', {'form': form, 'title': "Join"})


@login_required()
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        try:
            pu_form = ProfileUserUpdateForm(request.POST, instance=request.user.client)  # user profile

            if user_form.is_valid() and pu_form.is_valid():
                user_form.save()
                pu_form.save()
                messages.success(request, f"Your account has been update!")
                return redirect('profile')

            context = {
                'u_form': user_form,
                'pu_form': pu_form,
            }

        except:
            pw_form = ProfileWorkerUpdateForm(request.POST, instance=request.user.worker)  # worker profile
            if user_form.is_valid() and pw_form.is_valid():
                user_form.save()
                pw_form.save()
                messages.success(request, f"Your account has been update!")
                return redirect('profile')

            context = {
                'u_form': user_form,
                'pw_form': pw_form,
            }
    else:
        user_form = UserUpdateForm(instance=request.user)
        try:
            pu_form = ProfileUserUpdateForm(instance=request.user.client)  # user profile
            context = {
                'u_form': user_form,
                'pu_form': pu_form,
            }
        except:
            pw_form = ProfileWorkerUpdateForm(instance=request.user.worker)  # worker profile
            context = {
                'u_form': user_form,
                'pw_form': pw_form,
            }

    return render(request, 'users/profile.html', context)
