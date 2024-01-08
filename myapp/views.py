from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse,Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myapp.models import Room, Message

def index(request):
    return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username is not available')
                return redirect('register')
            else:
                user = User.objects.create_user(username = username,email=email,password=password)    
                user.save()
                messages.info(request,'Username created Successfully')
                return redirect('login')
        else:
            messages.info(request,'Password is not same')
            return redirect('register')     
    else:
        return render(request,'register.html')                                        


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Credentials invalid")
            return redirect('login')
    else:
        return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def dashboard(request):
    if request.method == 'POST' and 'username' in request.POST:
        username = request.POST['username']
        return render(request, 'dashboard.html', {'name': username})
    else:
        if request.user.is_authenticated:
            username = request.user.username
            return render(request, 'dashboard.html', {'name': username})
        else:
            return redirect('login')

@login_required
def videocall(request):
    username = request.user.username 
    return render(request, 'videocall.html', {'name': username })

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'joinroom.html')


# Create your views here.
def home(request):
    return render(request, 'home.html')

def room(request, room):
    username = request.GET.get('username')
    try:
        room_details = Room.objects.get(name=room)
    except Room.DoesNotExist:
        room_details = None  # Room doesn't exist

    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })


def checkview(request):
    if request.method == 'POST':
        try:
            room = request.POST['room_name']
            username = request.POST['username']
        except KeyError:
            raise Http404("Required POST data is missing")

        if Room.objects.filter(name=room).exists():
            return redirect('/'+room+'/?username='+username)
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect('/'+room+'/?username='+username)
    else:
        raise Http404("Only POST requests are allowed for this endpoint")

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request,room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room = room_details.id)
    return JsonResponse({"messages":list(messages.values())})