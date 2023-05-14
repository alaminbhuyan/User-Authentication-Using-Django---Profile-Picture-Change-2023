from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.shortcuts import HttpResponseRedirect, redirect, render

from .models import UserRegistration


# Create your views here.
def home(request):
    return render(request, 'index.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            present_address = request.POST.get('address')
            parmanent_address = request.POST.get('address2')
            city = request.POST.get('city')
            
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already taken')
                print("Invalid credentials")
                return redirect('signuppage')
            
            if password != password2:
                messages.info(request, 'Passwords do not match')

            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
                model_user = UserRegistration(user=user, present_address=present_address, parmanent_address=parmanent_address, city=city)
                user.save()
                model_user.save()
                messages.success(request, "User Created Successfully")
                print("user created")
                return redirect('loginpage')
            
        return render(request, 'signup.html')
    
    else:
        return redirect('profilepage')


def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
                username = request.POST.get('username')
                password = request.POST.get('password')
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    auth.login(request, user)
                    return redirect('homepage')
                else:
                    messages.info(request, 'Invalid credentials')
                    print("Invalid credentials")
                    return redirect('loginpage')
                
        return render(request=request, template_name="login.html")
    else:
        return redirect('homepage')


def logout(request):
    auth.logout(request)
    return redirect('loginpage')

def profile(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)

        my_obj = UserRegistration.objects.get(user_id=request.user.id)

        context = {'user_id':request.user.id, 'username': user.username, 'email': user.email, 
                'first_name': user.first_name, 'last_name': user.last_name, 'present_address':my_obj.present_address,
                    'parmanent_address': my_obj.parmanent_address, 'city':my_obj.city}

        return render(request, 'profile.html', context= context)
    else:
        return redirect('loginpage')


def editprofile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            email = request.POST.get('email')
            # password = request.POST.get('password')
            # password2 = request.POST.get('password2')
            present_address = request.POST.get('address')
            parmanent_address = request.POST.get('address2')
            city = request.POST.get('city')
            

            user = User.objects.get(id=request.user.id)
            my_obj = UserRegistration.objects.get(user_id=request.user.id)
            
            user.username = username
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            # user.password = password
            my_obj.user = user
            my_obj.present_address = present_address
            my_obj.parmanent_address = parmanent_address
            my_obj.city = city
            user.save()
            my_obj.save()

            print("Update successfully")
            messages.success(request, "Profile Updated Successfully")
            return redirect(to="profilepage")
        
        else:
            user = User.objects.get(id=request.user.id)
            my_obj = UserRegistration.objects.get(user_id=request.user.id)

            context = {'user_id':request.user.id,'username': user.username, 'email': user.email,
               'first_name': user.first_name, 'last_name': user.last_name, 'present_address':my_obj.present_address,
                 'parmanent_address': my_obj.parmanent_address, 'city':my_obj.city}

        return render(request, 'editprofile.html' , context=context)
    else:
        return redirect('loginpage')

def profile_img_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and len(request.FILES) != 0:
            user_profile_img_obj = UserRegistration.objects.get(user_id=request.user.id)
            
            # 'profile_img' come from profile template
            user_profile_img_obj.user_profile_image = request.FILES['profile_image']
            
            user_profile_img_obj.save()
            
            messages.success(request=request, message="Profile Updated successfully!!")
            
            return redirect(to="profilepage")
        else:
            # redirect take the name part of urls.py file
            return redirect("editprofilepage")
        
        # return render(request, 'profile_img_change.html')
    else:
        return redirect('loginpage')
