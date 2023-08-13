import pytest
from django.urls import reverse
from goals.models import Board, BoardParticipant


@pytest.mark.django_db
class TestBoardList:
    url = reverse('goals:board-list')
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def test_get_board_list_not_auth(self, client):
        """проверка на получение списка досок не аутентифицированным пользователем"""
        result = client.get(self.url)
        assert result.status_code == 403

    def test_get_board_list(self, get_auth_client, board, user, board_participant):
        """проверка на получение списка досок аутентифицированным пользователем"""
        response = get_auth_client.get(self.url)
        expected_response = {
            'id': board.pk,
            'title': board.title,
            'created': board.created.strftime(self.date_format),
            'updated': board.updated.strftime(self.date_format),
            'is_deleted': False
        }
        assert response.status_code == 200
        assert response.data[0] == expected_response

    def test_get_board_list_alien(self, get_auth_client):
        """проверка на получение списка досок аутентифицированным пользователем,
        но не являющегося участником этих досок"""

        response = get_auth_client.get(self.url)
        assert response.status_code == 200
        assert response.data == []


@pytest.mark.django_db
class TestBoardCreated:
    url_create = reverse('goals:create-board')
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    def test_created_board_not_auth(self, client):
        """доску может создать только аутентифицированный пользователь"""
        response = client.post(self.url_create, data={'title': 'Test_title'})
        assert response.status_code == 403

    def test_created_board_auth(self, get_auth_client):
        """
        аутентифицированный пользователь может создать доску.
        проверяем то что текущий user является создателем доски и его роль -- "Владелец"
        """
        response = get_auth_client.post(self.url_create, data={'title': 'Test_Board_created'})
        current_user = response.wsgi_request.user
        created_board = Board.objects.get(pk=response.data['id'])
        owner = BoardParticipant.objects.get(board_id=created_board.pk)

        expected_response = {
            'id': created_board.pk,
            'title': created_board.title,
            'created': created_board.created.strftime(self.date_format),
            'updated': created_board.updated.strftime(self.date_format),
            'is_deleted': False
        }
        assert response.status_code == 201
        assert response.json() == expected_response
        assert current_user == owner.user
        assert owner.role == 1


