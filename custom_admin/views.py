from django.shortcuts import render, redirect, reverse
from board.models import Post, Category, Profile, Gallery , View , Favourite, Region, Chat , Message 
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.contrib.auth.models import User
from .translit import translit
from random import randint
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password

def index(request):
    return render(request, 'admin/index.html')

def posts(request):
    posts = Post.objects.all()
    return render(request, 'admin/posts/index.html', {'posts':posts})    

def post_create(request):
    users = User.objects.all()
    categories = Category.objects.all()
    regions = Region.objects.all()
    context = {'users':users, 'categories':categories, 'regions':regions}
    if request.method == "POST":
        post = Post()
        post.user = User.objects.get(id = request.POST.get('user'))
        post.title = request.POST.get('title')
        post.description = request.POST.get('description')
        new_slug = translit(request.POST.get('title'))
        if Post.objects.filter(slug__exact=new_slug).exists():
            post.slug = new_slug + '&' + str(timezone.now().format('Y-m-d_H-i-s')) + '__' + str(randint(1, 100))
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
        return redirect('admin.posts')
    return render(request, 'admin/posts/create.html', context)

def post_edit(request, id):
    post = Post.objects.get(id=id)
    users = User.objects.all()
    categories = Category.objects.all()
    regions = Region.objects.all()
    context = {'post':post, 'users':users, 'categories':categories, 'regions':regions}
    if request.method == "POST":
        post.user = User.objects.get(id = request.POST.get('user'))
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
        return redirect('admin.posts')
    return render(request, 'admin/posts/edit.html', context)

def post_delete(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('admin.posts')

def post_show(request, id):
    post = Post.objects.get(id=id)
    galleries = Gallery.objects.filter(post = None)
    return render(request, 'admin/posts/show.html', {'post':post, 'galleries': galleries})

def attach_to_post(request, id):
    post = Post.objects.get(id=id)
    if request.method == "POST":
        back_url = request.POST.get('back_url')
        ids = request.POST.getlist('images[]')
        for id in ids:
            image = Gallery.objects.get(id=id)
            post.gallery_set.add(image)
        return redirect(back_url)
    return redirect(reverse('admin.post.show', kwargs={'id':id}))

def post_moderated(request, id):
    if request.method == 'POST':
        post = Post.objects.get(id=id)
        post.moderation = request.POST.get('moderated')
        post.save()
    return redirect('admin.posts')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'admin/categories/index.html', {'categories':categories})

def category_create(request):
    if request.method == "POST":
        category = Category()
        category.title = request.POST.get('title')
        new_slug = translit(request.POST.get('title'))
        if Category.objects.filter(slug__exact=new_slug).exists():
                category.slug = new_slug + '__' + str(timezone.now().format('Y-m-d_H-i-s')) + '__' + str(randint(1, 100))
        else:
            category.slug = new_slug
        if Category.objects.filter(id=request.POST.get('parent')).exists():
            category.parent = Category.objects.get(id=request.POST.get('parent'))
        else:
            category.parent = None
        category.save()
        return redirect('admin.categories')
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'admin/categories/create.html', context)

def category_edit(request, id):
    category = Category.objects.get(id=id)
    categories = Category.objects.all()
    context = {'category':category, 'categories':categories}
    if request.method == "POST":
        category.title = request.POST.get('title')
        if Category.objects.filter(id=request.POST.get('parent')).exists():
            category.parent = Category.objects.get(id=request.POST.get('parent'))
        else:
            category.parent = None
        if request.POST.get('title') != category.title:
            new_slug = translit(request.POST.get('title'))
            if Category.objects.filter(slug__exact=new_slug).exists():
                category.slug = new_slug + str(category.id)
            else:
                category.slug = new_slug
        category.save()
        return redirect('admin.categories')
    return render(request, 'admin/categories/edit.html', context)

def category_delete(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('admin.categories')


def users(request):
    users = User.objects.all()
    return render(request, 'admin/users/index.html', {'users':users})


def user_create(request):
    regions = Region.objects.all()
    if request.method == "POST":
        user = User()
        user.username = request.POST.get('username') 
        user.first_name = request.POST.get('first_name') 
        user.last_name = request.POST.get('last_name') 
        user.password = make_password(request.POST.get('password'))
        user.email = request.POST.get('email') 
        user.save()
        profile = Profile()
        profile.user = user
        profile.phone = request.POST.get('phone') 
        profile.latitude = request.POST.get('latitude') 
        profile.longtitude = request.POST.get('longtitude') 
        profile.region = Region.objects.get(id=request.POST.get('region')) 
        if request.FILES.get('avatar', False) != False:
            myfile = request.FILES['avatar']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            profile.avatar = filename
        profile.save()
        return redirect('admin.users')
    context = {'regions':regions}
    return render(request, 'admin/users/create.html', context)

def user_edit(request, id):
    user = User.objects.get(id=id)
    regions = Region.objects.all()
    if request.method == "POST":
        user.username = request.POST.get('username') 
        user.first_name = request.POST.get('first_name') 
        user.last_name = request.POST.get('last_name') 
        if request.POST.get('password') != '':
            user.password = make_password(request.POST.get('password'))
        user.email = request.POST.get('email') 
        user.save()
        profile = user.profile
        profile.phone = request.POST.get('phone') 
        profile.latitude = request.POST.get('latitude') 
        profile.longtitude = request.POST.get('longtitude') 
        profile.region = Region.objects.get(id=request.POST.get('region')) 
        if request.FILES.get('avatar', False) != False:
            myfile = request.FILES['avatar']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            profile.avatar = filename
        profile.save()
        return redirect('admin.users')
    context = {'regions':regions, 'user':user}
    return render(request, 'admin/users/edit.html', context)

def user_delete(request, id):
    user = User.objects.get(id = id)
    user.delete()
    return redirect('admin.users')


def user_show(request, id):
    user = User.objects.get(id = id)
    return render(request, 'admin/users/show.html', {'user':user})


def regions(request):
    regions = Region.objects.all()
    return render(request, 'admin/regions/index.html', {'regions':regions})

def region_create(request):
    if request.method == "POST":
        region = Region()
        region.title = request.POST.get('title')
        new_slug = translit(request.POST.get('title'))
        if Region.objects.filter(slug__exact=new_slug).exists():
                region.slug = new_slug + '__' + str(timezone.now().format('Y-m-d_H-i-s')) + '__' + str(randint(1, 100))
        else:
            region.slug = new_slug
        if Region.objects.filter(id=request.POST.get('parent')).exists():
            region.parent = Region.objects.get(id=request.POST.get('parent'))
        else:
            region.parent = None
        region.save()
        return redirect('admin.regions')
    regions = Region.objects.all()
    context = {'regions':regions}
    return render(request, 'admin/regions/create.html', context)

def region_edit(request, id):
    region = Region.objects.get(id=id)
    regions = Region.objects.all()
    context = {'region':region, 'regions':regions}
    if request.method == "POST":
        region.title = request.POST.get('title')
        if Region.objects.filter(id=request.POST.get('parent')).exists():
            region.parent = Region.objects.get(id=request.POST.get('parent'))
        else:
            region.parent = None
        if request.POST.get('title') != region.title:
            new_slug = translit(request.POST.get('title'))
            if Region.objects.filter(slug__exact=new_slug).exists():
                region.slug = new_slug + str(region.id)
            else:
                region.slug = new_slug
        region.save()
        return redirect('admin.regions')
    return render(request, 'admin/regions/edit.html', context)

def region_delete(request, id):
    region = Region.objects.get(id=id)
    region.delete()
    return redirect('admin.regions')


def galleries(request):
    galleries = Gallery.objects.order_by('-date')
    return render(request, 'admin/galleries/index.html', {'galleries': galleries})

def gallery_create(request):
    if request.method == "POST":
        back_url = request.POST.get('back_url')
        gallery = Gallery()
        gallery.title = request.POST.get('title')
        if request.FILES.get('image', False) != False:
            myfile = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            gallery.image = filename
        gallery.save()
        return redirect(back_url)
    return redirect('galleries')
        
def gallery_delete(request):
    if request.method == "POST":
        back_url = request.POST.get('back_url')
        ids = request.POST.getlist('images[]')
        for id in ids:
            image = Gallery.objects.get(id=id)
            fs = FileSystemStorage()
            fs.delete(image.image.name)
            image.delete()
        return redirect(back_url)
    return redirect('admin.galleries.index')