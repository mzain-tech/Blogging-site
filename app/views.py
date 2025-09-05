from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from . models import Blog_post, Comment
from . forms import UserUpdateForm, Blogform
from django.contrib import messages
# Create your views here.

def register(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Password do not match')
            return redirect('register')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        messages.success(request, "Account created successfully!")

        return redirect('user_login')
    return render(request, 'register.html')


def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)

        if user:
            login(request,user)
            return redirect('dashboard_redirect')
        else:
            messages.error(request, 'Wrong username or password')
    return render(request, 'user_login.html')


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('user_login')

@login_required(login_url='user_login')
def dashboard_redirect(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        return redirect('user_dashboard')


#Admin dashboard view
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')
    total_users=User.objects.count()
    total_blogs=Blog_post.objects.count()
    published_blogs=Blog_post.objects.filter(status='approved').count()
    pending_blogs=Blog_post.objects.filter(status='pending').count()

    users=User.objects.all()
    blogs=Blog_post.objects.all()

    context={
        'total_users':total_users,
        'total_blogs':total_blogs,
        'published_blogs':published_blogs,
        'pending_blogs':pending_blogs,
        'users':users,
        'blogs':blogs,
    }
    return render(request, 'admin_dashboard.html', context)

# Block/Unblock users
@login_required
def block_user(request, user_id):
    if request.user.is_staff:
        user=get_object_or_404(User, id=user_id)
        user.is_active=False
        user.save()
    return redirect('admin_dashboard')

@login_required
def unblock_user(request, user_id):
    if request.user.is_staff:
        user=get_object_or_404(User, id=user_id)
        user.is_active=True
        user.save()
    return redirect('admin_dashboard')

@login_required
def approved_blog(request, blog_id):
    if request.user.is_staff:
        blog=get_object_or_404(Blog_post, id=blog_id)
        blog.status='approved'
        blog.save()
    return redirect('admin_dashboard')

@login_required
def reject_blog(request, blog_id):
    if request.user.is_staff:
        blog=get_object_or_404(Blog_post, id=blog_id)
        blog.status='rejected'
        blog.save()
    return redirect('admin_dashboard')


@login_required
def user_dashboard(request):
    posts=Blog_post.objects.filter(author=request.user)
    context={
        'posts':posts
    }
    return render(request, 'user_dashboard.html', context)

@login_required
def add_blog(request):
    if request.method=='POST':
        form = Blogform(request.POST, request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.author=request.user
            blog.save()
            form.save_m2m() #save tags
            messages.success(request, 'Blog added successfully!')
        return redirect('user_dashboard')
    else:
        form = Blogform()
    context={
        'form':form
    }
    return render(request, 'add_blog.html', context)

@login_required
def edit_blog(request,id):
    post = get_object_or_404(Blog_post, id=id, author=request.user)
    if request.method=='POST':
        form = Blogform(request.POST, request.FILES, instance=post)
        if form.is_valid():
            blog= form.save(commit=False)
            blog.author = request.user
            form.save()
            messages.success(request, 'Blog updated succesfully!')
            return redirect('user_dashboard')
    else:
        form= Blogform(instance=post)
    context={
        'form':form
    }
    return render(request, 'edit_blog.html', context)


def del_blog(request,id):
    post=get_object_or_404(Blog_post, id=id, author=request.user)
    if request.method=='POST':
        post.delete()
        messages.success(request, 'Blog Deleted successfully!')
        return redirect('user_dashboard')
    context={
        'post':post
    }
    return render(request, 'del_blog.html', context)



def home(request):
    posts = Blog_post.objects.filter(status='approved').order_by('-id')
    
    # Get the sort parameter
    sort = request.GET.get('sort')
    
    # Apply sorting if "most_viewed" is requested
    if sort == 'most_viewed':
        posts = posts.order_by('-views')  # Sort by views descending

    query = request.GET.get('q')
    author = request.GET.get('author')
    tag = request.GET.get('tag')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(author__username__icontains=query) | 
            Q(tags__name__icontains=query)
        )
    
    if author:
        posts = posts.filter(author__username__icontains=author)
    
    if tag:
        posts = posts.filter(tags__name__icontains=tag)

    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'author': author,
        'tag': tag,
        'sort': sort,  # Pass sort to template
    }
    return render(request, 'home.html', context)

@login_required
def update_profile(request):
    if request.method=='POST':
        form=UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_dashboard')
    else:
        form= UserUpdateForm(instance=request.user)

    context={
        'form':form
    }
    return render(request, 'update_profile.html', context)

def blog_detail(request, id):
    post=get_object_or_404(Blog_post,id=id)
    post.views +=1
    post.save(update_fields=['views'])
    post=Blog_post.objects.get(id=id)
    comments=post.comments.all().order_by('-created_at')
    if request.method=='POST':
        if request.user.is_authenticated:
            content=request.POST.get('content')
            if content:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    content=content,
                )
                return redirect('blog_detail', id=post.id)
        else:
            return HttpResponse('login required to comment.')
    context={
        'post':post,
        'comments':comments,
    }
    return render(request, 'blog_detail.html', context)



@login_required
def del_comment(request,id):
    comment=get_object_or_404(Comment,id=id)
    if request.user.is_superuser or request.user==comment.user:
        comment=Comment.objects.get(id=id)
        post_id=comment.post.id
        comment.delete()
        return redirect('blog_detail', id=post_id)
    
def analytics(request):
    top_posts=Blog_post.objects.order_by('-views')[:5]
    context={
        'top_posts':top_posts
    }
    return render(request, 'analytics.html',context)

@login_required
def del_user(request, user_id):
    user=get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('admin_dashboard')