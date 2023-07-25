from rest_framework import generics, permissions, filters
from django.db import transaction

from goals.permissions import BoardPermission
from goals.serializers import BoardSerializer, BoardWithParticipantSerializer
from goals.models import BoardParticipant, Board, Goal


class BoardCreateView(generics.CreateAPIView):
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        with transaction.atomic():
            board = serializer.save()
            BoardParticipant.objects.create(user=self.request.user, board=board)


class BoardListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BoardSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ['title']

    def get_queryset(self):
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [BoardPermission]
    serializer_class = BoardWithParticipantSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants__user').exclud(is_deleted=True)

    def perform_destroy(self, instance:Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(status=Goal.Status.archived)
