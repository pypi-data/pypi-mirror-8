"""
nodeshot.core.nodes unit tests
"""

import os
import simplejson as json

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AnonymousUser
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D
from django.contrib.auth import get_user_model
User = get_user_model()

from nodeshot.core.layers.models import Layer
from nodeshot.core.base.tests import user_fixtures, BaseTestCase

from .models import *


class ModelsTest(TestCase):

    fixtures = [
        'initial_data.json',
        user_fixtures,
        'test_layers.json',
        'test_status.json',
        'test_nodes.json',
        'test_images.json'
    ]

    def test_status_model(self):
        """ test status model internal mechanism works correctly """
        for status in Status.objects.all():
            status.delete()

        testing = Status(name='testing', slug='testing', description='slug')
        testing.save()

        self.assertEqual(testing.order, 0)
        self.assertEqual(testing.is_default, True)

        active = Status(name='active', slug='active', description='active')
        active.save()

        self.assertEqual(active.order, 1)
        self.assertEqual(active.is_default, False)

        pending = Status(name='pending', slug='pending', description='pending')
        pending.save()

        self.assertEqual(pending.order, 2)
        self.assertEqual(pending.is_default, False)

        pending.is_default = True
        pending.save()

        default_statuses = Status.objects.filter(is_default=True)
        self.assertEqual(default_statuses.count(), 1)
        self.assertEqual(default_statuses[0].pk, pending.pk)

        unconfirmed = Status(name='unconfirmed', slug='unconfirmed', description='unconfirmed', is_default=True)
        unconfirmed.save()

        default_statuses = Status.objects.filter(is_default=True)
        self.assertEqual(default_statuses.count(), 1)
        self.assertEqual(default_statuses[0].pk, unconfirmed.pk)

    def test_current_status(self):
        """ test that node._current_status is none for new nodes """
        n = Node()
        self.failUnlessEqual(n._current_status, None, 'new node _current_status private attribute is different than None')
        n = Node.objects.all().order_by('-id')[0]
        self.failUnlessEqual(n._current_status, n.status.id, 'new node _current_status private attribute is different than status')
        n.status = Status.objects.get(pk=2)
        self.failIfEqual(n._current_status, n.status.id, 'new node _current_status private attribute is still equal to status')
        n.save()
        self.failUnlessEqual(n._current_status, n.status.id, 'new node _current_status private attribute is different than status')
        n.status_id = 3
        n.save()
        n = Node.objects.all().order_by('-id')[0]
        self.failUnlessEqual(n._current_status, n.status.id, 'new node _current_status private attribute is different than status')

    def test_node_manager(self):
        """ test manager methods of Node model """
        # published()
        Node.objects.published
        count = Node.objects.published().filter(layer=1).count()
        # no unplished nodes on that layer, so the count should be the same
        self.assertEqual(count, Node.objects.filter(layer=1).count())
        # unpublish the first
        node = Node.objects.published().filter(layer=1)[0]
        node.is_published = False
        node.save()
        # should be -1
        self.assertEqual(count-1, Node.objects.published().filter(layer=1).count())

        # Ensure GeoManager distance is available
        pnt = Node.objects.get(slug='pomezia').geometry
        Node.objects.filter(geometry__distance_lte=(pnt, 7000))

        # access level manager
        user = User.objects.get(pk=1, is_superuser=True)
        # superuser can see all nodes
        self.assertEqual(Node.objects.all().count(), Node.objects.accessible_to(user).count())
        # same but passing only user_id
        user_1 = User.objects.get(pk=1)
        self.assertEqual(Node.objects.all().count(), Node.objects.accessible_to(user_1).count())
        # simulate non authenticated user
        self.assertEqual(8, Node.objects.accessible_to(AnonymousUser()).count())
        # public nodes
        self.assertEqual(8, Node.objects.access_level_up_to('public').count())
        # public and registered
        self.assertEqual(9, Node.objects.access_level_up_to('registered').count())
        # public, registered and community
        self.assertEqual(10, Node.objects.access_level_up_to('community').count())

        ### --- START CHAINING! WOOOO --- ###
        # 9 because we unpublished one
        self.assertEqual(9, Node.objects.published().access_level_up_to('community').count())
        self.assertEqual(9, Node.objects.access_level_up_to('community').published().count())
        # user 1 is admin and can see all the nodes, published() is the same as writing filter(is_published=True)
        count = Node.objects.all().filter(is_published=True).count()
        self.assertEqual(count, Node.objects.published().accessible_to(user_1).count())
        self.assertEqual(count, Node.objects.accessible_to(user_1).published().count())
        # chain with geographic query
        count = Node.objects.all().filter(is_published=True).filter(layer_id=1).count()
        self.assertEqual(count, Node.objects.filter(geometry__distance_lte=(pnt, 70000)).accessible_to(user_1).published().count())
        self.assertEqual(count, Node.objects.accessible_to(user_1).filter(geometry__distance_lte=(pnt, 70000)).published().count())
        self.assertEqual(count, Node.objects.accessible_to(user_1).published().filter(geometry__distance_lte=(pnt, 70000)).count())
        self.assertEqual(count, Node.objects.filter(geometry__distance_lte=(pnt, 70000)).accessible_to(user_1).published().count())

        # slice, first, last, find
        self.assertEqual(Node.objects.last().__class__.__name__, 'Node')
        self.assertEqual(Node.objects.last(), Node.objects.order_by('-id')[0])

        self.assertEqual(Node.objects.first().__class__.__name__, 'Node')
        self.assertEqual(Node.objects.first(), Node.objects.order_by('id')[0])

        self.assertEqual(Node.objects.find(1), Node.objects.get(pk=1))

        self.assertEqual(list(Node.objects.slice('name', 5)), list(Node.objects.order_by('name')[0:5]))
        self.assertEqual(list(Node.objects.slice('-name', 5)), list(Node.objects.order_by('-name')[0:5]))

        # chained
        self.assertEqual(Node.objects.published().first(), Node.objects.filter(is_published=True).order_by('id')[0])
        self.assertEqual(Node.objects.published().last(), Node.objects.filter(is_published=True).order_by('-id')[0])

        self.assertEqual(
            Node.objects.published().access_level_up_to('public').first(),
            Node.objects.filter(is_published=True, access_level__lte=0).order_by('id')[0]
        )
        self.assertEqual(
            Node.objects.published().access_level_up_to('public').last(),
            Node.objects.filter(is_published=True, access_level__lte=0).order_by('-id')[0]
        )

    def test_autogenerate_slug(self):
        n = Node()
        n.name = 'Auto generate this'
        n.layer_id = 1
        n.geometry = 'POINT(12.509303756712 41.881163629853)'
        n.full_clean()

        n.save()

        n = Node.objects.get(pk=n.id)
        self.assertEqual(n.slug, 'auto-generate-this')

    def test_node_point(self):
        node = Node.objects.first()
        self.assertEqual(node.point, node.geometry)

        node = Node()
        with self.assertRaises(ValueError):
            node.point

        node.geometry = GEOSGeometry(json.dumps({"type":"Polygon","coordinates":[[[12.501493164066,41.990441051094],[12.583890625003,41.957770034531],[12.618222900394,41.912820024702],[12.607923217778,41.877552973685],[12.582088180546,41.82423212474],[12.574148841861,41.813357913568],[12.551532455447,41.799730560554],[12.525053688052,41.795155470656],[12.510505386356,41.793715689492],[12.43308610535,41.803249638226],[12.388883300784,41.813613798573],[12.371030517581,41.870906276755],[12.382016845706,41.898511105474],[12.386136718753,41.912820024702],[12.38064355469,41.926104006681],[12.38064355469,41.955727539561],[12.413602539065,41.974107637675],[12.445188232426,41.983295698272],[12.45617456055,41.981254021593],[12.476773925785,41.985337309484],[12.490506835941,41.985337309484],[12.506986328129,41.990441051094],[12.501493164066,41.990441051094]]]}))
        node.point  # must not raise GEOSException

    def test_image_manager(self):
        """ test manager methods of Image model """
        # admin can see all the images
        user_1 = User.objects.get(pk=1)
        self.assertEqual(Image.objects.all().count(), Image.objects.accessible_to(user_1).count())

    def test_image_auto_order(self):
        """ test image automatic ordering works correctly """
        # node #3 has already 2 images, therefore the new image auto order should be set to 2
        image = Image(node_id=3, file='test3.jpg')
        image.full_clean()
        image.save()
        self.assertEqual(image.order, 2)

        # node #2 does not have any image, therefore the new image auto order should be set to 0
        image = Image(node_id=2, file='test2.jpg')
        image.full_clean()
        image.save()
        self.assertEqual(image.order, 0)

    def test_geometry_collection_with_single_item(self):
        node = Node.objects.get(pk=1)
        node.geometry = GEOSGeometry("GEOMETRYCOLLECTION(POINT(12.509303756712 41.881163629853))")
        node.save()
        # fetch again cos geometry value is modified while saving
        node = Node.objects.get(pk=1)

        point = GEOSGeometry("POINT(12.509303756712 41.881163629853)")
        self.assertEqual(node.geometry, point)


### ------ API tests ------ ###


class APITest(BaseTestCase):

    fixtures = [
        'initial_data.json',
        user_fixtures,
        'test_layers.json',
        'test_status.json',
        'test_nodes.json',
        'test_images.json'
    ]

    def test_node_list(self):
        """ test node list """
        url = reverse('api_node_list')

        # GET: 200
        response = self.client.get(url, { "limit": 0 })
        public_node_count = Node.objects.published().access_level_up_to('public').count()
        self.assertEqual(public_node_count, len(response.data['results']))

        node = {
            "layer": "rome",
            "name": "test distance",
            "address": "via dei test",
            "description": "",
            "geometry": json.loads(GEOSGeometry("POINT (12.99 41.8720419277)").json),
        }

        # POST: 403 - unauthenticated
        response = self.client.post(url, json.dumps(node), content_type='application/json')
        self.assertEqual(403, response.status_code)

        # POST: 201
        self.client.login(username='registered', password='tester')
        response = self.client.post(url, json.dumps(node), content_type='application/json')
        self.assertEqual(201, response.status_code)

        self.assertEqual(response.data['user'], 'registered')

        node = Node.objects.get(slug='test-distance')
        self.assertEqual(node.name, "test distance")

    def test_node_list_search(self):
        url = reverse('api_node_list')

        # GET: 200
        response = self.client.get(url, { "search": "Fusolab" })
        self.assertEqual(response.data['count'], 1)

    def test_delete_node(self):
        node = Node.objects.first()
        node.delete()

    def test_node_geojson_list(self):
        """ test node geojson list """
        url = reverse('api_node_gejson_list')

        # GET: 200
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_node_details(self):
        """ test node details """
        url = reverse('api_node_details', args=['fusolab'])

        # GET: 200
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        node = response.data
        # images_url in node['images']
        self.assertTrue(isinstance(node['relationships']['images'], list))
        self.assertTrue(isinstance(node['relationships']['images'][0], dict))

        # PUT: 403 - must be logged in
        response = self.client.put(url)
        self.assertEqual(403, response.status_code)

        self.client.login(username='pisano', password='tester')
        # PUT: 403 - only owner can edit
        data = {
            "name": "Fusolab Rome test",
            "slug": "fusolab",
            "user": "romano",
            "elev": 80.0,
            "address": "",
            "description": "Fusolab test 2",
            "access_level": "public",
            "layer": "rome",
            "geometry": json.loads(GEOSGeometry("POINT (12.582239191899999 41.872041927700003)").json)
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(403, response.status_code)

        self.client.logout()
        self.client.login(username='romano', password='tester')
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(200, response.status_code)
        node = Node.objects.get(slug='fusolab')
        self.assertEqual(node.name, 'Fusolab Rome test')
        self.assertEqual(node.description, 'Fusolab test 2')

        # PATCH
        response = self.client.patch(url, { 'name': 'Patched Fusolab Name' })
        self.assertEqual(200, response.status_code)
        node = Node.objects.get(slug='fusolab')
        self.assertEqual(node.name, 'Patched Fusolab Name')
        self.client.logout()

        # CAN'T GET restricted if not authenticated
        fusolab = Node.objects.get(slug='fusolab')
        fusolab.access_level = 2
        fusolab.save()
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

        # Admin can get it
        self.client.login(username='admin', password='tester')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # unpublished will return 404
        fusolab.is_published = False
        fusolab.save()
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

        fusolab.is_published = True
        fusolab.save()

        # DELETE 204
        response = self.client.delete(url)
        self.assertEqual(204, response.status_code)
        with self.assertRaises(Node.DoesNotExist):
            Node.objects.get(slug='fusolab')

    def test_node_images_relationship(self):
        url = reverse('api_node_details', args=['fusolab'])

        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        images = response.data['relationships']['images']
        public_image_count = Image.objects.access_level_up_to('public').filter(node__slug='fusolab').count()
        self.assertEqual(public_image_count, len(images))
        # admin can get more images
        self.client.login(username='admin', password='tester')
        response = self.client.get(url)
        images = response.data['relationships']['images']
        node_image_count = Image.objects.accessible_to(User.objects.get(pk=1)).filter(node__slug='fusolab').count()
        self.assertEqual(node_image_count, len(images))

    def test_node_images(self):
        """ test node images """
        url = reverse('api_node_images', args=['fusolab'])

        # GET: 200
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        images = json.loads(response.content)
        public_image_count = Image.objects.access_level_up_to('public').filter(node__slug='fusolab').count()
        self.assertEqual(public_image_count, len(images))
        # admin can get more images
        self.client.login(username='admin', password='tester')
        response = self.client.get(url)
        images = json.loads(response.content)
        node_image_count = Image.objects.accessible_to(User.objects.get(pk=1)).filter(node__slug='fusolab').count()
        self.assertEqual(node_image_count, len(images))

        # GET: 404
        url = reverse('api_node_images', args=['idontexist'])
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

        # POST
        # todo
        login = self.client.login(username='admin', password='tester')
        good_post_data = { "description": "new image", "order": "" }
        bad_post_data = { "node": 100, "image": "jpeg99" ,"description" : "new image", "order": "" }
        url = reverse('api_node_images', args=['fusolab'])
        wrong_url = reverse('api_node_images', args=['idontexist'])

        # wrong slug -- 404
        response = self.client.post(wrong_url, good_post_data)
        self.assertEqual(response.status_code, 404)

        # correct POST data and correct slug -- 201
        with open("%s/templates/image_unit_test.gif" % os.path.dirname(os.path.realpath(__file__)), 'rb') as image_file:
            good_post_data['file'] = image_file
            response = self.client.post(url, good_post_data)
            self.assertEqual(response.status_code, 201)
            # ensure image name is in DB
            image = Image.objects.all().order_by('-id')[0]
            self.assertIn('image_unit_test', image.file.name)
            self.assertIn('.gif', image.file.name)
            # remove file
            os.remove(image.file.file.name)

        # POST 201 - ensure additional post data "user" and "node" are ignored
        with open("%s/templates/image_unit_test.gif" % os.path.dirname(os.path.realpath(__file__)), 'rb') as image_file:
            bad_post_data['file'] = image_file
            response = self.client.post(url, bad_post_data)
            self.assertEqual(response.status_code, 201)
            image_dict = json.loads(response.content)
            self.assertEqual(image_dict['node'], 1)
            self.assertEqual(image_dict['description'], "new image")
            # ensure image name is in DB
            image = Image.objects.all().order_by('-id')[0]
            self.assertIn('image_unit_test', image.file.name)
            # remove file
            os.remove(image.file.file.name)

        self.client.logout()
        self.client.login(username='pisano', password='tester')

        with open("%s/templates/image_unit_test.gif" % os.path.dirname(os.path.realpath(__file__)), 'rb') as image_file:
            good_post_data['file'] = image_file
            response = self.client.post(url, good_post_data)
            self.assertEqual(response.status_code, 403)

    def test_node_image_list_permissions(self):
        # GET protected image should return 404
        url = reverse('api_node_images', args=['hidden-rome'])
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

        self.client.login(username='admin', password='tester')
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_node_geometry_distance_and_area(self):
        """ test minimum distance check between nodes """
        self.client.login(username='admin', password='tester')

        url = reverse('api_node_list')

        json_data = {
            "layer": "rome",
            "name": "test_distance",
            "slug": "test_distance",
            "address": "via dei test",
            "description": "",
            "geometry": json.loads(GEOSGeometry("POINT (12.5822391919000012 41.8720419276999820)").json),
        }
        layer = Layer.objects.get(pk=1)
        layer.minimum_distance = 100
        layer.save()

        # Node coordinates don't respect minimum distance. Insert should fail because coords are near to already existing PoI ( fusolab )
        response = self.client.post(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(400, response.status_code)

        # Node coordinates respect minimum distance. Insert should succed
        json_data['geometry'] = json.loads(GEOSGeometry("POINT (12.7822391919 41.8720419277)").json);
        response = self.client.post(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(201, response.status_code)

        # Disable minimum distance control in layer and update node inserting coords too near. Insert should succed
        layer.minimum_distance = 0
        layer.save()
        json_data['geometry'] = json.loads(GEOSGeometry("POINT (12.5822391917 41.872042278)").json)
        n = Node.objects.get(slug='test_distance')
        node_slug = n.slug
        url = reverse('api_node_details', args=[node_slug])
        response = self.client.put(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(200, response.status_code)

        # re-enable minimum distance and update again with coords too near. Insert should fail
        layer.minimum_distance = 100
        layer.save()
        url = reverse('api_node_details', args=[node_slug])
        response = self.client.put(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(400, response.status_code)

        # Defining an area for the layer and testing if node is inside the area
        layer.area = GEOSGeometry('POLYGON ((12.19 41.92, 12.58 42.17, 12.82 41.86, 12.43 41.64, 12.43 41.65, 12.19 41.92))')
        layer.save()

        # Node update should fail because coords are outside layer area
        json_data['geometry'] = json.loads(GEOSGeometry("POINT (50 50)").json)
        url = reverse('api_node_details', args=[node_slug])
        response = self.client.put(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(400, response.status_code)

        # Node update should succeed because coords are inside layer area and respect minimum distance
        json_data['geometry'] = json.loads(GEOSGeometry("POINT (12.7822391919 41.8720419277)").json)
        url = reverse('api_node_details', args=[node_slug])
        response = self.client.put(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(200, response.status_code)

        # Node update should succeed because layer area is disabled
        layer.area = None
        layer.save()
        json_data['geometry'] = json.loads(GEOSGeometry("POINT (50 50)").json)
        url = reverse('api_node_details', args=[node_slug])
        response = self.client.put(url, json.dumps(json_data), content_type='application/json')
        self.assertEqual(200, response.status_code)

        # re-enable minimum distance
        layer.minimum_distance = 100
        layer.save()

        # delete new nodes just added before
        n.delete()
