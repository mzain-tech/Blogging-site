from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User

# Create your models here.
class Blog_post(models.Model):
    STATUS_CHOICES=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    title=models.CharField(max_length=50)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE, related_name='blog')
    tags=TaggableManager()
    image=models.ImageField(upload_to='blogs/', blank=True, null=True)
    post_date=models.DateField( auto_now_add=True)
    is_active=models.BooleanField(default=False)
    status=models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    views=models.PositiveIntegerField(default=0)


    class Meta:
        ordering=['-post_date']

    def __str__(self):
        return self.title



class Comment(models.Model):
    post=models.ForeignKey(Blog_post, on_delete=models.CASCADE, related_name='comments')
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"