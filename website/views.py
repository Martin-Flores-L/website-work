from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record

# Create your views here.

def home(request):
    # Get all the records
    records = Record.objects.all()

    if request.method == "POST":
        # Check if user is logging in
        if request.POST.get('Login'):
            # Get the username and password
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # If user is valid, log them in
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully logged in!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('home')

        # Check if user is logging out
        elif request.POST.get('Logout'):
            logout(request)
            messages.success(request, "Successfully logged out!")
            return redirect('home')
    else:

        return render(request, 'home.html', {'records': records})


def register_user(request):
    # Check to see if registering
    if request.method == "POST":
        # Get the form data
        form = SignUpForm(request.POST)

        # Check if form is valid
        if form.is_valid():
            # Save the user
            form.save()

            # Get the username and password
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            # Log the user in
            login(request, user)

            # Send a success message
            messages.success(request, "Successfully registered!")
            return redirect('home')
        
        else:
            # Send an error message
            messages.error(request, "Unsuccessful registration. Invalid information.")
            # return redirect('register')
    else:
        # Create a blank form
        form = SignUpForm()

        # Send the form to the template
        return render(request, 'register.html', {'form': form})
    
    #Using this, it keeps the username and the email in the form after the user submits the form with invalid information
    return render(request, 'register.html', {'form': form})     
    

def customer_record(request, pk):

    if request.user.is_authenticated:
        # Get the record
        customer_record = Record.objects.get(id=pk)

        # Send the record to the template
        return render( request, 'record.html', {'customer_record': customer_record} )
    
    else:
        messages.error(request, "Please login to view this record.")
        return redirect('home')