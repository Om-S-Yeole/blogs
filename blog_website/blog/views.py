from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.http import JsonResponse, HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Category
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.conf import settings
from django.db.models import Count, Q
from django.contrib import messages
from django.core.files.storage import default_storage  # To delete old image file

def home(request):
    recent_posts = Post.objects.all().order_by('-created_at')[:3]
    most_liked_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:3]
    context = {
        'title': 'Home',
        'posts': recent_posts,
        'featured_posts': most_liked_posts,
    }
    return render(request, 'blog/home.html', context)

def about_me(request):
    context = {
        'title': 'About Me',
    }
    return render(request, 'blog/about_me.html', context)

def contact_us(request):
    context = {
        'title': 'Contact Us',
    }
    return render(request, 'blog/contact_us.html', context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/all_posts.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_categories = self.request.GET.getlist('categories')  # Get selected categories from query parameters
        search_query = self.request.GET.get('search', '')  # Get the search query from the query parameters

        # Filter by categories (intersection logic)
        if selected_categories:
            selected_category_ids = list(map(int, selected_categories))  # Convert selected category IDs to integers

            if len(selected_category_ids) == 1:
                # If only one category is selected, show all posts in that category
                queryset = queryset.filter(categories__id=selected_category_ids[0])
            else:
                # If multiple categories are selected, apply intersection logic
                for category_id in selected_category_ids:
                    queryset = queryset.filter(categories__id=category_id)

        # Filter by search query
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |  # Title contains search query (case insensitive)
                Q(content__icontains=search_query) |  # Content contains search query (case insensitive)
                Q(categories__name__icontains=search_query)  # Category name contains search query
            ).distinct()  # Use distinct to prevent duplicate results if a post matches multiple categories

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'All Posts'
        context['categories'] = Category.objects.all()  # Pass all categories to the template
        context['selected_categories'] = list(map(int, self.request.GET.getlist('categories')))  # Get selected categories
        context['search_query'] = self.request.GET.get('search', '')  # Pass the search query to the template
        return context

        
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'  # The object will be available as 'post' in the template

    def get_context_data(self, **kwargs):
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        
        # Get the current post object
        post = self.get_object()
        
        # Comments pagination
        comments = Comment.objects.filter(post=post).order_by('-created_at')  # Most recent comments first
        paginator = Paginator(comments, 4)  # Show 4 comments per page
        context['comments'] = paginator.page(1)  # Send only the first page of comments
        context['total_comments'] = comments.count()  # Total number of comments
        context['has_more_comments'] = paginator.num_pages > 1  # Whether more pages of comments exist

        # Add other context data
        context['total_likes'] = post.likes.count()  # Total number of likes
        context['categories'] = post.categories.all()  # Categories associated with the post
        
        # Check if the logged-in user has liked the post
        user = self.request.user
        if user.is_authenticated:
            context['has_liked'] = Like.objects.filter(user=user, post=post).exists()
        else:
            context['has_liked'] = False
        
        return context
    
class LoadCommentsView(View):
    def get(self, request, slug):
        # Get the blog post by slug
        post = Post.objects.get(slug=slug)

        # Get all comments for the post
        comments = Comment.objects.filter(post=post).order_by('-created_at')

        # Pagination: Show 4 comments per page
        page_number = request.GET.get('page', 1)  # Get page number from query params
        paginator = Paginator(comments, 4)

        try:
            page_obj = paginator.get_page(page_number)
        except:
            return JsonResponse({'error': 'Invalid page number'}, status=400)

        # Serialize the comments into JSON
        comments_data = []
        for comment in page_obj:
            comments_data.append({
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%B %d, %Y, %I:%M %p'),
            })

        # Return JSON response
        return JsonResponse({
            'comments': comments_data,
            'has_next': page_obj.has_next()
        })
    
@login_required
def like_post(request, slug):
    if not request.user.is_authenticated:
        # Redirect to login page with "next" parameter pointing to the current URL
        return redirect(f"{reverse('login')}?next={request.path}")

    # Retrieve the post
    post = get_object_or_404(Post, slug=slug)

    # Check if the user already liked the post
    like, created = Like.objects.get_or_create(post=post, user=request.user)

    if not created:  # If like already exists, remove it (unlike)
        like.delete()
        liked = False
    else:  # If like didn't exist, create it
        liked = True

    # Return the updated like count and liked status as JSON
    likes_count = post.likes.count()
    return JsonResponse({'liked': liked, 'likes_count': likes_count})

class AddCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        # Manually check if the user is authenticated
        if not request.user.is_authenticated:
            slug = kwargs.get('slug')  # Get the slug of the post
            # Redirect to login with `next` pointing to the post detail page
            return redirect(f"{settings.LOGIN_URL}?next=/posts/{slug}/")
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        text = request.POST.get('text')

        if text:  # Ensure the comment text is not empty
            Comment.objects.create(user=request.user, post=post, content=text)

        return redirect('post-detail', slug=slug)

    def get(self, request, slug):
        # Return a 405 Method Not Allowed response for GET requests
        return HttpResponseNotAllowed(["POST"])
    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    model= Category
    fields = ['name']

    def form_valid(self, form):
        messages.success(self.request, "Your New Category has been successfully created!")
        return super().form_valid(form)
class PostCreateView(LoginRequiredMixin, CreateView):
    model= Post
    fields = ['title', 'slug', 'content', 'image', 'short_description', 'categories']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been successfully created!")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        context['post_action'] = "Create New Post"
        context['post_method'] = "Post"

        return context
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'content', 'image', 'short_description', 'categories']

    def form_valid(self, form):
        post = self.get_object()  # Get the post being updated
        new_image = form.cleaned_data.get('image')  # Get the new image from the form

        # Check if the image is updated
        if new_image and post.image and post.image.name != new_image.name:
            # Delete the old image if it's not the default image
            if post.image.name != 'post_images/logo.png':  # Check to ensure not deleting the default image
                default_storage.delete(post.image.path)  # Delete old image from storage

        form.instance.author = self.request.user  # Set the author of the post
        messages.success(self.request, "Your Post has been successfully updated!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Get the default context from the superclass
        context = super().get_context_data(**kwargs)
        context['post_action'] = "Update Post"
        context['post_method'] = "Update"

        return context
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/"

    def form_valid(self, form):
        post = self.get_object()  # Get the post being deleted

        # Check if the image is updated
        if post.image:
            # Delete the old image if it's not the default image
            if post.image.name != 'post_images/logo.png':  # Check to ensure not deleting the default image
                default_storage.delete(post.image.path)  # Delete old image from storage

        messages.success(self.request, "Your Post has been successfully Deleted!")

        return super().form_valid(form)
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    success_url = reverse_lazy('blog-home')  # Redirect to blog homepage after deletion

    def form_valid(self, form):
        messages.success(self.request, "Comment deleted successfully.")
        return super().form_valid(form)

    def test_func(self):
        # Only allow superusers to delete comments
        return self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect non-superusers to the homepage or display an error message
        if self.request.user.is_authenticated:
            messages.error(self.request, "You do not have permission to delete this comment.")
            return redirect('blog-home')
        return super().handle_no_permission()