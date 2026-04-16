from django.shortcuts import render, redirect
from .forms import UserSignupForm, UserLoginForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from email.mime.image import MIMEImage
import os
from .models import User

def userSignupView(request):
    if request.method == "POST":
        form = UserSignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            role  = form.cleaned_data['role']

            #Send welcome email 
            html_content = render_to_string('core/welcome_email.html', {
                'email': email,
                'role':  role,
            })

            msg = EmailMultiAlternatives(
                subject    = 'Welcome to Bug Tracking System',
                body       = f'Welcome {email}! Your account has been created.',
                from_email = settings.EMAIL_HOST_USER,
                to         = [email],
            )
            msg.attach_alternative(html_content, "text/html")
            

            # attach inline image
            image_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
            with open(image_path, 'rb') as img:
                mime_image = MIMEImage(img.read(),'png')
                mime_image.add_header('Content-ID', '<logo_image>')
                mime_image.add_header('Content-Disposition', 'inline', filename='logo.png')
                msg.attach(mime_image)

            msg.send()
            #end email

            return redirect('login')
        else:
            return render(request, 'core/signup.html', {'form': form})
    else:
        form = UserSignupForm()
        return render(request, 'core/signup.html', {'form': form})



def userLoginView(request):
    if request.method == "POST":
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            print(form.cleaned_data)
            email    = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user     = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                if user.role == "admin":
                    return redirect("adminDashboard")
                elif user.role == "manager":
                    return redirect("managerDashboard")
                elif user.role == "developer":
                    return redirect("developerDashboard")
                elif user.role == "tester":
                    return redirect("testerDashboard")
            else:
                return render(request, 'core/login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = UserLoginForm()
        return render(request, 'core/login.html', {'form': form})


def userLogoutView(request):
    logout(request)
    return redirect('login')

def homeView(request):
    return render(request, 'core/home.html')

def forgotPasswordView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request,'core/forgot_password.html',{'error': 'Passwords do not match!'})

        try:
            user = User.objects.get(email=email)
            user.set_password(password1)
            user.save()
            return redirect('login')
        except User.DoesNotExist:
            return render(request,'core/forgot_password.html',{'error': 'No account found with this email!'})
    
    return render(request,'core/forgot_password.html')