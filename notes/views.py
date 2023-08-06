from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render



from .models import *


# Create your views here.
def about(request):
     return render(request,'about.html')
def index(request):
    return render(request,'index.html')
def contact(request):
    return render(request,'contact.html')
def userlogin(request):
    error = ""
    if request.method == 'POST':
    
        u =request.POST ['emailid']
        p =request.POST ['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error':error}
    return render(request,'login.html', d)


def admin_home(request):
    if not request.user.is_staff:
            return redirect('Admin')
    pn = Notes.objects.filter(status="pending").count()
    an = Notes.objects.filter(status="Accept").count()
    rn = Notes.objects.filter(status="Reject").count()
    alln = Notes.objects.all().count()

   
    d = {'pn': pn,'an': an,'rn': rn,'alln': alln,} 
    
    return render(request,'admin_home.html',d)  


def Admin(request):
    error = True
    if request.method == 'POST':
        u =request.POST ['uname']
        p =request.POST ['pwd']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error':error}
    return render(request,'Admin.html', d)

    
def signup1(request):
    error = ""
    if request.method == 'POST':
        a = request.POST ['firstname']
        b = request.POST ['lastname']
        c = request.POST ['contact']
        d = request.POST ['emailid']
        e = request.POST ['password']
        f = request.POST ['branch']
        g = request.POST ['role']
        try:
            user = User.objects.create_user(username=d, password=e, first_name=a, last_name=b)
            Signup.objects.create(user=user, contact=c, branch=f, role=g)
            error = "no"
        except:
            error = "yes"  
    d={'error':error}   
    return render(request,'signup.html',d)

def Logout(request):
    logout(request)
    return redirect('index')


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')       
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user)  
    d = {'data':data,'user':user}  
    return render(request,'profile.html',d)  
    
def edit_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')       
    user = User.objects.get(id=request.user.id)
    data = Signup.objects.get(user = user) 
    error = False
    if request.method == 'POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        c = request.POST['contact']
        b = request.POST['branch']
        user.first_name = f
        user.last_name = l
        data.contact = c
        data.branch = b
        user.save()
        data.save()
        error=True

    d = {'data':data,'user':user,'error':error}  
    return render(request,'edit_profile.html',d)  

def cpassword(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    error=""      
    if request.method=="POST":
        o = request.POST['old']
        n = request.POST['new']
        c = request.POST['confirm']
        if c==n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error="no"
        else:
            error="yes"
    d = {'error':error}
    return render(request,'cpassword.html',d)  

def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login') 
    error = ""
    if request.method == 'POST':
        b = request.POST ['branch']
        s = request.POST ['subject']
        p = request.POST ['semester']
        n = request.FILES ['notesfile']
        f = request.POST ['filetype']
        d = request.POST ['description']
        u = User.objects.filter(username=request.user.username).first()

        
        try:
            Notes.objects.create(user=u,uploadingdate=date.today(),branch=b,subject=s,semester=p,
                                 notesfile=n,filetype=f,description=d,status='pending')
            
            error = "no"
        except: 
            error = "yes"  
    d={'error':error}   
    return render(request,'upload_notes.html',d)

def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')       
    user = User.objects.get(id=request.user.id)
    notes = Notes.objects.filter(user = user) 
        
    d = {'notes':notes,}  
    return render(request,'view_mynotes.html',d)  


def delete_mynotes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login') 
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return redirect('view_mynotes')


def view_users(request):
    if not request.user.is_authenticated:
        return redirect('login')       
    user = Signup.objects.all()
   
    d = {'user':user,}  
    return render(request,'view_users.html',d)  

def delete_user(request,pid):
    if not request.user.is_authenticated:
        return redirect('Admin') 
    users = User.objects.get(id=pid)
    users.delete()
    return redirect('view_users')

def pending_notes(request):
    if not request.user.is_authenticated:
        return redirect('Admin')       
    notes = Notes.objects.filter(status = "pending")
    d = {'notes':notes}  
    return render(request,'pending_notes.html',d)  

def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('Admin')       
    notes = Notes.objects.filter(status = "Accept")
    d = {'notes':notes}  
    return render(request,'accepted_notes.html',d)  

def assign_status(request,pid):
    if not request.user.is_authenticated:
        return redirect('Admin') 
    notes = Notes.objects.get(id=pid)
    error = ""
    if request.method == 'POST':        
        s = request.POST ['status']
        try:
            notes.status = s
            notes.save()
            error = "no"
        except:
            error = "yes"  
    d = {'notes':notes,'error':error}
    return render(request,'assign_status.html',d)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('Admin')       
    notes = Notes.objects.filter(status = "Reject")
    d = {'notes':notes}  
    return render(request,'rejected_notes.html',d)  

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('Admin')       
    notes = Notes.objects.all()
    d = {'notes':notes}  
    return render(request,'all_notes.html',d)  


def delete_notes(request,pid):
    if not request.user.is_authenticated:
        return redirect('login') 
    notes = Notes.objects.get(id=pid)
    notes.delete()
    return redirect('all_notes')
    
def viewallnotes(request):
          
    notes = Notes.objects.filter(status="Accept")
    d = {'notes':notes}  
    return render(request,'viewallnotes.html',d)  

def bookfinder(request):
     return render(request,'bookfinder.html')

def book(request):
     return render(request,'book.html')

def syllabus(request):
     return render(request,'syllabus.html')

def syllabus1(request):
     return render(request,'syllabus1.html')


# def category(request):
#     notes = Notes.objects.all()
#     notes_filter = NotesFilter(request.GET, queryset=notes)
#     context = {
#         'notes_filter' : notes_filter
#     }
#     return render(request, "category.html", context)

def computerscience(request):
    notes = Notes.objects.all()
    notes = Notes.objects.filter(branch="Computer Science")
    d = {'notes':notes}  
    return render(request,'computerscience.html',d)  

def Civil(request):
    notes = Notes.objects.all()
    notes = Notes.objects.filter(branch="Civil")
    d = {'notes':notes}  
    return render(request,'Civil.html',d)  

def Electrical(request):
    notes = Notes.objects.all()
    notes = Notes.objects.filter(branch="Electrical")
    d = {'notes':notes}  
    return render(request,'Electrical.html',d)  

def Mechancial(request):
    notes = Notes.objects.all()
    notes = Notes.objects.filter(branch="Mechancial")
    d = {'notes':notes}  
    return render(request,'Mechancial.html',d)  

def Electronics(request):
    notes = Notes.objects.all()
    notes = Notes.objects.filter(branch="Electronics")
    d = {'notes':notes}  
    return render(request,'Electronics.html',d)  
