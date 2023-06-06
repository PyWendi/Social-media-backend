from django.db import models

class Page(models.Model):
    admin = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    pageName = models.CharField(max_length=150, null=False)
    pageProfile = models.ImageField(upload_to="page_profile_images", default="")
    pageCover = models.ImageField(upload_to="page_cover_images", default="")
    bio = models.TextField()
    num_like = models.IntegerField(default=0, null=False)
    num_follower = models.IntegerField(default=0, null=False)

    def __str__(self):
        return self.pageName


""" About follower who follows the page """
class PageFollower(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    follow = models.BooleanField(default=True)
    description = models.CharField(max_length=250, null=True)

""" Page like by user """
class PageLike(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user_id = models.IntegerField()


"""  ____________________   """


""" Post page """
class PagePost(models.Model):
    page_owner = models.ForeignKey(Page, on_delete=models.CASCADE)
    post_status = models.TextField(null=True)
    num_like = models.IntegerField()
    num_coment = models.IntegerField()
    num_share = models.IntegerField()
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_status

    class Meta:
        ordering = ["-create_at"]


""" Like to a post """
class PagePostLike(models.Model):
    #If like, see post, if follow, get notification
    post = models.ForeignKey(PagePost, on_delete=models.CASCADE)
    user_id = models.IntegerField()


""" Page Post Comment """
class PagePostComment(models.Model):
    post = models.ForeignKey(PagePost, on_delete=models.CASCADE)
    user_id = models.IntegerField() # User id
    #owner_id = models.IntegerField() # page owner id
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text