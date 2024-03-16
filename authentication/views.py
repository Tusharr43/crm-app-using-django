from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail  # Add this import statement
from djangobasic import settings
from templated_email import send_templated_mail

def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        password1 = request.POST.get('pass1')
        password2 = request.POST.get('pass2')

        if not all([username, first_name, last_name, email, password1, password2]):
            messages.error(request, "Please fill in all fields.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('signup')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        # Create user
        new_user = User.objects.create_user(username=username, email=email, password=password1)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        # Send verification email
        subject = 'Authenticate your account'
        message_body = f'Hello {new_user.username}\nWelcome to the demo\This mail is regarding activation of your account\n\nTHANK YOU HAVE A WONDERFUL DAY :))'
        from_email = settings.EMAIL_HOST_USER
        to_list = [email]
        try:
            send_mail(subject, message_body, from_email, to_list)
            messages.success(request, "Account created successfully. Please check your email for verification.\n\n RELOAD THIS PAGE") 
            return redirect('home')
        except Exception as e:
            messages.error(request, f"Failed to send email: {e}")

        return redirect('home')

    return render(request, "signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')  # Assuming the username field in your form is named 'username'
        password = request.POST.get('password')

        # Authenticate using username
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return render(request,'signin.html')  # Redirect to home or any other page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('home')  # Redirect back to the home page if login fails

    return render(request, "index.html")  # Render the signin page template


def Home(request):
    return render(request, "Home.html")  

def about(request):
    return render(request, "about.html")

def signout(request):
    logout(request)
    return redirect('home')
