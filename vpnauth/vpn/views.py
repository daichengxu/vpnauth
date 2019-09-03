from django.shortcuts import render
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response,render,redirect
from vpn.forms import VpnForm

# Create your views here.
ERROR_MESSAGE = "Please enter a correct username and password. "

def index(request):
        form = VpnForm()
        return render_to_response('edit.html',{'form': form})

def save(request):
    if request.method == 'POST':
        form = VpnForm(request.POST)
        if form.is_valid():
            f_cd = form.cleaned_data
            data = authenticate(username=f_cd['username'],password=f_cd['password'])
            if data is not None:
                newpasswd=form.data['newpass']
                data.set_password(newpasswd)
                data.save()
                return render_to_response('password_change_done.html',{'newpasswd': newpasswd})
            else:
                return render_to_response('error.html')
    else:
        form = VpnForm()
    return render_to_response('edit.html',{'form': form})