from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, UserManager, Books
from django.db.models import Count
import bcrypt

# Create your views here.


def index(request):
    request.session.flush()
    return render(request, 'index.html')


def register(request):  # post redirect
    if request.method == "POST":
        errors = User.objects.reg_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        # hash the password
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        # create a user
        new_user = User.objects.create(
            first_name=request.POST['first_name'], last_name=request.POST[
                'last_name'], email=request.POST['email'], password=hashed_pw
        )
        # create a session
        request.session['user_id'] = new_user.id
        return redirect('/success')
    return redirect('/')


# render the success page


def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'wall_messages' : Books.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'how_many' : Books.objects.filter(granted_wish=True).count,
        'how_many2' : Books.objects.filter(user_who_grants=request.session['user_id']).count,
        'how_many3' : Books.objects.filter(granted_wish=False).count,

        
        
        
        
    }

    return render(request, 'success.html', context)

def post_title(request):
    errors = Books.objects.message_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/success')
    else:
        user = User.objects.get(id=request.session["user_id"])
        book = Books.objects.create(
            message = request.POST['message'],
            description = request.POST['description'],
            poster = user
        )
    return redirect('/success')

def stats(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'wall_messages' : Books.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'how_many' : Books.objects.filter(granted_wish=True).count,
        'how_many2' : Books.objects.filter(user_who_grants=request.session['user_id']).count,
        'how_many3' : Books.objects.filter(granted_wish=False).count,

        
        
        
        
    }
    return render(request, 'stats.html', context)

def post_description(request):
    if request.method == 'POST':
        errors = Books.objects.message_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            Books.objects.create(description=request.POST['description'])
    return redirect('/success')

def like(request, id):
    
        user = User.objects.get(id=request.session["user_id"])
        book = Books.objects.get(id=id)
        book.user_who_grants=user
        book.granted_wish=True
        book.save()
        
        
        return redirect('/success')

def like1(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Books.objects.get(id=id)
    user.liked_books.add(book)
    
    return redirect('/success')

def unlike(request, id):
    user = User.objects.get(id=request.session["user_id"])
    book = Books.objects.get(id=id)
    user.liked_books.remove(book)
    messages.success(request, "Like removed")
    return redirect('/success')

# log in

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.filter(email=request.POST['email'])
        request.session['user_id'] = this_user[0].id
        return redirect('/success')
    return redirect('/')
# log out

def quote_page(request, user_id):
    this_user = User.objects.filter(id=user_id)
    context = {
        'one_user' : User.objects.get(id=user_id),
        'user': this_user[0],
        
        
    }
    return render(request, 'quote_page.html', context)

# grant wish

def make(request):
    if 'user_id' not in request.session:
        return redirect('/')
    this_user = User.objects.filter(id=request.session['user_id'])
    context = {
        'user': this_user[0],
        'wall_messages' : Books.objects.all(),
        'current_user': User.objects.get(id=request.session['user_id']),
        'how_many' : Books.objects.filter(granted_wish=True).count,
        'how_many2' : Books.objects.filter(user_who_grants=request.session['user_id']).count,
        'how_many3' : Books.objects.filter(granted_wish=False).count,

        
        
        
        
    }

    return render(request, 'make_a_quote.html', context)

def update(request, id):
    errors = User.objects.update_validator(request.POST)
    if errors:
        for key, value in errors.items():
            messages.error(request, value)
    else:
        account = User.objects.get(id=request.session['user_id'])
        account.first_name = request.POST['first_name']
        account.last_name = request.POST['last_name']
        account.email = request.POST['email']
        
        account.save()
    return redirect(f'/edit/{id}')

def edit(request, id):
    account = User.objects.get(id=request.session['user_id'])
    context = {
        'user_account' : account,
    }
    return render(request, "edit.html", context)

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

def delete_message(request, id):
    destroyed = Books.objects.get(id=id)
    destroyed.delete()
    return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')



