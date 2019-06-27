import json
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler
from ..models import Event
from .test_tasks import event_search


DEFAULT_REQUEST_PARAMS = {
    'content_type': 'application/json',
    'accept': 'application/json',
}


class AuthTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_superuser('admin2', 'admin2@example.com', 'secret')

    def tearDown(self) -> None:
        get_user_model().objects.all().delete()

    def test_obtain_jwt(self) -> None:
        response = self.client.post(
            reverse('create-token'),
            json.dumps({'username': 'admin2', 'password': 'secret'}),
            **DEFAULT_REQUEST_PARAMS,
        )
        self.assertIn('token', response.data)

    def test_verify_jwt(self) -> None:
        token = jwt_encode_handler(jwt_payload_handler(self.user))

        response = self.client.post(
            reverse('verify-token'),
            json.dumps({'token': token}),
            **DEFAULT_REQUEST_PARAMS,
            # Authorization=f'Bearer {token}'
        )

        self.assertIn('token', response.data)


class EventsTestCase(APITestCase):
    def setUp(self) -> None:
        Event.objects.bulk_create([Event(**row) for row in event_search('clean_results')],
                                  ignore_conflicts=True)

    def tearDown(self) -> None:
        Event.objects.all().delete()

    def assertDictKeysEqual(self, dict1: dict, list2: list) -> None:
        self.assertListEqual(sorted(dict1.keys()), sorted(list2))

    def test_get_events_list(self) -> None:
        response = self.client.get(reverse('event-list'), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictKeysEqual(response.data['results'][0], list(event_search('clean_results')[0].keys())
                                 + ['local_created_at', 'local_updated_at'])

    def test_retrieve_event(self) -> None:
        response = self.client.get(reverse('event-detail', args=['26066153567']), format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertDictKeysEqual(response.data,
                                 list(list(filter(lambda x: x['id'] == '26066153567', event_search('clean_results')))[0].keys())
                                 + ['local_created_at', 'local_updated_at'])

    def test_update_event(self) -> None:
        superuser = get_user_model().objects.create_superuser('admin2', 'admin2@example.com', 'secret')

        auth_params = {
            'HTTP_AUTHORIZATION': 'Bearer ' + jwt_encode_handler(jwt_payload_handler(superuser))
        }

        response = self.client.patch(
            reverse('event-detail', args=['26066153567']),
            '{"name": "name_changed"}',
            **DEFAULT_REQUEST_PARAMS,
            **auth_params,
        )

        self.assertEqual(response.data['name'], 'name_changed')
        self.assertEqual(Event.objects.get(pk=26066153567).name, 'name_changed')

    def test_update_event_non_admin(self) -> None:
        user = get_user_model().objects.create(
            username='admin2',
            email='admin2@example.com',
            password='secret_hash')

        auth_params = {
            'HTTP_AUTHORIZATION': 'Bearer ' + jwt_encode_handler(
                jwt_payload_handler(user))
        }

        response = self.client.patch(
            reverse('event-detail', args=['26066153567']),
            '{"name": "name_changed"}',
            **DEFAULT_REQUEST_PARAMS,
            **auth_params,
        )
        self.assertEqual(response.status_code, 403)

    # TODO: mock ES response
    def test_search_event_by_name(self) -> None:
        pass

    def test_search_event_by_start_date(self) -> None:
        pass

    def test_search_event_by_organizer_name(self) -> None:
        pass

    def test_search_event_by_cost(self) -> None:
        pass
