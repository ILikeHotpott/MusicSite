from django.utils import timezone
from app01.models import NotifiCenter, NotifiLikesPost, NotifiPostComment, NotifiCommentComment, Like, Comment, Moments

class Notification:

    def notify_comment(child, parent, nf_type):
        
        notifi_center = NotifiCenter.objects.create(
            user= parent.user,
            time=timezone.now(),
            read=False,
            types= nf_type
        )
        
        if nf_type == 1:
            NotifiPostComment.objects.create(
                notifi=notifi_center,
                post_id=parent.id,
                comment_id=child.id
            )
        else:
            NotifiCommentComment.objects.create(
                notifi=notifi_center,
                p_comment_id=parent.id,
                c_comment_id=child.id
            )
        parent.user.unread_count += 1
        parent.user.save()
        return
    
    def notify_like(like, moment):
        notifi_center = NotifiCenter.objects.create(
            user= moment.user,  
            time=timezone.now(),
            read=False,
            types=0  
        )
        NotifiLikesPost.objects.create(
            notifi=notifi_center,
            like=like
        )
        moment.user.unread_count += 1
        moment.user.save()
        return 