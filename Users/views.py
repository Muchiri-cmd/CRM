from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from Users.models import User
from django.core.exceptions import ObjectDoesNotExist


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        try:
            # Check if user exists
            User.objects.get(email=email)
            print("User already exists with this email")
        except ObjectDoesNotExist:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.is_employee = True
            user.save()
            return redirect("dashboard:index")
        except Exception as e:
            print(f"Something went wrong: {e}")

    return render(request, "users/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        try:
            user = User.objects.get(username=username)
            authenticated_user = authenticate(request, username=username, password=password)
            
            if authenticated_user is not None:
                # Check if the user has the correct role
                if (role == 'employee' and authenticated_user.is_employee) or \
                   (role == 'manager' and authenticated_user.is_manager):
                    login(request, authenticated_user)
                    return redirect("dashboard:index")
                else:
                    print("Role access denied")
            else:
                print("Authentication failed")

        except ObjectDoesNotExist:
            print("User not registered")
        except Exception as e:
            print(f"Something went wrong: {e}")

    return render(request, "users/login.html")

# def login_view(request):
#     #if request.user.is_authenticated:
#         #return redirect("main:index")
    
#     if request.method == "POST": 
#         username = request.POST['username']
#         password = request.POST['password']
#         role = request.POST['role']

#         try:
#             user = User.objects.get(username=username)

#             authenticated_user=authenticate(request,username=username,password=password)
#             if authenticated_user is not None:
#                 # Check if the user has the correct role
#                 if (role == 'employee' and authenticated_user.is_employee) or \
#                 (role == 'manager' and authenticated_user.is_manager):
#                     login(request, authenticated_user)
#                     return redirect("dashboard:index")
#                 else:
#                     print("Role access denied")
#             else:
#                 print("Authentication failed")

#         except User.DoesNotExist:
#             print("User not registered")
#         except Exception as e:
#             print(f"Something went wrong: {e}")
           

#     return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("Users:login")
