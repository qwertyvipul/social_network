from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .forms import *
from django.urls import reverse_lazy
from django.shortcuts import redirect

import numpy as np
import json
import face_recognition
import cv2



def index(request):
    return redirect('newsfeed:newsfeed')

def newsfeed(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')
    query = UserInfo.objects.filter(id=id)
    for user in query:
        break
    all_posts = NewsFeed.objects.all().order_by('time').reverse()

    form = StatusForm()
    context = {
        'user': user,
        'all_posts': all_posts,
        'statusForm': form,
    }
    return render(request, 'newsfeed/index.html', context)
    #return HttpResponse('<h1>You are viewing newsfeed</h1>')

def messages(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    query = UserInfo.objects.filter(id=id)
    for user in query:
        name = user.name

    all_messages = Messages.objects.all()
    context = {
        'name': name,
        'all_messages':all_messages,
    }
    return render(request, 'newsfeed/messages.html', context)

def notifcations(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    query = UserInfo.objects.filter(id=id)
    for user in query:
        name = user.name
    context = {
        'name': name,
    }
    return render(request, 'newsfeed/notifications.html', context)

def register(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
        if registerForm.is_valid():
            user = UserInfo()
            user.name = registerForm.cleaned_data['name']
            user.username = registerForm.cleaned_data['username']
            # You may not want to store plain text password in your database
            # This is just for testing purpose in real life it is not safe
            # You miss they hit!
            user.password = registerForm.cleaned_data['password']
            user.save()
            return redirect('newsfeed:login')
    else:
        form = RegisterForm()
        return render(request, 'newsfeed/register.html', context={'form':form})

def login(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            query = UserInfo.objects.filter(username=loginForm.cleaned_data['username'])
            query = query.filter(password=loginForm.cleaned_data['password'])
            total = query.count()
            if total==1:
                id = 0
                for result in query:
                    id = result.id

                request.session['user_id'] = id
                return redirect('newsfeed:newsfeed')

    form = LoginForm()
    return render(request, 'newsfeed/login.html', context={'form':form})

def logout(request):
    request.session['user_id']=0
    return redirect('newsfeed:login')

def postStatus(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    if request.method == "POST":
        statusForm = StatusForm(request.POST)
        if statusForm.is_valid():
            status = NewsFeed()
            query = UserInfo.objects.filter(id=id)
            for user in query:
                status.user = user
                break
            status.title = statusForm.cleaned_data['title']
            status.content = statusForm.cleaned_data['content']
            status.save()

    return redirect('newsfeed:newsfeed')


def uploadPhoto(request):
    pass

def likeStatus(request, status_id):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    query = UserInfo.objects.filter(id=id)
    for user in query:
        break

    query = NewsFeed.objects.filter(id=status_id)
    for status in query:
        break

    query = Likes.objects.filter(user=user)
    query = query.filter(newsfeed=status)
    if query.count()>0:
        for like in query:
            if like.has_liked:
                return HttpResponse('<h3>This is post has already been liked by you.</h3>')
            else:
                like.has_liked = True
                return redirect('newsfeed:newsfeed')
    like = Likes()
    like.user = user
    like.newsfeed = status
    like.has_liked = True
    like.save()

    return redirect('newsfeed:newsfeed')

def unlikeStatus(request):
    pass

def profile(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')
    query = UserInfo.objects.filter(id=id)
    for user in query:
        break

    query = ProfilePictures.objects.filter(user = user)
    profilePicForm = ProfilePicForm()
    context = {
        'user': user,
        'profilePicForm': profilePicForm,
        'query': query,
    }
    return render(request, 'newsfeed/profile.html', context)

def uploadProfilePic(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')

    if request.method == "POST":
        profilePicForm = ProfilePicForm(request.POST, request.FILES)
        if profilePicForm.is_valid():
            profilePic = ProfilePictures()
            query = UserInfo.objects.filter(id=id)
            for user in query:
                profilePic.user = user
                break
            profilePic.profile_pic = profilePicForm.cleaned_data['profile_pic']
            profilePic.save()

            new_data = {}
            new_data['people'] = []

            # Need a check that if a file does not exist skip to create file and adding the content
            with open('encodings.json') as infile:
                d = json.load(infile)

            for people in d['people']:
                new_data['people'].append({
                    'name': people['name'],
                    'encoding': people['encoding']
                })

            new_image = face_recognition.load_image_file(profilePic.profile_pic)
            face_location = face_recognition.face_locations(new_image)
            face_encoding = face_recognition.face_encodings(new_image, face_location)

            for encoding in face_encoding:
                new_data['people'].append({
                    'name': user.name,
                    'encoding': encoding.tolist()
                })
                break

            with open('encodings.json', 'w') as outfile:
                json.dump(new_data, outfile, indent=4)


            return redirect('newsfeed:profile')
        else:
            print(profilePicForm.errors)
            return HttpResponse(profilePicForm.errors)

    return HttpResponse("<h1>Return</h1>")
    return redirect('newsfeed:profile')

def liveAttendance(request):
    if request.session.has_key('user_id') and request.session['user_id']!=0:
        id = request.session['user_id']
    else:
        return redirect('newsfeed:login')



    #webcamDetection()
    all_names = webcamRecognition()

    query = UserInfo.objects.filter(id=id)
    for user in query:
        break

    context = {
        'user': user,
        'all_names': all_names,
    }
    return render(request, 'newsfeed/live-attendance.html', context)

def webcamDetection():

    print('Capturing video...')
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)

        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left) in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Draw a box around the face

        cv2.imshow('Video', frame)  # Display the resulting image

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Hit 'q' on the keyboard to quit!
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    return


def webcamRecognition():

    video_capture = cv2.VideoCapture(0)  # start capturing the video

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    with open('encodings.json') as infile:
        d = json.load(infile)

    name_list = []

    while True:
        ret, frame = video_capture.read()  # Grab a single frame of video
        small_frame = cv2.resize(frame, (0, 0), fx=0.25,
                                 fy=0.25)  # Resize frame of video to 1/4 size for faster face recognition processing
        rgb_small_frame = small_frame[:, :,
                          ::-1]  # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:

                for people in d['people']:
                    known_face_encodings = []
                    known_face_encodings.insert(0, np.array(people['encoding']))

                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:  # If a match was found in known_face_encodings, just use the first one.
                        first_match_index = matches.index(True)
                        name = people['name']
                        index = len(name_list)
                        face_names.append(name)
                        if name in name_list:
                            pass
                        else:
                            name_list.insert(index, name)

                        break



        process_this_frame = not process_this_frame

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Draw a box around the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255),
                          cv2.FILLED)  # Draw a label with a name below the face
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)  # Display the resulting image

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Hit 'q' on the keyboard to quit!
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    print(name_list)

    return name_list

