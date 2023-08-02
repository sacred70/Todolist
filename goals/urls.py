from django.urls import path

from goals.views.comments import GoalCommentCreateView, GoalCommentListView, GoalCommentDetailView
from goals.views.goals import GoalListView, GoalCreateView, GoalDetailView
from goals.views.categories import CategoryCreateView, CategoryListView, CategoryDetailView
from goals.views.boards import BoardListView, BoardCreateView


urlpatterns = [
    path('board/create', BoardCreateView.as_view(), name='create-board'),
    path('board/list', BoardListView.as_view(), name='board-list'),

    path('goal_category/create', CategoryCreateView.as_view()),
    path('goal_category/list', CategoryListView.as_view()),
    path('goal_category/<int:pk>', CategoryDetailView.as_view()),

    path('goal/create', GoalCreateView.as_view(), name='create-goal'),
    path('goal/list', GoalListView.as_view(), name='goals-list'),
    path('goal/<int:pk>', GoalDetailView.as_view(), name='goal-details'),

    path('goal_comment/create', GoalCommentCreateView.as_view(), name='create-comment'),
    path('goal_comment/list', GoalCommentListView.as_view(), name='comments-list'),
    path('goal_comment/<int:pk>', GoalCommentDetailView.as_view(), name='comment-details'),


]
#