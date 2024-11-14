from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate
from datetime import date
import whisper
from django.http import HttpResponse
from django.core.files.storage import default_storage
import os
from django.conf import settings

# Create your views here.

def index(request):
    return render(request,'index.html')

def login(request):
    if request.POST:
        usname = request.POST["user"]
        pasw = request.POST["pass"]
        check_cust_user = authenticate(username=usname,password = pasw)
        if check_cust_user is not None:
                chef =UserReg.objects.get(email = usname)
                request.session['uid'] = chef.id
                
                messages.info(request,"Login successfull")
                return redirect("/userHome")
        else:
            messages.info(request,"Password not matching")
    return render(request,'login.html')

def Reg(request):
    if request.POST:
        name = request.POST["name"]
        phone = request.POST["phone"]
        email = request.POST["email"]
        password = request.POST["pass"]
        city = request.POST["add"]
        if CustomUser.objects.filter(username = email).exists():
            messages.info(request,"Email is taken")
        else:
            To_CustomUser = CustomUser.objects.create_user(first_name = name,
                                                          username = email,
                                                          password = password,
                                                          is_active = 1,
                                                          usertype = "user",
                                                          pswrd = password)
            To_CustomUser.save()
            To_User_Reg =UserReg.objects.create(usr_con = To_CustomUser,
                                                  name = name,
                                                  phone = phone,
                                                  email = email,
                                                  Address = city)
            To_User_Reg.save()
            messages.info(request,"Registered succesfully")
    return render(request,'Reg.html')

def userHome(request):
    id=request.session['uid']
    user=UserReg.objects.get(id=id)
    return render(request,'userHome.html',{"user":user})

import traceback
import re

def upload_audio(request):
    if request.method == 'POST' and request.FILES.get('audioFile'):
        try:
            # Ensure 'temp/' directory exists within MEDIA_ROOT
            temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            # Save the file temporarily
            audio_file = request.FILES['audioFile']
            cleaned_filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', audio_file.name)
            file_path = default_storage.save(f'temp/{cleaned_filename}', audio_file)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            with open(full_file_path, 'rb') as f:
                print("File can be accessed.")

            # Debug: Print the full path
            print(f"Processing file at: {full_file_path}")

            # Load the Whisper model
            model = whisper.load_model("tiny")

            # Process the audio file using the full path
            result = model.transcribe(full_file_path)
            transcribed_text = result['text']
            print(transcribed_text)
            print("File path:", full_file_path)
            print("Transcription result:", result)

            # Delete the temporary file
            default_storage.delete(file_path)

            # Return the transcribed text as plain text
            return HttpResponse(transcribed_text, content_type="text/plain")
        
        except Exception as e:
            # Print the full traceback for debugging
            print("An error occurred:", e)
            traceback.print_exc()
            return HttpResponse(f"An error occurred: {str(e)}", status=500)

    return HttpResponse("Invalid request", status=400)