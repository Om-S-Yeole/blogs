from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Category(models.Model):
    """Model for blog categories."""
    name = models.CharField(unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        """Automatically generate slug from the name."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    """Model for blog posts."""
    title = models.CharField(max_length=500)
    slug = models.SlugField(max_length=700, unique=True, blank=True, null=True)
    content = models.TextField()
    image = models.ImageField(default='/post_images/logo.png', upload_to='post_images')
    short_description = models.TextField(default="A post by Om.")
    categories = models.ManyToManyField(Category, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Automatically generate slug from the title."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    @property
    def likes(self):
        return Like.objects.filter(post=self)
    
    @property
    def comments(self):
        return Comment.objects.filter(post=self)


class Comment(models.Model):
    """Model for comments on blog posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user', 'content')  # Prevent duplicate comments from the same user.

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)  # To track when the like was made

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can like a post only once
        verbose_name = 'Like'
        verbose_name_plural = 'Likes'

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"