from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView

from goals.models import GoalCategory


class GoalCategoryPermission(IsAuthenticated):

    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        return request.user == obj.user


class GoalPermission(IsAuthenticated):

    def has_object_permission(self, request: Request, view: GenericAPIView, obj: GoalCategory) -> bool:
        return request.user == obj.user