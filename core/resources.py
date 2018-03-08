from import_export.resources import ModelResource
from import_export.widgets import ForeignKeyWidget
from import_export import fields, resources
from django.utils.translation import gettext_lazy as _

from core.models import *
import logging
logger = logging.getLogger(__name__)


class PostResource(ModelResource):

    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=ForeignKeyWidget(Category, 'name'))

    class Meta:
        model = Post
        fields = ('name', 'desc', 'category', 'image')
        # check for unique fields because we have  no ids in excel file
        import_id_fields = ['name', 'category',]
        exclude = ('id',)
        export_order = fields
        skip_unchanged = True


    def before_import_row(self, row, **kwargs):
        """
        Override to add additional logic. Does nothing by default.
        """
        #row['district'] = District.objects.filter(name=row['district'])[0].pk
        pass






