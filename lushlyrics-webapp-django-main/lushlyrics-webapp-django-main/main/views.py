from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import playlist_user
from django.urls.base import reverse
from django.contrib.auth import authenticate,login,logout
from youtube_search import YoutubeSearch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import json
# import cardupdate

f = open('card.json', 'r')
CONTAINER = json.load(f)

@login_required(login_url='/login/')
def default(request):
    global CONTAINER


    if request.method == 'POST':

        add_playlist(request)
        return HttpResponse("")

    song = 'kSFJGEHDCrQ'
    return render(request, 'player.html',{'CONTAINER':CONTAINER, 'song':song})


def playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)
    try:
      song = request.GET.get('song')
      song = cur_user.playlist_song_set.get(song_title=song)
      song.delete()
    except:
      pass
    if request.method == 'POST':
        add_playlist(request)
        return HttpResponse("")
    song = 'kSFJGEHDCrQ'
    user_playlist = cur_user.playlist_song_set.all()
    # print(list(playlist_row)[0].song_title)
    return render(request, 'playlist.html', {'song':song,'user_playlist':user_playlist})


def search(request):
  if request.method == 'POST':

    add_playlist(request)
    return HttpResponse("")
  try:
    search = request.GET.get('search')
    song = YoutubeSearch(search, max_results=10).to_dict()
    song_li = [song[:10:2],song[1:10:2]]
    # print(song_li)
  except:
    return redirect('/')

  return render(request, 'search.html', {'CONTAINER': song_li, 'song':song_li[0][0]['id']})


def add_playlist(request):
    cur_user = playlist_user.objects.get(username = request.user)

    if (request.POST['title'],) not in cur_user.playlist_song_set.values_list('song_title', ):

        songdic = (YoutubeSearch(request.POST['title'], max_results=1).to_dict())[0]
        song__albumsrc=songdic['thumbnails'][0]
        cur_user.playlist_song_set.create(song_title=request.POST['title'],song_dur=request.POST['duration'],
        song_albumsrc = song__albumsrc,
        song_channel=request.POST['channel'], song_date_added=request.POST['date'],song_youtube_id=request.POST['songid'])


def user_signup(request):
   if request.method == 'POST':
      first_name = request.POST.get('first_name')
      last_name = request.POST.get('last_name')
      username = request.POST.get('username')
      email = request.POST.get('email')
      password = request.POST.get('password')

      if User.objects.filter(username=username).exists():
        messages.info(request, 'Username already exists.')
        return redirect('/signup/')
      
      if User.objects.filter(email=email).exists():
        messages.info(request, 'Email is already registered. Please login to continue.')
        return redirect('/signup/')

      user = User.objects.create(first_name=first_name,last_name=last_name, username=username, email=email)
      user.set_password(password)

      user.save()
      messages.success(request, 'Account created. Please Login to continue.')

      return redirect('/signup/')
   return render(request, 'signup.html')

def user_login(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')

      if not User.objects.filter(username=username).exists():
        messages.error(request, 'Invalid Username')
        return redirect('/login/')
      
      user = authenticate(username = username, password = password)

      if user == None:
        messages.error(request, 'Incorrect Password')
        return redirect('/login/')
      else:
         login(request, user)
         return redirect('/')

   return render(request, 'login.html')

def user_logout(request):
   logout(request)
   return redirect('/login/')

def recover_password(request):
  if request.method == 'POST':
      email = request.POST.get('email')

  if not User.objects.filter(email=email).exists():
    messages.info(request, 'Email is not registered.')
    return redirect('/recover/')
  
  send_mail(
    "Password Recovery Mail",
    "Here is the message.",
    "from@example.com",
    ["to@example.com"],
    fail_silently=False,
  )
  return render(request, 'recover_password.html')