from django.db import models


class Group(models.Model):
    # admin = models.ForeignKey(User, on_delete=models.CASCADE)
    admin = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE)
    groupName = models.CharField(max_length=150, null=False)
    groupeProfile = models.ImageField(upload_to="group_profile_images", default="")
    groupeCover = models.ImageField(upload_to="groupe_cover_images", default="")
    bio = models.TextField()
    num_member = models.IntegerField(default=0, null=False)
    state = models.CharField(max_length=15) # private, public

    def __str__(self):
        return self.groupName


""" About member """
class Member(models.Model):
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.IntegerField() # user id


""" ______________________________ """


""" Group post """
class GroupPost(models.Model):
    owner = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.IntegerField() # user who post in the group
    post_status = models.TextField()
    num_like = models.IntegerField()
    num_comment = models.IntegerField()
    num_share = models.IntegerField()
    create_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.post_status

    class Meta:
        ordering = ["-create_at"]


""" Groupe post liked model """
class GroupPostLike(models.Model):
    # Already get notification
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    user_id = models.IntegerField()


""" Group post comment """
class GroupPostComment(models.Model):
    post = models.ForeignKey(GroupPost, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)