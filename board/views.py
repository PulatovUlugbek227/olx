from django.shortcuts import render, redirect, reverse
from .models import Post, Category, Profile, Gallery , View , Favourite, Region, Chat , Message
from django.http import HttpResponse, Http404
from django.db.models import Q
from .forms import RegisterForm
from random import randint
from django.core.files.storage import FileSystemStorage
from .translit import translit
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from django.contrib.auth.models import User
from .translit import translit
from random import randint
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage
def index(request):
    posts = Post.objects.filter(moderation=True).filter(publish=True)
    categories = Category.objects.all()
    regions = Region.objects.all()
    return render(request, 'board/index.html', {'posts':posts, 'categories' : categories, 'regions': regions})

# <--- |  Posts  | ---> #

def allpost(request):
    posts = Post.objects.filter(moderation=True).filter(publish=True).order_by('-date')
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    categories = Category.objects.all()
    max_price = max([post.price for post in Post.objects.all()])
    regions = Region.objects.all()
    return render(request, 'board/allpost.html', {'max_price':max_price, 'posts':posts , 'categories' : categories , 'regions':regions})


def post_detail(request, slug):
    post = Post.objects.filter(moderation=True).filter(publish=True).get(slug__exact=slug)
    categories = Category.objects.filter(parent=None)
    regions = Region.objects.filter(parent=None)
    if request.user.is_authenticated:
        if not post.view_set.filter(user=request.user).exists():
            post.view_set.create(user=request.user)
        else:
            post.view_set.get(user=request.user).date = timezone.now()
            post.view_set.get(user=request.user).save()
    return render(request,'board/post_detail.html',{'post' : post , 'categories':categories , 'regions':regions})

def show_phone(request, slug):
    if request.method == "POST":
        post = Post.objects.filter(moderation=True).filter(publish=True).get(slug__exact=slug)
        post.phone_views += 1
        post.save()
        return HttpResponse(post.user.profile.phone)
    return HttpResponse('Недопустимый метод')

def post_create(request):
    if request.user.is_authenticated:
        categories = Category.objects.all()
        regions = Region.objects.all()
        context = {'categories':categories, 'regions':regions}
        if request.method == "POST":
            post = Post()
            post.user = request.user
            post.title = request.POST.get('title')
            post.description = request.POST.get('description')
            new_slug = translit(request.POST.get('title'))
            if Post.objects.filter(slug__exact=new_slug).exists():
                post.slug = new_slug + '__' + str(timezone.now().format('Y-m-d_H-i-s')) + '__' + str(randint(1, 100))
            else:
                post.slug = new_slug
            if request.FILES.get('image', False) != False:
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                post.image = filename
            post.publish = request.POST.get('publish', False)
            post.moderation = request.POST.get('moderation', False)
            post.price = request.POST.get('price')
            post.save()
            category_ids = request.POST.getlist('categories[]')
            region_ids = request.POST.getlist('regions[]')
            for id in category_ids:
                post.category.add(id)
            for id in region_ids:
                post.region.add(id)
            return redirect('profile_posts')
        return render(request, 'board/post_create.html', context)
    return redirect('login')

def post_edit(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        users = User.objects.all()
        categories = Category.objects.all()
        regions = Region.objects.all()
        context = {'post':post, 'users':users, 'categories':categories, 'regions':regions}
        if request.method == "POST":
            post.title = request.POST.get('title')
            post.description = request.POST.get('description')
            if request.POST.get('title') != post.title:
                new_slug = translit(request.POST.get('title'))
                if Post.objects.filter(slug__exact=new_slug).exists():
                    post.slug = new_slug + str(post.id)
                else:
                    post.slug = new_slug
            if request.FILES.get('image', False) != False:
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                post.image = filename
            post.publish = request.POST.get('publish', False)
            post.moderation = request.POST.get('moderation', False)
            post.price = request.POST.get('price')
            post.save()
            category_ids = request.POST.getlist('categories[]')
            region_ids = request.POST.getlist('regions[]')
            post.category.set(category_ids)
            post.region.set(region_ids)
            return redirect('profile_posts')
        return render(request, 'board/posts_edit.html', context)    
    return redirect('login')

def post_delete(request,id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        post.delete()
        return redirect('profile_posts')
    return redirect('login')
    
def profile_post_gallery(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(id=id)
        if request.method == "POST":
            back_url = request.POST.get('back_url')
            ids = request.POST.getlist('images[]')
            for id in ids:
                image = Gallery.objects.get(id=id)
                post.gallery_set.add(image)
            return redirect(back_url)
        return render(request, 'board/profile_post_gallery.html', {'post':post})
    return redirect('index')

def gallery_create(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            back_url = request.POST.get('back_url')
            if request.FILES.get('image', False) != False:
                gallery = Gallery()
                gallery.post = Post.objects.get(id=id)
                gallery.title = request.POST.get('title')
                myfile = request.FILES['image']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                gallery.image = filename
                gallery.save()
            return redirect(back_url)
    return redirect('index')

def gallery_delete(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            back_url = request.POST.get('back_url')
            ids = request.POST.getlist('images[]')
            for id in ids:
                image = Gallery.objects.get(id=id)
                fs = FileSystemStorage()
                fs.delete(image.image.name)
                image.delete()
            return redirect(back_url)
    return redirect('index')
# <--- |  login & logout     | ---> #

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            _login(request, user)
            return redirect ('index')
    return render(request, 'board/login.html')

def logout(request):
    _logout(request)
    return redirect('index')

# <--- | Profile | ---> #

def profile(request):
    if request.user.is_authenticated:
        regions = Region.objects.all()
        if request.method == "POST":
            user = request.user
            user.first_name = request.POST.get('first_name') 
            user.last_name = request.POST.get('last_name') 
            if request.POST.get('password') != '':
                user.password = make_password(request.POST.get('password'))
            user.email = request.POST.get('email') 
            user.save()
            if not Profile.objects.filter(user=user).exists():
                profile = Profile()
                profile.user = user
                profile.save()
            profile = user.profile
            profile.phone = request.POST.get('phone') 
            profile.latitude = request.POST.get('latitude') 
            profile.longtitude = request.POST.get('longtitude')
            if request.POST.get('region', False) != False: 
                profile.region = Region.objects.get(id=request.POST.get('region')) 
            if request.FILES.get('avatar', False) != False:
                myfile = request.FILES['avatar']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                profile.avatar = filename
            profile.save()    
            return redirect('profile')
        posts = Post.objects.filter(user=request.user).order_by("-date")
        return render(request, 'board/profile.html', {'posts': posts, 'regions':regions})
    return redirect('register')

def profile_posts(request):
    if request.user.is_authenticated:
        posts = request.user.post_set.filter(moderation=True).filter(publish=True).order_by('-date')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, 'board/profile_posts.html', {'page_number':page_number, 'posts' : posts})
    return redirect('login')

def profile_archieved_posts(request):
    if request.user.is_authenticated:
        posts = request.user.post_set.filter(moderation=True).filter(publish=False).order_by('-date')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, 'board/profile_archieved.html', {'posts' : posts})
    return redirect('login')

def profile_moderating_posts(request):
    if request.user.is_authenticated:
        posts = request.user.post_set.filter(moderation=False).filter(publish=True).order_by('-date')
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, 'board/profile_moderating.html', {'posts' : posts})
    return redirect('login')


# <--- |       | ---> #



# <--- | Filters | ---> #

def filter(request):
    query = request.POST.get('search')
    categories = Category.objects.all()
    regions = Region.objects.all()
    category = Category.objects.get(id=request.POST.get('category'))
    region = Region.objects.get(id=request.POST.get('region'))
    from_price = request.POST.get('from_price')
    to_price = request.POST.get('to_price')
    sort = request.POST.get('sort')
    posts = category.posts.filter(moderation=True).filter(publish=True).filter(region=region).filter(Q(title__icontains=query)).filter(price__gte = from_price).filter(price__lte = to_price).order_by(sort)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    max_price = max([post.price for post in Post.objects.all()])
    context = {
        'query':query,
        'cat':category, 
        'reg':region, 
        'from':from_price, 
        'to':to_price, 
        'sort':sort,
        'posts':posts,
        'categories':categories,
        'regions':regions,
        'max_price': max_price,
    }
    return render(request, 'board/filter.html' , context)

def search(request):
    if request.method == "POST":
        categories = Category.objects.all()
        regions = Region.objects.all()
        query = request.POST.get('search')
        category = Category.objects.get(id = request.POST.get('category'))
        region = Region.objects.get(id = request.POST.get('region'))
        posts = Post.objects.filter(category=category).filter(region=region).filter(Q(title__icontains=query)).order_by('-date')
        paginator = Paginator(posts, 12)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        context = {
            'posts' : posts,
            'query' : query,
            'categories' : categories,
            'regions' : regions,
            'c' : category,
            'r' : region,
        }
        return render(request,'board/search.html', context)
    return redirect('index')

def category_detail(request, slug):
    categories = Category.objects.all()
    regions = Region.objects.all()
    category = Category.objects.get(slug__exact=slug)
    max_price = max([post.price for post in Post.objects.all()])
    posts = category.posts.filter(publish=True)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request,'board/category_detail.html', {'max_price':max_price,'category':category , 'posts': posts , 'categories':categories , 'regions':regions})

def region_detail(request, slug):
    regions = Region.objects.filter(parent=None)
    categories = Category.objects.filter(parent=None)
    region = Region.objects.get(slug__exact=slug)
    posts = region.posts.filter(publish=True)
    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    max_price = max([post.price for post in Post.objects.all()])
    posts = paginator.get_page(page_number)
    return render(request,'board/region_detail.html', {'max_price':max_price, 'region':region , 'posts': posts , 'categories':categories , 'regions':regions })


# <--- |       | ---> #



# <--- | Chats | ---> #

def send_chat(request, user_id, post_id):
    if request.user.is_authenticated:
        user = request.user
        reciever = User.objects.get(id=user_id)
        post = Post.objects.get(id=post_id)
        if not user.reciever_chats.filter(post=post).filter(sender=reciever).exists() and not user.sender_chats.filter(post=post).filter(reciever=reciever).exists():
            chat = Chat()
            chat.reciever = reciever
            chat.sender = user
            chat.post = post
            chat.save()
        elif user.sender_chats.filter(post=post).filter(reciever=reciever).exists():
            chat = user.sender_chats.filter(post=post).get(reciever=reciever)
        elif user.reciever_chats.filter(post=post).filter(sender=reciever).exists():
            chat = user.reciever_chats.filter(post=post).get(sender=reciever)
        return redirect(reverse('chat_detail_url', kwargs={'chat_id':chat.id}))
    return redirect('register')

def chats(request):
    if request.user.is_authenticated:
        chats = Chat.objects.filter(Q(reciever = request.user) | Q(sender = request.user)).order_by('-id')
        return render(request, 'board/chats.html', {'chats':chats})
    return redirect('login')

def chat_detail(request, chat_id):
    if request.user.is_authenticated:
        user = request.user
        chats = Chat.objects.filter(Q(reciever = request.user) | Q(sender = request.user)).order_by('-id')
        chat = Chat.objects.get(id=chat_id)
        if chat.reciever == request.user or chat.sender == request.user:
            messages = chat.message_set.exclude(user=request.user).order_by('-date')
            for message in messages:
                if message.readed == False:
                    message.readed = True
                    message.save()
            return render(request, 'board/chat_detail.html', {'chat':chat, 'chats': chats})
    return Http404('Пиздец')

def send_message(request, chat_id):
    if request.user.is_authenticated:
        if request.method == "POST":
            chat = Chat.objects.get(id=chat_id)
            chat.message_set.create(
                user = request.user,
                text = request.POST.get('text')
            )
        return redirect(reverse('chat_detail_url', kwargs={'chat_id':chat_id}))
    return redirect('login')

def delete_chat_detail(request, chat_id):
    if request.user.is_authenticated:
        user = request.user
        chat = Chat.objects.get(id=chat_id)
        if chat.reciever == request.user or chat.sender == request.user:
            messages = chat.message_set.order_by('-date')
            for message in messages:
                message.delete()
        return redirect('chat_detail_url')
    return Http404('Пиздец')

# <--- |       | ---> #



# <--- | Favourite | ---> #

def favourite(request):
    if request.user.is_authenticated:
        posts = Favourite.objects.filter(user=request.user)
        paginator = Paginator(posts, 12)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        return render(request, 'board/favourite.html' , {'posts':posts})
    return redirect('login')

def add_to_favourite(request, post_id):
    post = Post.objects.filter(moderation=True).filter(publish=True).get(id=post_id)
    if request.user.is_authenticated:
        if not request.user.favourite_set.filter(post = post).exists():
            item = Favourite()
            item.post = post
            item.user = request.user
            item.save()
        return redirect('index')
    return redirect('register')

def delete_favourite(request, item_id):
    item = Favourite.objects.get(id=item_id)
    if request.user.is_authenticated:
        item.delete()
        return redirect('favourite')
    return redirect('register')

# <--- |       | ---> #



# <--- | Regisration | ---> #

def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            profile = Profile()
            profile.user = user
            profile.save()
            return redirect('index')
        else:
            return HttpResponse('Попробуй снова')
    register_form = RegisterForm()
    return render(request, 'board/register.html' , {'register_form':register_form})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            _login(request, user)
            return redirect ('index')
    return render(request, 'board/login.html')   

def logout(request):
    _logout(request)
    return redirect('index')
