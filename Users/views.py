from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User



def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Check if user exists
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = User.objects.create_user(email=email,password=password,username=username)
            user.save()
            return redirect("dashboard:index")
        except:
            print("Something went wrong. Please try again.")
           
    return render(request, "users/signup.html")

def login_view(request):
    #if request.user.is_authenticated:
        #return redirect("main:index")
    
    if request.method == "POST": 
        #email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
           
            if user is not None:
                authenticated_user=authenticate(request,username=username,password=password)
                if authenticated_user is not None:
                    login(request, user)
                    return redirect("dashboard:index")
                else:
                    print("authentication failed")
        except User.DoesNotExist:
            print("User not registered")
            
        except:
            print("Something went wrong. Please try again.")
           

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("Users:login")
