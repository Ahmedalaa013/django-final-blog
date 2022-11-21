from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView,DetailView
from django.http import HttpResponseRedirect 
from django.urls import reverse

from .models import Post,fWord,Category,Tag
from .decorators import is_unauthenticated
from .forms import CreateUserForm,CreateCommentForm
# Create your views here.

@is_unauthenticated
def registerUser(request): 
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/login')
    context = {'form':form}
    return render(request,'registration/register.html',context)

@is_unauthenticated
def loginUser(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Sorry you are blocked, please contact the admin')

        else:
            messages.error(request,'Invalid credentials username or password is incorrect')
    return render(request,'registration/login.html')

def logoutUser(request):
    logout(request)
    return redirect('home')
   

class HomeView(ListView):
    model = Post
    template_name = 'myblog/home.html'
    ordering = ['-post_date']
    def get_context_data(self,*args,**kwargs):   
        context = super(HomeView,self).get_context_data(*args,**kwargs)
        get_categories = Category.objects.all()
        dic = {}
        for cat in get_categories:
            subscribed = False
            if cat.subscribe.filter(id=self.request.user.id).exists():
                subscribed = True
            dic[cat.name] = subscribed
        get_category = Category.objects.all()
        context['category'] = get_category
        context['subscribtions'] = dic 
        print(dic)
        return context

def subscriptionPostView(request):
        get_categories = Category.objects.all()
        posts = None
        for cat in get_categories:
            if cat.subscribe.filter(id=request.user.id).exists():
                cat_posts = Post.objects.filter(category=cat)
                if posts is None:
                    posts = cat_posts
                else:
                    posts = posts | cat_posts
        if posts:
            posts = posts.distinct() 
        return render(request,'myblog/subscriptions.html',context={'posts':posts})

class Post_detailView(DetailView):
    model = Post
    template_name = 'myblog/post_details.html'

    def get_context_data(self,*args,**kwargs):   
        context = super(Post_detailView,self).get_context_data(*args,**kwargs)
        get_post = get_object_or_404(Post,id=self.kwargs['pk'])
        
        comments = get_post.comments.all()
        total_likes = get_post.total_likes()
        liked = False
        if get_post.likes.filter(id=self.request.user.id).exists():
            liked = True
       
        total_dislikes = get_post.total_dislikes()
        disliked = False
        if get_post.dislikes.filter(id=self.request.user.id).exists():
            disliked = True
        context['total_likes'] = total_likes
        context['total_dislikes'] = total_dislikes
        context['liked'] = liked
        context['disliked'] = disliked
        context['comments'] = comments
        context['form'] = CreateCommentForm()
        return context
    
   
def comment(request,pk):
    post= get_object_or_404(Post,id=request.POST.get('post_id'))
    fwords = fWord.objects.all()
    user_comment =None
    if request.method == 'POST':
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.post = post
            user_comment.author = request.user
            for word in fwords:
                user_comment.content = user_comment.content.replace(word.word,"*"*len(word.word)) 
            user_comment.save()
            return HttpResponseRedirect(reverse('post_details',args=[str(pk)]))


def subscribe(request,pk):
    cat= get_object_or_404(Category,id=pk)
    if cat.subscribe.filter(id=request.user.id).exists():
        cat.subscribe.remove(request.user)
    else: 
        cat.subscribe.add(request.user)
    return HttpResponseRedirect(reverse('sub_list'))

def like(request,pk):
    post= get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False 
    else: 
        post.likes.add(request.user)
        if post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        liked = True
    return HttpResponseRedirect(reverse('post_details',args=[str(pk)]))

def dislike(request,pk):
    post= get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.dislikes.filter(id=request.user.id).exists():
        post.dislikes.remove(request.user)
        disliked = False 
    else: 
        post.dislikes.add(request.user)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        dislike= True
    return HttpResponseRedirect(reverse('post_details',args=[str(pk)]))


def get_category(request, id):
    category = get_object_or_404(Category,pk=id)
    return render(request,"myblog/category.html", context={"category":category})

def get_tag(request, id):
    post = Post.objects.filter(tag=id)
    return render(request,"myblog/tag.html", context={"posts":post})


def search(request):
    if request.method =='POST':
        term = request.POST['search_term']
        post_res = Post.objects.filter(title__contains=term)
        tag_res = Tag.objects.filter(name__contains=term)
        post_tag =None
        if tag_res:
            for tag in tag_res:
                tag_post = Post.objects.filter(tag=tag)
                if post_tag is None:
                    post_tag = tag_post
                else:
                    post_tag = post_tag | tag_post
                    if post_tag:
                        post_tag.distinct()
        return render(request,'myblog/search.html',context={'posts':post_res,'tags':post_tag,'term':term})
    else:
        return render(request,'myblog/search.html')