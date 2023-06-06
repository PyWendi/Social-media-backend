from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .manager import CustomUserManager

import uuid


def generate_custom_uid():
    uid = uuid.uuid4()
    uid_str = str(uid).replace("-", "")
    return uid_str

""" User model """

class CustomUser(AbstractBaseUser, PermissionsMixin):
    uid = models.CharField(max_length=32, unique=True, default=generate_custom_uid)
    fname  = models.CharField(max_length=150, null=False)
    lname  = models.CharField(max_length=200, null=False)
    tel = models.CharField(max_length=20, null=False) #Used for API auth
    country = models.CharField(max_length=100, blank=False, null=False)
    date_of_birth = models.DateField(editable=True)
    create_at = models.DateTimeField("User creation", auto_now_add=True)
    
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __str__(self):
        return self.email


""" User profile """
class Profile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_img = models.ImageField(upload_to="profile_images", default="AccountLogo.png")
    cover_img = models.ImageField(upload_to="cover_images", default="marvin-meyer-SYTO3xs06fU-unsplash.jpg")
    num_followers = models.IntegerField(default=0, null=False)
    num_friends = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.user.name


""" Invitations model """
class Invitation(models.Model):
    """
    1) user send invitation
    2) the other get the invitation and is notified for confirmation
    3) if the other user confirm or the owner of the account, this table is 'destroyed' and the different type of the request is set
    4) the friend list of each other get the id of the other one
    5) Then they become friend :) !!
    """
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    invite_id = models.IntegerField(null=True)
    type = models.CharField(max_length=15, null=False, default="demand")  # demand, confirmation
    # confirm = models.BooleanField(null=True, default=False)


""" Friend list model """
class FriendList(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    friend_id = models.IntegerField()


""" User followed """
class Follow(models.Model):
    owner = models.IntegerField() #Profile owner id
    user_followed_id = models.IntegerField(null=False, default=0)
    followed = models.BooleanField(null=False, default=True) #else unfollow


class PageFollowed(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    page_followed = models.IntegerField()


class GroupFollowed(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group_followed = models.IntegerField()


""" Post """
class Post(models.Model):
    # origin = post || share
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_status = models.TextField()
    create_at = models.DateTimeField("Date published", auto_now=True)
    # on shared, number become 0
    num_like = models.IntegerField(default=0)
    num_comment = models.IntegerField(default=0)
    Num_share = models.IntegerField(default=0)

    def __str__(self):
        return self.post_status

    class Meta:
        ordering = ["-create_at"]


class PostShared(models.Model):
    owner = models.IntegerField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    post_status = models.TextField()
    date_of_share = models.DateTimeField("Date of shared", auto_now=True)

    def __str__(self):
        return self.post_status

    class Meta:
        ordering = ["-date_of_share"]


class PostGroupShared(models.Model):
    post = models.ForeignKey("groups.GroupPost", on_delete=models.CASCADE)
    post_status = models.TextField()
    owner = models.IntegerField()
    date_of_share = models.DateTimeField("Date of shared", auto_now=True)

    def __str__(self):
        return self.post_status

    class Meta:
        ordering = ["-date_of_share"]


class PostPageShared(models.Model):
    post = models.ForeignKey("pages.PagePost", on_delete=models.CASCADE)
    post_status = models.TextField()
    owner = models.IntegerField()
    date_of_share = models.DateTimeField("Date of shared", auto_now=True)

    def __str__(self):
        return self.post_status


""" All post photo which is linked to a specific post"""
class PostPhoto(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="post_images")

""" Post comments """
class Comment(models.Model):
    commenter_id = models.IntegerField() #id of the commenter
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    create_at = models.DateTimeField("Date of comment", auto_now_add=True)
    text = models.TextField()


    def __str__(self):
        return self.text


class CommentShared(models.Model):
    commenter_id = models.IntegerField() #id of the commneter
    post = models.ForeignKey(PostShared, on_delete=models.CASCADE)
    create_at = models.DateTimeField("Date of comment", auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text


class CommentGroupShared(models.Model):
    commenter_id = models.IntegerField() #id of the commneter
    post = models.ForeignKey(PostGroupShared, on_delete=models.CASCADE)
    create_at = models.DateTimeField("Date of comment", auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text


class CommentPageShared(models.Model):
    commenter_id = models.IntegerField() #id of the commneter
    post = models.ForeignKey(PostPageShared, on_delete=models.CASCADE)
    create_at = models.DateTimeField("Date of comment", auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        return self.text

""" Like model """
class PostLiked(models.Model):
    user_id = models.IntegerField()
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False, null=False)


class PostSharedLike(models.Model):
    user_id = models.IntegerField()
    post_shared_id = models.ForeignKey(PostShared, on_delete=models.CASCADE)
    liked = models.BooleanField(null=False, default=False)


class PostGroupSharedLike(models.Model):
    user_id = models.IntegerField()
    post_shared_id = models.ForeignKey(PostGroupShared, on_delete=models.CASCADE)
    liked = models.BooleanField(null=False, default=False)


class PostPageSharedLike(models.Model):
    user_id = models.IntegerField()
    post_shared_id = models.ForeignKey(PostPageShared, on_delete=models.CASCADE)
    liked = models.BooleanField(null=False, default=False)


""" creating an historic for the user post that will be output"""
class PostHistoric(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post_origin = models.IntegerField(null=True)  # POST ID
    post_shared = models.IntegerField(null=True)  # POST SHARED ID
    post_group_shared = models.IntegerField(null=True) # POST GROUP SHARED ID
    post_page_share = models.IntegerField(null=True) # POST GROUP SHARED ID
    type = models.CharField(max_length=30, null=False, default="post")
    post_date = models.DateTimeField("post date", auto_now_add=True)

    class Meta:
        ordering = ["-post_date"]

    def __str__(self):
        return self.type


""" Notification according to the user actions """
class Notification(models.Model):
    """
    1) Select all friend 'pk'
    2) Select all notif user 'pk'
    3) Compare and append(pk) where f.pk = n.pk
    4) Select * comment on owner post
    5) List all notification with groupement
    """
    """ Entity id """
    owner = models.IntegerField(null=False, default=0)
    user_id = models.IntegerField(null=True) #Id of the user who performed the action | if in user friend list
    page_id = models.IntegerField(null=True) #Id of the page
    group_id = models.IntegerField(null=True) #Id of the group

    """ Major entity id """
    post_id = models.IntegerField(null=True) #Post id
    post_shared_id = models.IntegerField(null=True)

    post_group_shared_id = models.IntegerField(null=True)
    post_group_id = models.IntegerField(null=True) #group post id

    post_page_id = models.IntegerField(null=True) #page post id
    post_page_shared_id = models.IntegerField(null=True)

    """ like entity id """
    like_id = models.IntegerField(null=True)
    like_shared_id = models.IntegerField(null=True)
    like_group_shared_id = models.IntegerField(null=True)
    like_page_shared_id = models.IntegerField(null=True)

    """comment entity id"""
    comment_id = models.IntegerField(null=True)
    comment_share_id = models.IntegerField(null=True)
    comment_group_shared_id = models.IntegerField(null=True)
    comment_page_shared_id = models.IntegerField(null=True)

    """ Invitation state notif """
    invitation_id = models.IntegerField(null=True)

    """ 
    ["post","like", "comment","share",invitation, confirmation,"pdp","pdc",]
    ["group_post_like, post_group_share,post_group_comment"] owner post on group
    """
    notif_type = models.CharField(max_length=30)

    """ Date of action """
    date = models.DateTimeField("Notification date", auto_now_add=True)

    """ if seen or not """
    seen = models.BooleanField(default=False) #if seen

    class Meta:
        ordering = ["-date"]
