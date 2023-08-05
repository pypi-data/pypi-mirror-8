

import json
from example.tests import TestBase
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings


class ModelViewSetTests(TestBase):
    """
    Test usage with ModelViewSets

    [<RegexURLPattern user-list ^user-viewsets/$>, <RegexURLPattern user-detail ^user-viewsets/(?P<pk>[^/]+)/$>]
    """
    list_url = reverse_lazy('user-list')

    def setUp(self):
        super(ModelViewSetTests, self).setUp()
        self.detail_url = reverse('user-detail', kwargs={'pk': self.miles.pk})

    def test_key_in_list_result(self):
        """
        Ensure the result has a "user" key since that is the name of the model
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        user = get_user_model().objects.all()[0]
        expected = {"user": [{
            'id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }]}

        json_content = json.loads(response.content)
        meta = json_content.get("meta")

        self.assertEquals(expected.get('user'), json_content.get('user'))
        self.assertEquals(meta.get('count', 0),
            get_user_model().objects.count())
        self.assertEquals(meta.get("next"), 2)
        self.assertEqual('http://testserver/user-viewset/?page=2',
            meta.get("next_link"))
        self.assertEqual(meta.get("page"), 1)

    def test_page_two_in_list_result(self):
        """
        Ensure that the second page is reachable and is the correct data.
        """
        response = self.client.get(self.list_url, {'page': 2})
        self.assertEqual(response.status_code, 200)

        user = get_user_model().objects.all()[1]
        expected = {"user": [{
            'id': user.pk,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }]}

        json_content = json.loads(response.content)
        meta = json_content.get("meta")

        self.assertEquals(expected.get('user'), json_content.get('user'))
        self.assertEquals(meta.get('count', 0),
            get_user_model().objects.count())
        self.assertIsNone(meta.get("next"))
        self.assertIsNone(meta.get("next_link"))
        self.assertEqual(meta.get("previous"), 1)
        self.assertEqual('http://testserver/user-viewset/?page=1',
            meta.get("previous_link"))
        self.assertEqual(meta.get("page"), 2)

    def test_page_range_in_list_result(self):
        """
        Ensure that the range of a page can be changed from the client.
        """
        response = self.client.get(self.list_url, {'page_size': 2})
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        expected = {"user": [
        {
            'id': users[0].pk,
            'first_name': users[0].first_name,
            'last_name': users[0].last_name,
            'email': users[0].email
        },
        {
            'id': users[1].pk,
            'first_name': users[1].first_name,
            'last_name': users[1].last_name,
            'email': users[1].email
        }]}

        json_content = json.loads(response.content)
        meta = json_content.get("meta")
        self.assertEquals(expected.get('user'), json_content.get('user'))
        self.assertEquals(meta.get('count', 0),
            get_user_model().objects.count())


    def test_key_in_detail_result(self):
        """
        Ensure the result has a "user" key.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)

        result = json.loads(response.content)
        expected = {
            'user': {
                'id': self.miles.pk,
                'first_name': self.miles.first_name,
                'last_name': self.miles.last_name,
                'email': self.miles.email
            }
        }

        self.assertEqual(result, expected)

    def test_key_in_post(self):
        """
        Ensure a key is in the post.
        """
        self.client.login(username='miles', password='pw')
        data = {
            'user': {
                'id': self.miles.pk,
                'first_name': self.miles.first_name,
                'last_name': self.miles.last_name,
                'email': 'miles@trumpet.org'
            }
        }
        response = self.client.put(self.detail_url, data=data, format='json')

        result = json.loads(response.content)

        self.assertIn('user', result.keys())
        self.assertEqual(result['user']['email'], 'miles@trumpet.org')

        # is it updated?
        self.assertEqual(
            get_user_model().objects.get(pk=self.miles.pk).email,
            'miles@trumpet.org')

