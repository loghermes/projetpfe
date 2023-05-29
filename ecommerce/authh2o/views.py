from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User 
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str ,DjangoUnicodeDecodeError 
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate ,update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
# Create your views here.

def Signup(request):
    if request.method=="POST":
        email=request.POST['email']
       
        password=request.POST['password1']
        
        confirm_password=request.POST['password2']
        if password != confirm_password:
            messages.warning(request,"Password is not matching")
            return render (request,'Signup.html')
        try :
            if User.objects.get(username=email):
                #return HttpResponse("email already exist")
                messages.info(request,"Email already taken")
                return render (request,"Signup.html")
        except Exception as identifier:
            pass
        user =User.objects.create_user(email,email,password)
        user.is_active=True
        user.save()
        email_subject="Active your Account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })



        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
        email_message.send()
        messages.success(request,'Activate your account by clicking the link in your Email')
        return redirect('/auth/Login/')    
    return render (request,"Signup.html")
class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:

            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.info(request,"Account Activated Successfully")
            return redirect('/auth/Login')
        return render(request,'activatefail.html')

def handlelogin(request):
    if request.method=="POST":

        username=request.POST['email']
        userpassword=request.POST['password1']
        myuser=authenticate(username=username ,password=userpassword)

        if myuser is not None :
            login(request,myuser)
            messages.success(request,"login success ")
            return redirect('/')
        else :
            messages.error(request,"Wrong credentials")
            return redirect('/auth/Login')
    return render (request,"Login.html")
        
def handlelogout(request):
    logout (request)
    messages.info(request,"logout Success")
    return redirect('/auth/Login')

def update_user (request): 
    if request.method=="POST":
        email=request.POST['email']
       
        password=request.POST['password1']
        
        confirm_password=request.POST['password2']
        if password != confirm_password:
            messages.warning(request,"Password is not matching")
            return render (request,'update_user.html')
    
        try :
            if User.objects.get(username=email):
                #return HttpResponse("email already exist")
                messages.info(request,"Email already taken")
                return render (request,"update_user")
        except Exception as identifier:
            pass
        user =User.objects.create_user(email,email,password)
        user.save()


class RequestResetEmailView(View):
    def get(self,request):
        return render(request,'request-reset-email.html')
    
    def post(self,request):
        email=request.POST['email']
        user=User.objects.filter(email=email)

        if user.exists():
            # current_site=get_current_site(request)
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token':PasswordResetTokenGenerator().make_token(user[0])
            })

            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.info(request,"WE HAVE SENT YOU AN EMAIL WITH INSTRUCTIONS ON HOW TO RESET THE PASSWORD " )
            return render(request,'request-reset-email.html')
        
class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64':uidb64,
            'token':token
        }
        try:
            user_id=force_bytes(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)

            if  not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"Password Reset Link is Invalid")
                return render(request,'request-reset-email.html')

        except DjangoUnicodeDecodeError as identifier:
            pass

        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        
        try:
            user_id=force_bytes(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Success Please Login with NewPassword")
            return redirect('/auth/Login/')

        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

        return render(request,'set-new-password.html',context)



        
def update_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('update_user')

        if request.user.check_password(password1):
            messages.error(request, "New password cannot be the same as your current password.")
            return redirect('update_user')

        # update user email and password
        if email is not None:
            request.user.email = email
        if password1 is not None:
            request.user.set_password(password1)
        request.user.save()

        messages.success(request, "Your profile has been updated.")
        return redirect('profile')
    else:
        return render(request, 'update_user.html')



