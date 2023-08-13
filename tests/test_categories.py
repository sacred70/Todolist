import pytest
from django.urls import reverse
from goals.models import GoalCategory


@pytest.mark.django_db
class TestGoalCategory:
    url = reverse('goals:create-category')
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def test_create_category_not_auth_auth(self, client, board):
        """категории не могут создавать не аутентифицированные пользователи"""
        response = client.post(self.url, data={'title': 'Test_title', 'board': board.title})
        assert response.status_code == 403

    def test_create_category_auth(self, get_auth_client, board):
        """категории могут создавать только аутентифицированные пользователи и у которых role = 1 или 2"""
        response = get_auth_client.post(self.url, data={'title': 'Test_title', 'board': board.pk})
        assert response.status_code == 403

    @pytest.mark.parametrize('role', [1, 2, 3])
    def test_create_category(self, get_auth_client, board, board_participant, goal_category, role):
        """создание категории"""

        board_participant.role = role
        board_participant.save()
        response = get_auth_client.post(self.url, data={'title': goal_category.title, 'board': board.pk})

        if role in (1, 2):
            goal_category_obj = GoalCategory.objects.get(pk=response.data['id'])
            expected_response = {
                'id': goal_category_obj.pk,
                'title': goal_category.title,
                'board': board.pk,
                'is_deleted': False,
                'created': goal_category_obj.created.strftime(self.date_format),
                'updated': goal_category_obj.updated.strftime(self.date_format),
            }
            assert response.status_code == 201
            assert response.json() == expected_response
        else:
            assert response.status_code == 403

    @pytest.mark.django_db
    @pytest.mark.parametrize('role', [1, 2, 3])
    def test_delete_goal_category(self, get_auth_client, board_participant, goal_category, role):
        """категорию может удалить только владелец у которого role = 1 или редактор с role = 2"""
        response = get_auth_client.delete(f'/goals/goal_category/{goal_category.pk}')
        deleted_category = GoalCategory.objects.get(pk=goal_category.pk)

        if board_participant.role in (1, 2):
            assert response.status_code == 204
            assert deleted_category.is_deleted
        else:
            assert response.status_code == 403
