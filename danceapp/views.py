from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .import models

# Create yfrom django.shortcuts import render

# Create your views here.
def index(request):
    students = models.User.objects.all()
    trainers = models.Trainer.objects.all()
    institutions = models.Institution.objects.all()
    dance_forms = models.Courses.objects.all()
    return render(request,'index.html', {
        'students': students,
        'trainers': trainers,
        'institutions': institutions,
        'dance_forms': dance_forms
    })


def userregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        age=request.POST.get('age')
        password=request.POST.get('password')
        gender=request.POST.get('gender')
        image=request.FILES.get('image')
        address=request.POST.get('address')
        batch_time = request.POST.get('batch_time')
        course_id = request.POST.get('course')

        if models.User.objects.filter(email=email).exists():
            return HttpResponse('<script>alert("email already exits");window.history.back();</script>')
        else:
            course = models.Courses.objects.get(id=course_id)
            user=models.User(name=name,age=age,email=email,password=password,Gender=gender,image=image,address=address,batch_time=batch_time,course=course)
            user.save()
            return redirect('userlogin')
    else: 
        courses = models.Courses.objects.all()
        return render(request,'userregister.html',{'courses': courses})


def userlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=models.User.objects.get(email=email)
            if user.password==password:
                if not user.is_approved or user.is_rejected:
                    return HttpResponse('<script>alert("Your registration is pending approval or rejected by the admin. Please wait for admin approval.");window.location.href="/";</script>')
                request.session['email']=email
                return redirect('userhome')
            else:
                return HttpResponse('<script>alert("Invalid password");window.history.back();</script>')
        except models.User.DoesNotExist:
            return HttpResponse('<script>alert("User not found");window.history.back();</script>')
    else:
        return render(request,'userlogin.html')
    

from django.utils import timezone

def userhome(request):
    if 'email' not in request.session:
        return redirect('userlogin')
    
    user = models.User.objects.get(email=request.session['email'])
    
    if not user.is_approved or user.is_rejected:
        return HttpResponse('<script>alert("Your registration is pending approval or rejected by the admin. Please wait for admin approval.");window.location.href="/";</script>')
    
    if not user.is_joined_institution:
        return render(request,'join_an_institution.html',{'user': user})
    
    # --- ADDED ATTENDANCE LOGIC ---
    # 1. Get today's date
    today = timezone.localtime(timezone.now()).date()
    
    # 2. Check if a record exists for this user for today
    has_marked_today = models.Attendance.objects.filter(user=user, date=today).exists()
    
    # 3. Pass 'needs_attendance' and 'user' to the template
    return render(request, 'userhome.html', {
        'user': user,
        'needs_attendance': not has_marked_today
    })

def mark_attendance(request):
    if request.method == 'POST':
        student = models.User.objects.get(email=request.session.get('email'))
        today = timezone.localtime(timezone.now()).date()
        
        # get_or_create ensures we don't accidentally create duplicates if they click twice
        models.Attendance.objects.get_or_create(
            user=student,
            date=today,
            defaults={'is_present': True}
        )
    return redirect('userhome')

def userprofile(request):
    if 'email' not in request.session:
        return redirect('userlogin')
    user=models.User.objects.get(email=request.session['email'])
    return render(request,'userprofile.html',{'user':user})

def usereditprofile(request):
    if 'email' not in request.session:
        return redirect('userlogin')
    user=models.User.objects.get(email=request.session['email'])
    if request.method=='POST':
        user.name=request.POST.get('name')
        user.email=request.POST.get('email')
        user.age=request.POST.get('age')
        user.password=request.POST.get('password')
        user.Gender=request.POST.get('Gender')
        user.address=request.POST.get('address')
        if 'image' in request.FILES:
            user.image=request.FILES.get('image')
        user.batch_time = request.POST.get('batch_time')

        user.save()
        return redirect('userprofile')
    return render(request,'usereditprofile.html',{'user':user})

def logout(request):
    request.session.flush()
    return redirect('index')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Trainer

def trainerregister(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        password = request.POST.get('password')
        gender = request.POST.get('Gender')
        phone = request.POST.get('phone')
        experiance = request.POST.get('experiance')
        category = request.POST.get('category')

        image = request.FILES.get('image')
        certificate = request.FILES.get('certificate')

        if Trainer.objects.filter(email=email).exists():
            return HttpResponse(
                '<script>alert("Email already exists");window.history.back();</script>'
            )
        course = models.Courses.objects.get(id=category)
        Trainer.objects.create(
            name=name,
            email=email,
            age=age,
            password=password,
            Gender=gender,
            phone=phone,
            experiance=experiance,
            course=course,
            image=image,
            certificate=certificate,
        )

        return redirect('trainerlogin')
    courses = models.Courses.objects.all()
    return render(request, 'trainerregister.html', {'courses': courses})

    
def trainerlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            user=models.Trainer.objects.get(email=email)
            if user.password==password:
                request.session['email']=email
                return redirect('trainerhome')
            else:
                return HttpResponse('<script>alert("Invalid password");window.history.back();</script>')
        except models.Trainer.DoesNotExist:
            return HttpResponse('<script>alert("User not found");window.history.back();</script>')
    else:
        return render(request,'trainerlogin.html')
    
from django.utils import timezone
from django.db.models import Sum

def trainerhome(request):
    if 'email' not in request.session:
        return redirect('trainerlogin')

    trainer = models.Trainer.objects.get(email=request.session['email'])

    institution = models.Institution.objects.filter(
        trainers__trainer=trainer
    ).first()

    # Students in this trainer's course + institution
    students = models.User.objects.filter(
        course=trainer.course,
        joined_institutions__institution=institution,
        joined_institutions__is_approved=True
    ).distinct()

    total_students = students.count()

    # ── ATTENDANCE ────────────────────────────────────────
    today = timezone.localtime(timezone.now()).date()

    present_today = models.Attendance.objects.filter(
        user__in=students,
        date=today,
        is_present=True
    ).count()

    attendance_percentage = (
        round((present_today / total_students) * 100)
        if total_students > 0 else 0
    )

    # ── EARNINGS ─────────────────────────────────────────
    # Sum all SUCCESSFUL payments from students in this trainer's batch
    total_paid = models.PaymentRecord.objects.filter(
        user__in=students,
        is_successful=True
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Trainer earns 30% of total fees collected from their students
    trainer_earnings = round(total_paid * 0.3, 2)

    # Per-student breakdown (optional — useful for a detail view later)
    paid_students_count = models.PaymentRecord.objects.filter(
        user__in=students,
        is_successful=True
    ).values('user').distinct().count()

    return render(request, 'trainerhome.html', {
        'trainer':               trainer,
        'institution':           institution,
        'total_students':        total_students,
        'present_today':         present_today,
        'absent_today':          total_students - present_today,
        'attendance_percentage': attendance_percentage,
        'today':                 today,
        'trainer_earnings':      trainer_earnings,      # ← ₹ amount trainer earns
        'total_fees_collected':  total_paid,            # ← total paid by all students
        'paid_students_count':   paid_students_count,   # ← how many students have paid
    })

def trainerprofile(request):
    trainer = Trainer.objects.get(email=request.session['email'])
    return render(request, 'trainerprofile.html', {'trainer': trainer})



def trainereditprofile(request, id):
    trainer = Trainer.objects.get(email=request.session['email'])

    if request.method == "POST":
        trainer.name = request.POST.get('name')
        trainer.email = request.POST.get('email')
        trainer.age = request.POST.get('age')
        trainer.password = request.POST.get('password')
        trainer.Gender = request.POST.get('Gender')
        trainer.phone = request.POST.get('phone')
        trainer.experiance = request.POST.get('experiance')
        trainer.category = request.POST.get('category')

        if request.FILES.get('image'):
            trainer.image = request.FILES.get('image')

        if request.FILES.get('certificate'):
            trainer.certificate = request.FILES.get('certificate')

        trainer.save()
        return redirect('trainerprofile')
    courses = models.Courses.objects.all()
    return render(request, 'trainereditprofile.html', {'trainer': trainer, 'courses': courses})

def institutionregister(request):
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        logo=request.FILES.get('logo')
        address=request.POST.get('address')
        phone=request.POST.get('phone')
        established_year=request.POST.get('established_year')
        location=request.POST.get('location')


        if models.Institution.objects.filter(email=email).exists():
            return HttpResponse('<script>alert("email already exits");window.history.back();</script>')
        else:
            institution=models.Institution(name=name,email=email,password=password,logo=logo,address=address,phone=phone,established_year=established_year,location=location)
            institution.save()
            return redirect('institutionlogin')
    else: 
        return render(request,'institutionregister.html')
    
def institutionlogin(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        try:
            institution=models.Institution.objects.get(email=email)
            if institution.password==password:
                if not institution.is_approved or institution.is_rejected:
                    return HttpResponse('<script>alert("Your registration is pending approval or rejected by the admin. Please wait for admin approval.");window.location.href="/";</script>')
                request.session['email']=email
                return redirect('institutiondashboard')
            else:
                return HttpResponse('<script>alert("invalid password");window.history.back();</script>')
        except models.Institution.DoesNotExist:
            return HttpResponse('<script>alert("Institution not found");window.history.back();</script>')
    else:
        return render(request,'institutionlogin.html')
    
def institutiondashboard(request):
    if 'email' not in request.session:
        return redirect('institutionlogin')
    institution = models.Institution.objects.get(email=request.session['email'])
    total_trainers = models.InstitutionTrainer.objects.filter(institution=institution).count()
    total_students = models.JoinInstitution.objects.filter(institution=institution, is_approved=True).count()
    return render(request,'institutiondashboard.html',{'institution': institution, 'total_trainers': total_trainers, 'total_students': total_students})

def institutionprofile(request):
    if 'email' not in request.session:
        return redirect('institutionlogin')
    user=models.Institution.objects.get(email=request.session['email'])
    return render(request,'institutionprofile.html',{'institution':user})

def institutioneditprofile(request):
    if 'email' not in request.session:
        return redirect('institutionlogin')

    user = models.Institution.objects.get(email=request.session['email'])

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.location = request.POST.get('location')
        user.established_year = request.POST.get('established_year')

        if request.FILES.get('logo'):
            user.logo = request.FILES['logo']

        user.save()
        return redirect('institutionprofile')

    return render(request, 'institutioneditprofile.html', {'institution': user})

def artistregister(request):
    if request.method == 'POST':
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        experience = request.POST.get('experience')
        specialization = request.POST.get('specialization')
        location = request.POST.get('location')
        password = request.POST.get('password')

        profile_photo = request.FILES.get('profile_photo')

        # Check if email already exists
        if models.Artist.objects.filter(email=email).exists():
            return HttpResponse('<script>alert("Email already exists");window.history.back();</script>')

        else:
            artist = models.Artist(
                name=name,
                email=email,
                phone=phone,
                gender=gender,
                age=age,
                experience_years=experience,
                specialization=specialization,
                location=location,
                password=password,
                profile_photo=profile_photo
            )
            artist.save()
            return redirect('artistlogin')

    else:
        return render(request,'artistregister.html')

def artistlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            artist = models.Artist.objects.get(email=email)   

            if artist.phone == phone:    
                request.session['email'] = email
                return redirect('artistdashboard')
            else:
                return HttpResponse('<script>alert("Invalid phone");window.history.back();</script>')

        except models.Artist.DoesNotExist:
            return HttpResponse('<script>alert("Email not found");window.history.back();</script>')

    return render(request, 'artistlogin.html')

    
def artistprofile(request):
    if 'email' not in request.session:
        return redirect('artistlogin')

    email = request.session.get('email')

    try:
        artist = models.Artist.objects.get(email=email)
    except models.Artist.DoesNotExist:
        return HttpResponse("<script>alert('Artist not found!');window.location='/artistlogin';</script>")

    return render(request, 'artistprofile.html', {'artist': artist})

def artistdashboard(request):
    if 'email' not in request.session:
        return redirect('artistlogin')
    return render(request,'artistdashboard.html')


def artisteditprofile(request):
    if 'email' not in request.session:
        return redirect('artistlogin')

    user = models.Artist.objects.get(email=request.session['email'])

    if request.method == "POST":
        user.name = request.POST.get('name')
        user.phone = request.POST.get('phone')
        user.email= request.POST.get('email')
        user.location = request.POST.get('location')
        user.gender = request.POST.get('gender')
        user.age = request.POST.get('age')
        user.experience_years = request.POST.get('experience_years')
        user.specialization = request.POST.get('specialization')
        
        if request.FILES.get('logo'):
            user.logo = request.FILES['logo']

        user.save()
        return redirect('artistprofile')

    return render(request, 'artisteditprofile.html', {'artist': user})


def shopregister(request):
    if request.method == 'POST':
        
        sname = request.POST.get('sname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        password = request.POST.get('password')

        shop_logo = request.FILES.get('shop_logo')

        # Check if email already exists
        if models.Shop.objects.filter(email=email).exists():
            return HttpResponse('<script>alert("Email already exists");window.history.back();</script>')

        else:
            shop = models.Shop(
                sname=sname,
                email=email,
                phone=phone,
                address=location,
                password=password,
                shop_logo=shop_logo
            )
            shop.save()
            return redirect('shoplogin')

    else:
        return render(request,'shopregister.html')
    
def shoplogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        try:
            shop = models.Shop.objects.get(email=email)   

            if shop.phone == phone:    
                request.session['email'] = email
                return redirect('shopdashboard')
            else:
                return HttpResponse('<script>alert("Invalid phone");window.history.back();</script>')

        except models.Shop.DoesNotExist:
            return HttpResponse('<script>alert("Email not found");window.history.back();</script>')

    return render(request, 'shoplogin.html')


def shopdashboard(request):
    if 'email' not in request.session:
        return redirect('shoplogin')
    return render(request,'shopdashboard.html')

def shopprofile(request):
    if 'email' not in request.session:
        return redirect('shoplogin')

    email = request.session.get('email')

    try:
        shop = models.Shop.objects.get(email=email)

    except models.Shop.DoesNotExist:
        return HttpResponse("<script>alert('shop not found!');window.location='/shoplogin';</script>")

    return render(request, 'shopprofile.html', {'shop': shop})

def shopeditprofile(request):
    if 'email' not in request.session:
        return redirect('shoplogin')

    user = models.Shop.objects.get(email=request.session['email'])

    if request.method == "POST":
        user.sname = request.POST.get('sname')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.password = request.POST.get('password')
       
        if request.FILES.get('logo'):
            user.logo = request.FILES['logo']

        user.save()
        return redirect('shopprofile')

    return render(request, 'shopeditprofile.html', {'shop': user})

def deleteprofile(request,id):
    user=models.User.objects.get(id=id)
    user.delete()
    return redirect('userlogin')

def trainerdeleteprofile(request,id):
    trainer=models.Trainer.objects.get(id=id)
    trainer.delete()
    return redirect('trainerlogin')

def shopdeleteprofile(request,id):
    shop=models.Shop.objects.get(id=id)
    shop.delete()
    return redirect('trainerlogin')

def artistdeleteprofile(request,id):
    artist=models.Artist.objects.get(id=id)
    artist.delete()
    return redirect('trainerlogin')

def user_list(request):
    users=models.User.objects.all()
    return render(request,'userlist.html',{'users':users})

def admindashboard(request):
    users = models.User.objects.all()
    trainers = models.Trainer.objects.all()
    institutions = models.Institution.objects.all()
    pending_institutions = models.Institution.objects.filter(is_approved=False)
    recent_students = models.User.objects.order_by('-id')[:5]  # Get the 5 most recent users
    no_of_students_present = models.Attendance.objects.filter(date=timezone.now().date(), is_present=True).count()
    no_of_students_absent = users.count() - no_of_students_present

    return render(request,'admindashboard.html', 
                  {'users': users, 'trainers': trainers, 
                   'institutions': institutions, 
                   'pending_institutions': pending_institutions, 
                   'recent_students': recent_students, 
                   'no_of_students_present': no_of_students_present, 
                   'no_of_students_absent': no_of_students_absent})

from django.http import JsonResponse
from django.utils import timezone
from . import models

def get_batch_attendance(request):
    # 1. Get the batch requested by the JavaScript
    batch = request.GET.get('batch')
    today = timezone.now().date()

    # 2. If a specific batch is selected
    if batch and batch != "":
        # Note: Change 'batch_timing' to whatever your actual field name is!
        total_students = models.User.objects.filter(batch_time=batch).count()
        
        present_count = models.Attendance.objects.filter(
            date=today, 
            is_present=True, 
            user__batch_time=batch  # Follow the relationship to the user's batch
        ).count()
        
    # 3. If "Select Batch Timing" (All) is selected
    else:
        total_students = models.User.objects.count()
        present_count = models.Attendance.objects.filter(
            date=today, 
            is_present=True
        ).count()

    absent_count = total_students - present_count

    # 4. Return the data as JSON
    return JsonResponse({
        'present': present_count,
        'absent': absent_count
    })

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        psw = request.POST.get('psw')
        if email=='admin@gmail.com' and psw=='admin':
            return redirect('admindashboard')
    return render(request,'adminlogin.html')

def trainer_list(request):
    users=models.Trainer.objects.all()
    return render(request,'trainerlist.html',{'users':users})

def shop_list(request):
    users=models.Shop.objects.all()
    return render(request,'shoplist.html',{'users':users})

def institution_list(request):
    users=models.Institution.objects.all()
    return render(request,'institutionlist.html',{'users':users})

def artist_list(request):
    users=models.Artist.objects.all()
    return render(request,'artistlist.html',{'users':users})

def deleteuser(request,id):
    user=models.User.objects.get(id=id)
    user.delete() 
    return redirect('userlist')

def approveuser(request, id):
    user = models.User.objects.get(id=id)
    user.is_approved = True
    user.is_rejected = False
    user.save()
    return redirect('userlist')

def rejectuser(request, id):
    user = models.User.objects.get(id=id)
    user.is_approved = False
    user.is_rejected = True
    user.save()
    return redirect('userlist')

def deletetrainer(request,id):
    user=models.Trainer.objects.get(id=id)
    user.delete() 
    return redirect('trainerlist')

def deleteshop(request,id):
    user=models.Shop.objects.get(id=id)
    user.delete() 
    return redirect('shoplist')

def deleteinstitution(request,id):
    user=models.Institution.objects.get(id=id)
    user.delete() 
    return redirect('institutionlist')

def deleteartist(request,id):
    user=models.Artist.objects.get(id=id)
    user.delete() 
    return redirect('artistlist')

from django.shortcuts import render, redirect
from . import models

def usertrainers(request):
    try:
        student = models.User.objects.get(email=request.session.get('email'))
    except models.User.DoesNotExist:
        return redirect('login')

    joined_entry = models.JoinInstitution.objects.filter(
        user=student,
        is_approved=True
    ).first()

    if joined_entry:
        institution = joined_entry.institution
        trainers = models.Trainer.objects.filter(
            institutions__institution=institution,
            course=student.course          # ← only trainers who teach the student's course
        ).distinct()
    else:
        trainers = models.Trainer.objects.none()

    return render(request, 'usertrainers.html', {
        'users': trainers,
        'student': student,
        'institution': joined_entry.institution if joined_entry else None
    })

def addproduct(request):
    institution=models.Institution.objects.get(email=request.session['email'])

    if request.method=='POST':
        product_name=request.POST.get('product_name')
        product_code=request.POST.get('product_code')
        category=request.POST.get('category')
        dance_form=request.POST.get('dance_form')
        size=request.POST.get('size')
        color=request.POST.get('color')
        material=request.POST.get('material')
        rental_price_per_day=request.POST.get('rental_price_per_day')
        product_image=request.FILES.get('product_image')
        descripition=request.POST.get('descripition')
        is_available=request.POST.get('is_available')
        quantity = int(request.POST.get('quantity', 1))

        product=models.Product(
            institution=institution,
            product_name=product_name,
            product_code=product_code,
            category=category,
            dance_form=dance_form,
            size=size,
            color=color,
            material=material,
            rental_price_per_day= rental_price_per_day,
            product_image=product_image,
            description=descripition,
            quantity=quantity,
            is_available=quantity > 0 and is_available == 'on'
             )
        
        product.save()
        return HttpResponse("<script>alert('product add successfully');window.location.href='/productlist/';</script>")
    dance_forms = models.Courses.objects.all()
    return render(request,'addproduct.html', {'dance_forms': dance_forms})

def productlist(request):
    if 'email' not in request.session:
        return redirect('institutionlogin')

    institution = models.Institution.objects.get(email=request.session['email'])
    product = models.Product.objects.filter(institution=institution)

    return render(request, 'productlist.html', {'product': product})


def editproductlist(request, id):
    if 'email' not in request.session:
        return redirect('institutionlogin')

    institution = models.Institution.objects.get(email=request.session['email'])

    try:
        product = models.Product.objects.get(id=id, institution=institution)

        if request.method == 'POST':
            product.product_name = request.POST.get('product_name')
            product.product_code = request.POST.get('product_code')
            product.category = request.POST.get('category')
            product.dance_form = request.POST.get('dance_form')
            product.size = request.POST.get('size')
            product.color = request.POST.get('color')
            product.material = request.POST.get('material')
            product.rental_price_per_day = request.POST.get('rental_price_per_day')
            product.description = request.POST.get('descripition')
            product.quantity = int(request.POST.get('quantity', product.quantity))

            # ✅ FIX Boolean
            product.is_available = True if request.POST.get('is_available') == 'on' else False

            # ✅ Update image only if new one uploaded
            if request.FILES.get('product_image'):
                product.product_image = request.FILES.get('product_image')

            product.save()

            return HttpResponse(
                "<script>alert('Product details updated successfully');window.location.href='/productlist/';</script>"
            )

    except models.Product.DoesNotExist:
        return redirect('productlist')

    return render(request, 'editproductlist.html', {'product': product})

def deleteproductlist(request,id):
    product=models.Product.objects.filter(id=id)
    product.delete()
    return redirect('productlist')


def userartist(request):
    users=models.Artist.objects.all()
    return render(request,'userartist.html',{'users':users})

def userinstitution(request):
    student = models.User.objects.get(email=request.session['email'])
    student_course = student.course 

    applied_institutions = models.JoinInstitution.objects.filter(
        user=student
    ).values_list('institution_id', flat=True)

    approved_institutions = models.JoinInstitution.objects.filter(
        user=student, is_approved=True
    ).values_list('institution_id', flat=True)

    rejected_institutions = models.JoinInstitution.objects.filter(
        user=student, is_rejected=True
    ).values_list('institution_id', flat=True)

    # FIX: Query Institution model directly using the 'trainers' related_name
    relevant_institutions = models.Institution.objects.filter(
        trainers__trainer__course=student_course
    ).distinct()

    if applied_institutions.exists():
        # Keep it as Institution objects
        display_institutions = relevant_institutions.filter(id__in=applied_institutions)
    else:
        display_institutions = relevant_institutions

    return render(request, 'userinstitution.html', {
        'users': display_institutions, # These are now Institution objects
        'student': student,
        'applied_institutions': list(applied_institutions),
        'approved_institutions': list(approved_institutions),
        'rejected_institutions': list(rejected_institutions)
    })

def usershop(request):
    users=models.Shop.objects.all()
    return render(request,'usershop.html',{'users':users})


# def addphotos(request):
#      return render(request,'addphotos.html')
            


def addphotos(request):
    if request.method == 'POST':
        dance_category = request.POST.get('dance_category')
        makeup_notes = request.POST.get('notes')
        images = request.FILES.getlist('makeup_images')
        for img in images:
            models.Photos.objects.create(
                dance_category=dance_category,
                makeup_Reference_image=img,
                makeup_notes=makeup_notes
            )

        return redirect('artistdashboard')  

    return render(request, 'addphotos.html')


def photolist(request):
    photos = models.Photos.objects.all().order_by('-id')
    return render(request, 'photolist.html', {'photos': photos})

def ViewProducts(request, id):
    shop = models.Shop.objects.filter(id=id).first()

    if not shop:
        return redirect('usershop')

    products = models.Product.objects.filter(shop=shop)

    return render(request, 'ViewProducts.html', {
        'shop': shop,
        'products': products
    })

def approveinstitution(request, id):
    institution = models.Institution.objects.get(id=id)
    institution.is_approved = True
    institution.is_rejected = False
    institution.save()
    return redirect('institutionlist')

def rejectinstitution(request, id):
    institution = models.Institution.objects.get(id=id)
    institution.is_approved = False
    institution.is_rejected = True
    institution.save()
    return redirect('institutionlist')

from .models import Feedback

def add_feedback(request):
    user = models.User.objects.get(email=request.session['email'])  # Get the logged-in user
    if request.method == "POST":
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        # Create the feedback object linked to the logged-in user
        Feedback.objects.create(
            user=user,
            rating=rating,
            comment=comment
        )
        return redirect('userhome')  # Redirect to user home after submitting feedback
        
    return render(request, 'add_feedback.html')


def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

from django.shortcuts import render, redirect
from .models import Courses
from django.contrib import messages

def add_course(request):
    if request.method == "POST":
        # Extract data from the form
        name = request.POST.get('course_name')
        desc = request.POST.get('description')
        dur = request.POST.get('duration')
        prc = request.POST.get('price')

        # Create and save the model instance
        Courses.objects.create(
            course_name=name,
            description=desc,
            duration=dur,
            price=prc
        )
        
        # Optional: add a success message
        messages.success(request, "Course added successfully!")
        return redirect('course_list') # Replace with your list view name

    return render(request, 'add_course.html')

def edit_course(request, id):
    course = Courses.objects.get(id=id)

    if request.method == "POST":
        course.course_name = request.POST.get('course_name')
        course.description = request.POST.get('description')
        course.duration = request.POST.get('duration')
        course.price = request.POST.get('price')
        course.save()
        messages.success(request, "Course updated successfully!")
        return redirect('course_list')

    return render(request, 'edit_course.html', {'course': course})

def course_list(request):
    courses = Courses.objects.all().order_by('-id')
    return render(request, 'course_list.html', {'courses': courses})

def delete_course(request, id):
    course = Courses.objects.get(id=id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect('course_list')

def trainerlist_institution(request):
    institution = models.Institution.objects.get(email=request.session['email'])
    users = models.InstitutionTrainer.objects.filter(institution=institution)
    return render(request, 'trainerlist_institution.html', {'users': users, 'institution': institution})

from django.shortcuts import render, redirect
from .models import Trainer, InstitutionTrainer, Institution

def add_trainer_institution(request):
    institution = Institution.objects.get(email=request.session['email'])

    if request.method == "POST":
        trainer_id = request.POST.get('trainer')
        trainer = Trainer.objects.get(id=trainer_id)

        # Check if trainer already assigned anywhere
        if InstitutionTrainer.objects.filter(trainer=trainer).exists():
            return HttpResponse("Trainer already assigned to another institution!")

        # Create the link
        InstitutionTrainer.objects.create(
            institution=institution,
            trainer=trainer
        )

        return redirect('trainerlist_institution')

    # Get all trainers already assigned anywhere
    assigned_trainers = InstitutionTrainer.objects.values_list('trainer_id', flat=True)

    # Show only unassigned trainers
    available_trainers = Trainer.objects.exclude(id__in=assigned_trainers)

    return render(request, 'add_trainer_institution.html', {
        'all_trainers': available_trainers
    })

def delete_trainer_institution(request, id):
    institution_trainer = InstitutionTrainer.objects.get(id=id)
    institution_trainer.delete()
    return redirect('trainerlist_institution')


#user clicks to join an institution
def join_institution(request, id):
    institution = Institution.objects.get(id=id)
    user = models.User.objects.get(email=request.session['email'])

    # Check if user already joined any institution
    if models.JoinInstitution.objects.filter(user=user).exists():
        return HttpResponse("You have already joined an institution!")

    # Create the link
    models.JoinInstitution.objects.create(
        user=user,
        institution=institution
    )

    return redirect('userinstitution')

def userlist_institution(request):
    institution = models.Institution.objects.get(email=request.session['email'])
    users=models.JoinInstitution.objects.filter(institution=institution).select_related('user').order_by('-joined_at')
    return render(request,'userlist_institution.html',{'users':users})

def delete_user_application(request, id):
    join_request = models.JoinInstitution.objects.get(id=id)
    join_request.delete()
    join_request.user.is_joined_institution = False
    join_request.user.save()    
    return redirect('userlist_institution')

def approve_request(request, id):
    join_request = models.JoinInstitution.objects.get(id=id)
    join_request.is_approved = True
    join_request.is_rejected = False
    join_request.save()
    join_request.user.is_joined_institution = True
    join_request.user.save()
    return redirect('userlist_institution')

def reject_request(request, id):
    join_request = models.JoinInstitution.objects.get(id=id)
    join_request.is_approved = False
    join_request.is_rejected = True
    join_request.save()
    join_request.user.is_joined_institution = False
    join_request.user.save()
    return redirect('userlist_institution')

def cancel_application(request, id):
    user = models.User.objects.get(email=request.session['email'])
    institution = Institution.objects.get(id=id)
    application = models.JoinInstitution.objects.filter(user=user, institution=institution).first()

    if application:
        application.delete()
        return HttpResponse("<script>alert('Application cancelled successfully');window.location.href='/userinstitution/';</script>")
    else:
        return HttpResponse("<script>alert('No application found to cancel');window.location.href='/userinstitution/';</script>")
    

def add_reel(request):
    trainer = Trainer.objects.get(email=request.session['email'])

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        video = request.FILES.get('video')

        reel = models.Reel.objects.create(
            trainer=trainer,
            title=title,
            description=description,
            video=video
        )

        return HttpResponse("<script>alert('Reel added successfully');window.location.href='/reel_list/';</script>")

    return render(request, 'add_reel.html')

def reel_list(request):
    # Fetch only the reels belonging to the logged-in trainer
    reels = models.Reel.objects.filter(
        trainer__email=request.session['email']
    ).order_by('created_at') # Assuming you added a created_at field, otherwise use '-id'
    
    return render(request, 'reel_list.html', {'reels': reels})

def delete_reel(request, id):
    reel = models.Reel.objects.get(id=id, trainer__email=request.session['email'])
    reel.delete()
    return redirect('reel_list')    

def edit_reel(request, id):
    reel = models.Reel.objects.get(id=id, trainer__email=request.session['email'])

    if request.method == 'POST':
        reel.title = request.POST.get('title')
        reel.description = request.POST.get('description')

        if request.FILES.get('video'):
            reel.video = request.FILES.get('video')

        reel.save()
        return HttpResponse("<script>alert('Reel updated successfully');window.location.href='/reel_list/';</script>")

    return render(request, 'edit_reel.html', {'reel': reel})


def view_trainer_reels(request, trainer_id):
    student_email = request.session.get('email')
    if not student_email:
        return redirect('userlogin')
        
    try:
        student = models.User.objects.get(email=student_email)
    except models.User.DoesNotExist:
        return redirect('userlogin')

    # 3. THE GATEWAY: Check if they have paid
    if not student.has_paid:
        # If they haven't paid, bounce them to the payment page
        return render(request, 'payment_require.html')

    # 4. If they have paid, proceed as normal!
    trainer = get_object_or_404(models.Trainer, id=trainer_id)
    reels = models.Reel.objects.filter(trainer=trainer).order_by('id') 
    
    return render(request, 'view_trainer_reels.html', {
        'trainer': trainer,
        'reels': reels
    })


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def initiate_payment(request):
    student = models.User.objects.get(email=request.session.get('email'))
    
    # --- NEW LOGIC: Fetch amount from the user's course ---
    # Safety Check: Ensure the user has a course and the course has a price
    if not student.course or not student.course.price:
        return HttpResponse("<script>alert('Error: Course price is not set. Please contact the administrator.');window.location.href='/userhome/';</script>")
    
    # Fetch the price (Convert to integer to drop any decimals if you only want flat rupees)
    amount = int(student.course.price) 
    amount_paise = amount * 100

    # Create the Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': '1' # Auto-capture
    })

    # Save a pending record in our new database model
    models.PaymentRecord.objects.create(
        user=student,
        razorpay_order_id=razorpay_order['id'],
        amount=amount
    )

    context = {
        'amount': amount,
        'api_key': settings.RAZORPAY_KEY_ID,
        'order_id': razorpay_order['id'],
        'user': student,
        'course_name': student.course.course_name # Passing this so you can show it on the checkout page!
    }

    # Render the HTML page where the user clicks "Pay Now"
    return render(request, 'razorpay_checkout.html', context)


# View 2: Razorpay sends data here after the user pays
@csrf_exempt 
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            # Verify the payment is real and not hacked
            client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # If successful, find the record and update it
            payment_record = models.PaymentRecord.objects.get(razorpay_order_id=order_id)
            payment_record.razorpay_payment_id = payment_id
            payment_record.is_successful = True
            payment_record.save()

            # UNLOCK THE APP FOR THE USER
            student = payment_record.user
            student.has_paid = True
            student.save()

            # Show the celebration page!
            return render(request, 'payment_success.html')

        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Payment Verification Failed. Please contact support.")

    return redirect('userhome')


import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

# ─── HELPER ────────────────────────────────────────────────────────────────────

def _get_conversation(user, trainer):
    """Return all messages between a specific user and trainer, oldest first."""
    return models.Message.objects.filter(
        Q(sender_user=user,    receiver_trainer=trainer) |
        Q(sender_trainer=trainer, receiver_user=user)
    ).order_by('timestamp')


# ─── STUDENT SIDE ──────────────────────────────────────────────────────────────

def user_chat_list(request):
    """Show the student a list of trainers they can chat with (same institution + course)."""
    if 'email' not in request.session:
        return redirect('userlogin')

    user = models.User.objects.get(email=request.session['email'])

    # Find institution the student has been approved into
    join = models.JoinInstitution.objects.filter(user=user, is_approved=True).first()
    if not join:
        return HttpResponse("You are not part of any institution yet.")

    # Trainers in that institution who teach the student's course
    trainers = models.Trainer.objects.filter(
        institutions__institution=join.institution,
        course=user.course
    ).distinct()

    return render(request, 'user_chat_list.html', {'trainers': trainers})


def user_chat_room(request, trainer_id):
    """Student ↔ Trainer chat room (student's perspective)."""
    if 'email' not in request.session:
        return redirect('userlogin')

    user    = models.User.objects.get(email=request.session['email'])
    trainer = get_object_or_404(models.Trainer, id=trainer_id)

    if user.has_paid == False:
        return render(request, 'payment_require.html')

    # Mark messages sent by trainer to this user as read
    models.Message.objects.filter(
        sender_trainer=trainer, receiver_user=user, is_read=False
    ).update(is_read=True)

    messages = _get_conversation(user, trainer)
    return render(request, 'chat_room.html', {
        'messages':   messages,
        'trainer':    trainer,
        'user':       user,
        'room_role':  'user',          # tells template who "me" is
        'send_url':   f'/chat/user/send/{trainer_id}/',
        'poll_url':   f'/chat/user/poll/{trainer_id}/',
    })


@require_POST
def user_send_message(request, trainer_id):
    """AJAX: student sends a message to trainer."""
    if 'email' not in request.session:
        return JsonResponse({'error': 'unauthenticated'}, status=401)

    user    = models.User.objects.get(email=request.session['email'])
    trainer = get_object_or_404(models.Trainer, id=trainer_id)
    content = request.POST.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'empty message'}, status=400)

    msg = models.Message.objects.create(
        sender_user=user,
        receiver_trainer=trainer,
        content=content,
    )
    return JsonResponse({
        'id':        msg.id,
        'content':   msg.content,
        'timestamp': msg.timestamp.strftime('%H:%M'),
        'sender':    'user',
    })


def user_poll_messages(request, trainer_id):
    """AJAX: return messages newer than ?after=<message_id>."""
    if 'email' not in request.session:
        return JsonResponse({'error': 'unauthenticated'}, status=401)

    user    = models.User.objects.get(email=request.session['email'])
    trainer = get_object_or_404(models.Trainer, id=trainer_id)
    after   = int(request.GET.get('after', 0))

    new_msgs = _get_conversation(user, trainer).filter(id__gt=after)

    # Mark incoming messages as read
    new_msgs.filter(sender_trainer=trainer).update(is_read=True)

    data = [{
        'id':        m.id,
        'content':   m.content,
        'timestamp': m.timestamp.strftime('%H:%M'),
        'sender':    'user' if m.sender_user else 'trainer',
    } for m in new_msgs]

    return JsonResponse({'messages': data})


# ─── TRAINER SIDE ──────────────────────────────────────────────────────────────

def trainer_chat_list(request):
    """Show the trainer a list of students they can chat with."""
    if 'email' not in request.session:
        return redirect('trainerlogin')

    trainer = models.Trainer.objects.get(email=request.session['email'])

    institution = models.Institution.objects.filter(
        trainers__trainer=trainer
    ).first()

    students = models.User.objects.filter(
        course=trainer.course,
        joined_institutions__institution=institution,
        joined_institutions__is_approved=True,
    ).distinct()

    # Annotate unread count per student
    for student in students:
        student.unread_count = models.Message.objects.filter(
            sender_user=student, receiver_trainer=trainer, is_read=False
        ).count()

    return render(request, 'trainer_chat_list.html', {'students': students, 'trainer': trainer})


def trainer_chat_room(request, user_id):
    """Student ↔ Trainer chat room (trainer's perspective)."""
    if 'email' not in request.session:
        return redirect('trainerlogin')

    trainer = models.Trainer.objects.get(email=request.session['email'])
    user    = get_object_or_404(models.User, id=user_id)

    models.Message.objects.filter(
        sender_user=user, receiver_trainer=trainer, is_read=False
    ).update(is_read=True)

    messages = _get_conversation(user, trainer)
    return render(request, 'chat_room.html', {
        'messages':  messages,
        'trainer':   trainer,
        'user':      user,
        'room_role': 'trainer',
        'send_url':  f'/chat/trainer/send/{user_id}/',
        'poll_url':  f'/chat/trainer/poll/{user_id}/',
    })


@require_POST
def trainer_send_message(request, user_id):
    """AJAX: trainer sends a message to student."""
    if 'email' not in request.session:
        return JsonResponse({'error': 'unauthenticated'}, status=401)

    trainer = models.Trainer.objects.get(email=request.session['email'])
    user    = get_object_or_404(models.User, id=user_id)
    content = request.POST.get('content', '').strip()

    if not content:
        return JsonResponse({'error': 'empty message'}, status=400)

    msg = models.Message.objects.create(
        sender_trainer=trainer,
        receiver_user=user,
        content=content,
    )
    return JsonResponse({
        'id':        msg.id,
        'content':   msg.content,
        'timestamp': msg.timestamp.strftime('%H:%M'),
        'sender':    'trainer',
    })


def trainer_poll_messages(request, user_id):
    """AJAX: return messages newer than ?after=<message_id>."""
    if 'email' not in request.session:
        return JsonResponse({'error': 'unauthenticated'}, status=401)

    trainer  = models.Trainer.objects.get(email=request.session['email'])
    user     = get_object_or_404(models.User, id=user_id)
    after    = int(request.GET.get('after', 0))

    new_msgs = _get_conversation(user, trainer).filter(id__gt=after)
    new_msgs.filter(sender_user=user).update(is_read=True)

    data = [{
        'id':        m.id,
        'content':   m.content,
        'timestamp': m.timestamp.strftime('%H:%M'),
        'sender':    'user' if m.sender_user else 'trainer',
    } for m in new_msgs]

    return JsonResponse({'messages': data})

def trainer_student_list(request):
    if 'email' not in request.session:
        return redirect('trainerlogin')

    trainer = models.Trainer.objects.get(email=request.session['email'])

    institution = models.Institution.objects.filter(
        trainers__trainer=trainer
    ).first()

    if institution:
        students = models.User.objects.filter(
            course=trainer.course,
            joined_institutions__institution=institution,
            joined_institutions__is_approved=True,
        ).distinct()
    else:
        students = models.User.objects.none()

    return render(request, 'trainer_user_list.html', {
        'students': students,
        'trainer': trainer,
        'institution': institution,
    })


def product_list_user(request):
    """Browse available costumes from the student's institution."""
    if 'email' not in request.session:
        return redirect('userlogin')

    user = models.User.objects.get(email=request.session['email'])

    # Only show costumes from the institution the student has joined
    join = models.JoinInstitution.objects.filter(
        user=user, is_approved=True
    ).first()

    if join:
        products = models.Product.objects.filter(
            institution=join.institution
        )
    else:
        # Not yet in an institution — show nothing with a message
        products = models.Product.objects.none()
    dance_forms = models.Courses.objects.all()
    return render(request, 'product_list_user.html', {
        'products': products,
        'user':     user,
        'join':     join,
        'dance_forms': dance_forms,

    })

from django.db.models import Q
from django.utils import timezone
from datetime import datetime
def book_costume(request, product_id):
    if 'email' not in request.session:
        return redirect('userlogin')

    user    = models.User.objects.get(email=request.session['email'])
    product = get_object_or_404(models.Product, id=product_id)

    # Check availability by quantity
    if not product.is_available or product.quantity < 1:
        return HttpResponse(
            '<script>alert("This item is currently out of stock.");</script>'
            'window.location.href="/product_list_user/";</script>'
        )

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date', '').strip()
        to_date_str   = request.POST.get('to_date', '').strip()
        notes         = request.POST.get('notes', '').strip()

        if not from_date_str or not to_date_str:
            return HttpResponse('<script>alert("Please select both dates.");window.history.back();</script>')

        try:
            fd = datetime.strptime(from_date_str, '%Y-%m-%d').date()
            td = datetime.strptime(to_date_str,   '%Y-%m-%d').date()
        except ValueError:
            return HttpResponse('<script>alert("Invalid date format.");window.history.back();</script>')

        today = timezone.localtime(timezone.now()).date()

        if fd < today:
            return HttpResponse('<script>alert("Pickup date cannot be in the past.");window.history.back();</script>')

        if td <= fd:
            return HttpResponse('<script>alert("Return date must be after pickup date.");window.history.back();</script>')

        quantity     = int(request.POST.get('quantity', 1))
        quantity     = max(1, min(quantity, product.quantity))

        total_days   = (td - fd).days
        rental_total = total_days * quantity * product.rental_price_per_day
        grand_total  = rental_total

        booking = models.CostumeBooking.objects.create(
            user         = user,
            product      = product,
            from_date    = fd,
            to_date      = td,
            total_days   = total_days,
            rental_total = rental_total,
            grand_total  = grand_total,
            notes        = notes,
            quantity     = quantity,
        )

        return redirect('initiate_booking_payment', booking_id=booking.id)

    today = timezone.localtime(timezone.now()).date()
    return render(request, 'book_costume.html', {
        'product': product,
        'user':    user,
        'today':   today,
    })


import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def initiate_booking_payment(request, booking_id):
    """Create Razorpay order for a costume booking."""
    if 'email' not in request.session:
        return redirect('userlogin')

    user    = models.User.objects.get(email=request.session['email'])
    booking = get_object_or_404(
        models.CostumeBooking, id=booking_id, user=user
    )

    # Guard: don't create another payment if already paid
    if hasattr(booking, 'payment') and booking.payment.is_successful:
        return redirect('user_bookings')

    amount       = int(booking.grand_total)   # rupees
    amount_paise = amount * 100

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpay_order = client.order.create({
        'amount':          amount_paise,
        'currency':        'INR',
        'payment_capture': '1',
    })

    # Save pending payment record
    models.BookingPayment.objects.update_or_create(
        booking  = booking,
        defaults = {
            'user':              user,
            'razorpay_order_id': razorpay_order['id'],
            'amount':            amount,
            'is_successful':     False,
        }
    )

    return render(request, 'booking_checkout.html', {
        'booking':    booking,
        'product':    booking.product,
        'amount':     amount,
        'api_key':    settings.RAZORPAY_KEY_ID,
        'order_id':   razorpay_order['id'],
        'user':       user,
    })


@csrf_exempt
def booking_payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id   = request.POST.get('razorpay_order_id', '')
        signature  = request.POST.get('razorpay_signature', '')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id':   order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature':  signature,
            })

            payment                     = models.BookingPayment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.is_successful       = True
            payment.save()

            booking        = payment.booking
            booking.status = 'paid'
            booking.save()

            # ── Decrease quantity ──────────────────────────
            product          = booking.product
            product.quantity = max(0, product.quantity - booking.quantity)  # ← use booking.quantity
            product.is_available = product.quantity > 0
            product.save()
            # ───────────────────────────────────────────────

            return render(request, 'booking_payment_success.html', {
                'booking': booking,
                'payment': payment,
            })

        except razorpay.errors.SignatureVerificationError:
            return HttpResponse("Payment verification failed. Please contact support.")

    return redirect('user_bookings')


def user_bookings(request):
    """Student sees all their bookings."""
    if 'email' not in request.session:
        return redirect('userlogin')

    user     = models.User.objects.get(email=request.session['email'])
    bookings = models.CostumeBooking.objects.filter(user=user).select_related(
        'product', 'product__institution'
    )

    return render(request, 'user_bookings.html', {
        'bookings': bookings,
        'user':     user,
    })


def cancel_booking(request, booking_id):
    """Student cancels a pending booking."""
    if 'email' not in request.session:
        return redirect('userlogin')

    user    = models.User.objects.get(email=request.session['email'])
    booking = get_object_or_404(
        models.CostumeBooking,
        id=booking_id,
        user=user,
        status='pending'
    )
    booking.delete()
    return redirect('user_bookings')

# ══════════════════════════════════════════════════════
#  INSTITUTION SIDE — Manage Bookings
# ══════════════════════════════════════════════════════

def institution_booking_requests(request):
    if 'email' not in request.session:
        return redirect('institutionlogin')

    institution = models.Institution.objects.get(email=request.session['email'])
    bookings    = models.CostumeBooking.objects.filter(
        product__institution=institution
    ).select_related('user', 'product').order_by('-booked_at')

    return render(request, 'institution_booking_requests.html', {
        'bookings':       bookings,
        'institution':    institution,
        'paid_count':     bookings.filter(status='paid').count(),
        'returned_count': bookings.filter(status='returned').count(),
    })


def mark_costume_returned(request, booking_id):
    if 'email' not in request.session:
        return redirect('institutionlogin')

    institution = models.Institution.objects.get(email=request.session['email'])
    booking     = get_object_or_404(
        models.CostumeBooking,
        id=booking_id,
        product__institution=institution,
        status='paid'
    )

    booking.status = 'returned'
    booking.save()

    # ── Increase quantity back ─────────────────────────────
    product          = booking.product
    product.quantity = product.quantity + booking.quantity
    product.is_available = True
    product.save()
    # ───────────────────────────────────────────────────────

    return redirect('institution_booking_requests')