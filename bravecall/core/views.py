import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse, HttpResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
import requests

User = get_user_model()

from .tokens import account_activation_token

from core.models import Place
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def get_nearest_places(request):
    user_location_text = request.GET.get("location_text")
    severity = request.GET.get("severity")
    latitude = request.GET.get("latitude")
    longitude = request.GET.get("longitude")

    # If user doesn't enter a location, they must use GPS
    if not user_location_text and not (latitude and longitude):
        return JsonResponse({"error": "Please enter a location or enable GPS."}, status=400)

    # Geocode if location is given as text
    if user_location_text and not (latitude and longitude):
        geolocator = Nominatim(user_agent="bravecall")
        location = geolocator.geocode(user_location_text)

        if location:
            latitude, longitude = location.latitude, location.longitude
        else:
            return JsonResponse({"error": "Invalid location entered."}, status=400)

    # Convert latitude & longitude to float
    try:
        latitude, longitude = float(latitude), float(longitude)
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid coordinates."}, status=400)

    user_coords = (latitude, longitude)

    # Filter places based on severity
    if severity in ["mild", "moderate"]:
        places = Place.objects.filter(type="barangay_hall")
    elif severity == "severe":
        places = Place.objects.filter(type="police_station")
    else:
        return JsonResponse({"error": "Invalid severity. Choose mild, moderate, or severe."}, status=400)

    # Compute distances and sort by nearest
    places_data = []
    for place in places:
        place_coords = (place.latitude, place.longitude)
        distance = geodesic(user_coords, place_coords).km
        places_data.append({
            "name": place.name,
            "address": place.address,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "distance": round(distance, 2),
        })

    places_data.sort(key=lambda x: x["distance"])  # Sort by nearest

    return JsonResponse({"places": places_data[:5]}) 

def places_page(request):
    return render(request, "user/map.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.status = "active"
        user.save()

        messages.success(request, "Your account has been activated! You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link!")
        return redirect('login')

def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password != repassword:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered!")
            return redirect('signup')

        hashed_password = make_password(password)
        user = User(email=email, fname=fname, lname=lname, password=hashed_password)
        user.status = "inactive" 

        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

        try:
            subject = "Activate Your Account"
            message = render_to_string('activation_email.html', {
                'user': user,
                'activation_link': activation_link
            })
            send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
            messages.success(request, "An email has been sent to confirm your account.")
        except Exception as e:
            messages.error(request, f"Error sending email: {str(e)}")

        return redirect('login')

    return render(request, 'signup.html')


def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)

            if user.status != "active":
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = account_activation_token.make_token(user)
                activation_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))

                try:
                    subject = "Activate Your Account (Resent)"
                    message = render_to_string('activation_email.html', {
                        'user': user,
                        'activation_link': activation_link
                    })
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email], fail_silently=False)
                    messages.error(request, "Your account is not activated. A new activation email has been sent.")
                except Exception as e:
                    messages.error(request, f"Error sending activation email: {str(e)}")
                return redirect('login')

            if check_password(password, user.password):
                request.session['user_id'] = user.id
                request.session['user_fname'] = user.fname
                request.session['user_lname'] = user.lname
                request.session['user_role'] = user.role

                token, created = Token.objects.get_or_create(user=user)

                messages.success(request, "Login successful!")

                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({'message': 'Login successful!', 'token': token.key})

                if user.role == 'admin':
                    return redirect('dashboard')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid password")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, 'login.html')


@csrf_exempt
def google_auth(request):
    token = request.POST['credential'] 

    try:
        user_data = id_token.verify_oauth2_token(
        token, google_requests.Request(), os.getenv('GOOGLE_OAUTH_CLIENT_ID')
    )
    except ValueError:
        return HttpResponse(status=403)  

    try:
        user = User.objects.get(email=user_data['email'])
    except User.DoesNotExist:
        user = User(
            email=user_data['email'],
            fname=user_data['given_name'],
            lname=user_data['family_name']
        )
        user.save()

    request.session['user_id'] = user.id
    request.session['user_fname'] = user.fname
    request.session['user_lname'] = user.lname
    request.session['user_role'] = user.role

    token, created = Token.objects.get_or_create(user=user)

    messages.success(request, "Login successful with Google!")

    if user.role == 'admin':
        return redirect('dashboard')
    else:
        return redirect('home')

def logout_user(request):
    request.session.flush()
    messages.success(request, "You have been logged out!")
    return redirect('login')

def dashboard(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access the dashboard.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
        
        if user.role != 'admin':
            messages.error(request, "You do not have permission to access the dashboard.")
            return redirect('login')
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

    active_users = User.objects.filter(status="active")
    total_users = User.objects.all()

    active_percentage = (active_users.count() / total_users.count()) * 100 if total_users.count() > 0 else 0

    return render(request, 'admin/dashboard.html', {
        'active_users': active_users,
        'active_percentage': active_percentage,
        'user': user  
    })


def users(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
        
        if user.role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

    users = User.objects.all()

    if request.method == 'POST':
        if 'create' in request.POST:
            fname = request.POST.get('fname')
            lname = request.POST.get('lname')
            email = request.POST.get('email')
            password = request.POST.get('password')
            repassword = request.POST.get('repassword')
            role = request.POST.get('role')
            status = request.POST.get('status')
            
            if password != repassword:
                messages.error(request, "Passwords do not match!")
                return redirect('users')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered!")
                return redirect('users')

            hashed_password = make_password(password)

            User.objects.create(
                fname=fname, lname=lname, email=email, password=hashed_password, role=role, status=status
            )
            messages.success(request, "User created successfully!")
            return redirect('users')

        if 'update' in request.POST:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            user.role = request.POST.get('role')
            user.status = request.POST.get('status')
            user.save()

            messages.success(request, "User updated successfully!")
            return redirect('users')

        if 'delete' in request.POST:
            user_id = request.POST.get('user_id')
            user = User.objects.get(id=user_id)
            user.delete()

            messages.success(request, "User deleted successfully!")
            return redirect('users')

    return render(request, 'admin/users.html', {'users': users, 'user': user})

def reports(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
        
        if user.role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

    users = User.objects.all()


    return render(request, 'admin/reports.html', {'users': users, 'user': user})

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def faq(request):
    return render(request, 'faq.html')

def features(request):
    return render(request, 'features.html')

def index(request):
    return render(request, 'index.html')

def services(request):
    return render(request, 'services.html')

def profile(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access the this page.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
        
        if user.role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home')
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

    if request.method == 'POST':
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(profile_pic.name, profile_pic)
            user.profile_picture = os.path.join(settings.MEDIA_URL, filename)  
            user.save()
            messages.success(request, "Profile picture updated!")

        if 'password' in request.POST and request.POST['password']:
            password = request.POST['password']
            if password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user) 
                messages.success(request, "Password updated!")

        user.fname = request.POST.get('fname', user.fname)
        user.lname = request.POST.get('lname', user.lname)
        user.email = request.POST.get('email', user.email)
        user.save()

        messages.success(request, "Profile updated!")
        return redirect('profile')

    return render(request, 'admin/profile.html', {'user': user})

def userprofile(request):
    user = User.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        if 'profile_pic' in request.FILES:
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            filename = fs.save(profile_pic.name, profile_pic)
            user.profile_picture = os.path.join(settings.MEDIA_URL, filename) 
            user.save()
            messages.success(request, "Profile picture updated!")


        if 'password' in request.POST and request.POST['password']:
            password = request.POST['password']
            if password:
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  
                messages.success(request, "Password updated!")

        user.fname = request.POST.get('fname', user.fname)
        user.lname = request.POST.get('lname', user.lname)
        user.email = request.POST.get('email', user.email)
        user.save()

        messages.success(request, "Profile updated!")
        return redirect('user-profile')

    return render(request, 'user/profile.html', {'user': user})

def charts(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
        
        if user.role != 'admin':
            messages.error(request, "You do not have permission to access this page.")
            return redirect('home') 
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('login')

    return render(request, 'admin/charts.html', {'user': user})

def home(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')

    return render(request, 'user/home.html', {'user': user})

def history(request):
    if 'user_id' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    try:
        user = User.objects.get(id=request.session['user_id'])
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('login')
    return render(request, 'user/history.html', {'user': user})