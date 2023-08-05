from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, pagination
from rest_framework.reverse import reverse
from rest_framework_gis import serializers as geoserializers

from nodeshot.core.base.serializers import GeoJSONPaginationSerializer
from .settings import settings
from .base import ExtensibleNodeSerializer
from .models import *


__all__ = [
    'NodeListSerializer',
    'NodeCreatorSerializer',
    'NodeDetailSerializer',
    'NodeGeoSerializer',
    'PaginatedNodeListSerializer',
    'PaginatedGeojsonNodeListSerializer',
    'ImageListSerializer',
    'ImageAddSerializer',
    'ImageEditSerializer',
    'ImageRelationSerializer',
    'StatusListSerializer'
]


try:
    ADDITIONAL_NODE_FIELDS = Node._hstore_virtual_fields.keys()
except AttributeError:
    ADDITIONAL_NODE_FIELDS = []


class NodeDetailSerializer(ExtensibleNodeSerializer):
    """ node detail """
    layer = serializers.SlugRelatedField(slug_field='slug')

    class Meta:
        model = Node
        fields = [
            'name', 'slug', 'status', 'user',
            'access_level', 'layer', 'layer_name',
            'geometry', 'elev', 'address',
            'description',
        ] + ADDITIONAL_NODE_FIELDS + [
            'added', 'updated', 'relationships'
        ]

        read_only_fields = ('added', 'updated')
        geo_field = 'geometry'


class NodeListSerializer(NodeDetailSerializer):
    """ node list """
    details = serializers.HyperlinkedIdentityField(view_name='api_node_details', lookup_field='slug')

    class Meta:
        model = Node
        fields = [
            'name', 'slug', 'layer', 'layer_name', 'user', 'status',
            'geometry', 'elev', 'address', 'description',
            'updated', 'added', 'details'
        ]

        read_only_fields = ['added', 'updated']
        geo_field = 'geometry'
        id_field = 'slug'


class PaginatedNodeListSerializer(pagination.PaginationSerializer):
    class Meta:
        object_serializer_class = NodeListSerializer


class PaginatedGeojsonNodeListSerializer(GeoJSONPaginationSerializer):
    class Meta:
        object_serializer_class = NodeListSerializer


class NodeCreatorSerializer(NodeListSerializer):
    layer = serializers.WritableField(source='layer')


class NodeGeoSerializer(geoserializers.GeoFeatureModelSerializer, NodeListSerializer):
    pass


class ImageListSerializer(serializers.ModelSerializer):
    """ Serializer used to show list """
    file_url = serializers.SerializerMethodField('get_image_file')
    details = serializers.SerializerMethodField('get_uri')

    def get_image_file(self, obj):
        """ returns url to image file or empty string otherwise """
        url = ''

        if obj.file != '':
            url = '%s%s' % (settings.MEDIA_URL, obj.file)

        return url

    def get_uri(self, obj):
        """ returns uri of API image resource """
        args = {
            'slug': obj.node.slug,
            'pk': obj.pk
        }

        return reverse('api_node_image_detail', kwargs=args, request=self.context.get('request', None))

    class Meta:
        model = Image
        fields = (
            'id', 'file', 'file_url', 'description', 'order',
            'access_level', 'added', 'updated', 'details'
        )
        read_only_fields = ('added', 'updated')


class ImageAddSerializer(ImageListSerializer):
    """ Serializer for image creation """
    class Meta:
        model = Image
        fields = (
            'node', 'id', 'file', 'file_url', 'description', 'order',
            'access_level', 'added', 'updated', 'details'
        )


class ImageEditSerializer(ImageListSerializer):
    """ Serializer for image edit """
    class Meta:
        model = Image
        fields = ('id', 'file_url', 'description', 'order', 'access_level', 'added', 'updated', 'details')
        read_only_fields = ('file', 'added', 'updated')


class ImageRelationSerializer(ImageListSerializer):
    """ Serializer to reference images """
    class Meta:
        model = Image
        fields = ('id', 'file', 'file_url', 'description', 'added', 'updated')


ExtensibleNodeSerializer.add_relationship(
    'images',
    serializer=ImageRelationSerializer,
    many=True,
    queryset='obj.image_set.accessible_to(request.user).all()'
)


# --------- Status --------- #


class StatusListSerializer(serializers.ModelSerializer):
    """ status list """
    nodes_count = serializers.Field(source='nodes_count')

    class Meta:
        model = Status
        fields = [
            'name',
            'slug',
            'description',
            'is_default',
            'stroke_width',
            'fill_color',
            'stroke_color',
            'text_color',
            'nodes_count'
        ]
