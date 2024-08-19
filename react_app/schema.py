import graphene
from graphene_django.types import DjangoObjectType
from app01.models import UserInfo, Moments, MomentComment


class UserType(DjangoObjectType):
    class Meta:
        model = UserInfo


class MomentsType(DjangoObjectType):
    class Meta:
        model = Moments


class MomentCommentType(DjangoObjectType):
    class Meta:
        model = MomentComment


class Query(graphene.ObjectType):
    users = graphene.List(UserType)
    moments = graphene.List(MomentsType)
    moment_comments = graphene.List(MomentCommentType, moment_id=graphene.Int())

    def resolve_users(self, info, **kwargs):
        return UserInfo.objects.all()

    def resolve_moments(self, info, **kwargs):
        return Moments.objects.all()

    def resolve_moment_comments(self, info, moment_id=None):
        if moment_id is not None:
            return MomentComment.objects.filter(moment_id=moment_id)
        return MomentComment.objects.all()


schema = graphene.Schema(query=Query)


class CharacterInterface(graphene.Interface):
    id = graphene.ID(required=True)
    name = graphene.String(required=True)
