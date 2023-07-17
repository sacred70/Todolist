from django.urls import path

from goals.views.comments import GoalCommentCreateView, GoalCommentListView, GoalCommentDetailView
from goals.views.goals import GoalListView, GoalCreateView, GoalDetailView
from goals.views.categories import CategoryCreateView, CategoryListView, CategoryDetailView


urlpatterns = [
    path('goal_category/create', CategoryCreateView.as_view(), name='create-category'),
    path('goal_category/list', CategoryListView.as_view(), name='categories-list'),
    path('goal_category/<int:pk>', CategoryDetailView.as_view(), name='category-details'),

    path('goal/create', GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='goals-list'),
    path('goal/<int:pk>', GoalDetailView.as_view(), name='goal-details'),

    path('goal_comment/create', GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='comments-list'),
    path('goal_comment/<int:pk>', GoalCommentDetailView.as_view(), name='comment-details'),
]
#