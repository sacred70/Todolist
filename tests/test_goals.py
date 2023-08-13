import pytest

from django.urls import reverse
from rest_framework import status

from goals.models import BoardParticipant
from tests.factories import CreateGoalRequest


@pytest.mark.django_db()
class TestCreateGoalView:
    url = reverse('goals:create-goal')

    def test_auth_required(self, client):
        response = client.post(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_board_if_not_participant(self, get_auth_client, goal_category, faker):
        '''нельзя создать если ты не владелец доски'''
        data = CreateGoalRequest.build(category=goal_category.id)
        response = get_auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_board_if_reader(self, get_auth_client, board_participant, goal_category):
        '''нельзя создать если ты чтец'''
        board_participant.role = BoardParticipant.Role.reader
        board_participant.save(update_fields=['role'])
        data = CreateGoalRequest.build(category=goal_category.id)
        response = get_auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize('role',
                             [BoardParticipant.Role.owner, BoardParticipant.Role.writer],
                             ids=['owner', 'writer'])
    def test_have_to_create_to_with_roles_owner_or_writer(self, get_auth_client,
                                                          board_participant,
                                                          goal_category,
                                                          faker, role):
        '''создать цель если ты владелец или писатель'''
        board_participant.role = role
        board_participant.save(update_fields=['role'])
        data = CreateGoalRequest.build(category=goal_category.id)
        response = get_auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_goal_on_deleted_category(self, get_auth_client, goal_category):
        """создание цели на удаленую категорию"""
        goal_category.is_deleted = True
        goal_category.save(update_fields=['is_deleted'])
        data = CreateGoalRequest.build(category=goal_category.id)
        response = get_auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'category': ['Category not exists']}

    def test_create_goal_on_existing_category(self, get_auth_client, board_participant):
        """создание цели в несуществующей категории"""
        data = CreateGoalRequest.build(category=1)
        response = get_auth_client.post(self.url, data=data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {'category': ['Invalid pk "1" - object does not exist.']}