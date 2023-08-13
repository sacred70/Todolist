import pytest
from goals.models import Goal


@pytest.mark.django_db
class TestComment:

    @pytest.mark.parametrize('role', (1, 2, 3))
    def test_create_comment_auth(self, get_auth_client, goal, board_participant, role):
        """комментарии у цели может создавать только участник с role 1 и 2 (владелец и редактор)"""
        response = get_auth_client.post('/goals/goal_comment/create', data={
            'text': 'Test comment',
            'goal': goal.pk
        })

        test_goal = Goal.objects.get(user_id=response.wsgi_request.user.pk)

        if board_participant.role in (1, 2):
            assert response.status_code == 201

        else:
            assert response.status_code == 403

    def test_create_comment_not_auth(self, client, goal):
        """комментарии может отставлять только аутентифицированный пользователь"""
        response = client.post('/goals/goal_comment/create', data={
            'text': 'Test comment',
            'goal': goal.pk
        })
        assert response.status_code == 403


