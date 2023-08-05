import os
from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.interfaces import IBrowserLayerAwareExtender
from interfaces import IFormSaveData2ContentEntry
from Acquisition import aq_inner
from Products.Archetypes.Field import TextField, StringField, DateTimeField, \
    FixedPointField, LinesField, IntegerField, ObjectField, BooleanField
from Products.Archetypes.Widget import ImageWidget
from Products.Archetypes import atapi
from Products.PloneFormGen.content.fieldsBase import LinesVocabularyField, \
    StringVocabularyField
from Products.PloneFormGen.content.fields import HtmlTextField, \
    PlainTextField, FGFileField

from uwosh.pfg.d2c import pfgMessageFactory as _

from archetypes.schemaextender.field import ExtensionField
from plone.memoize.instance import memoize
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import DisplayList
from uwosh.pfg.d2c.interfaces import ILayer
from uwosh.pfg.d2c.widgets import DonationWidget

try:
    from plone.app.blob.field import ImageField, BlobField as FileField
except ImportError:
    from Products.Archetypes.Field import ImageField, FileField

try:
    import plone.app.imaging  # noqa
    IMAGE_SIZES = None
except:
    IMAGE_SIZES = {'large': (768, 768),
                   'preview': (400, 400),
                   'mini': (200, 200),
                   'thumb': (128, 128),
                   'tile': (64, 64),
                   'icon': (32, 32),
                   'listing': (16, 16)}


# extra field attributes to copy over.
extra_fields = [
    'widget', 'questionSet', 'answerSet', 'validators', 'fgDonationLevels',
    'fgCost', 'fgRecurForever', 'fgAllowRecurringPayments', 'default_output_type'  # noqa
]

# instance values to copy over
instance_values_to_field = ['minval', 'maxval', 'maxlength']


class XPlainTextField(ExtensionField, PlainTextField):
    pass


class XTextField(ExtensionField, TextField):
    pass


class XStringField(ExtensionField, StringField):
    pass


class XDateTimeField(ExtensionField, DateTimeField):
    pass


class XFixedPointField(ExtensionField, FixedPointField):
    pass


class XFileField(ExtensionField, FileField):
    pass


class XLinesField(ExtensionField, LinesField):
    pass


class XIntegerField(ExtensionField, IntegerField):
    pass


class XBooleanField(ExtensionField, BooleanField):
    pass


class XLinesVocabularyField(ExtensionField, LinesVocabularyField):
    pass


class XImageField(ExtensionField, ImageField):
    _properties = ImageField._properties.copy()
    _properties.update({'sizes': IMAGE_SIZES})

    def set(self, instance, value, **kwargs):
        if value == "DELETE_FILE":
            value = "DELETE_IMAGE"
        try:
            return super(XImageField, self).set(instance, value, **kwargs)
        except:
            pass


class XStringVocabularyField(ExtensionField, StringVocabularyField):
    security = ClassSecurityInfo()

    security.declarePublic('Vocabulary')
    def Vocabulary(self, content_instance=None):  # noqa
        """
        Returns a DisplayList.
        """
        # if there's a TALES override, return it as a DisplayList,
        # otherwise, build the DisplayList from fgVocabulary

        fieldContainer = content_instance.findFieldObjectByName(self.__name__)

        try:
            vl = fieldContainer.getFgTVocabulary()
        except AttributeError:
            vl = None
        if vl is not None:
            return DisplayList(data=vl)

        res = DisplayList()
        for line in fieldContainer.fgVocabulary:
            lsplit = line.split('|')
            if len(lsplit) == 2:
                key, val = lsplit
            else:
                key, val = (lsplit[0], lsplit[0])
            res.add(key, val)
        return res


class XHtmlTextField(ExtensionField, HtmlTextField):
    pass


extension_fields = [
    XTextField, XStringField, XDateTimeField, XFixedPointField, XFileField,
    XLinesField, XIntegerField, XLinesVocabularyField, XStringVocabularyField,
    XHtmlTextField, XPlainTextField
]

# XXX
# begin backwards compatible imports
# XXX
try:
    from Products.PloneFormGen.content.fields import \
        NRBooleanField as BooleanField

    class XNRBooleanField(ExtensionField, BooleanField):
        pass

    extension_fields.append(XNRBooleanField)
except:
    pass

try:
    from Products.PloneFormGen.content.likertField import LikertField

    def get_likert(self, instance, **kwargs):
        value = ObjectField.get(self, instance, **kwargs)
        if not value:
            return {}
        else:
            return value

    def set_likert(self, instance, value, **kwargs):
        if type(value) in (str, unicode):
            value = [v.strip() for v in value.split(',')]
        elif type(value) in (tuple, list, set):
            newval = {}
            for i in range(0, len(value)):
                newval[str(i + 1)] = value[i]
            value = newval

        ObjectField.set(self, instance, value, **kwargs)

    class XLikertField(ExtensionField, LikertField):
        """
        override default methods which have bugs...
        """

        get = get_likert
        set = set_likert

    # patch these methods to actually work.
    LikertField.get = get_likert
    LikertField.set = set_likert
    extension_fields.append(XLikertField)
except:
    pass

# XXX
# Conditional fields
# XXXX
try:
    from Products.DataGridField import DataGridField

    class XDataGridField(ExtensionField, DataGridField):
        pass
    extension_fields.append(XDataGridField)
    extra_fields.append('columns')
except:
    pass

FIELDS = {}

for klass in extension_fields:
    FIELDS[klass.__name__] = klass

INVALID_TYPES = (
    'FGFieldsetStart',
    'FGFieldsetEnd')


CUSTOM_WIDGETS_FOR_MACROS = {
    'donationfield_widget': DonationWidget
}

CUSTOM_WIDGETS = {
    XImageField: ImageWidget
}


class ContentEntryExtender(object):
    """
    We use this because it's a nice way to dynamically add fields
    to content.
    """
    adapts(IFormSaveData2ContentEntry)
    implements(ISchemaExtender)

    def __init__(self, context):
        self.context = context

    @memoize
    def getFields(self):
        context = aq_inner(self.context)
        form = context.getForm()
        if not form:
            return []
        obj_fields = form._getFieldObjects()
        fields = []

        for objfield in obj_fields:
            field = objfield.fgField
            if objfield.aq_base.__class__.__name__ in INVALID_TYPES:
                continue
            klassname = 'X' + field.__class__.__name__
            if klassname in FIELDS:
                macro = getattr(getattr(field, 'widget', None), 'macro', None)
                if 'XFileField' == klassname:
                    valid_image = False
                    try:
                        filename = getattr(context, field.getName()).filename
                        ext = os.path.splitext(filename)[-1].strip('.').lower()
                        if ext in ('png', 'gif', 'jpg', 'jpeg'):
                            valid_image = True
                    except:
                        pass
                    isImField = objfield.getField('isImage')
                    if valid_image and isImField and isImField.get(objfield):
                        klass = XImageField
                    else:
                        klass = FIELDS[klassname]
                else:
                    klass = FIELDS[klassname]
                newfield = klass(field.__name__, **field._properties)
                for key in extra_fields:
                    if hasattr(field, key):
                        setattr(newfield, key, getattr(field, key))

                for val in instance_values_to_field:
                    if hasattr(field, val):
                        setattr(newfield, val, getattr(field, val))

                if hasattr(objfield, 'getRequired'):
                    newfield.required = objfield.getRequired()

                if macro in CUSTOM_WIDGETS_FOR_MACROS:
                    widget = CUSTOM_WIDGETS_FOR_MACROS[macro](
                        label=field.widget.label,
                        description=field.widget.description,
                        macro=macro)
                    newfield.widget = widget
                elif klass in CUSTOM_WIDGETS:
                    widget = CUSTOM_WIDGETS[klass](
                        label=field.widget.label,
                        description=field.widget.description)
                    newfield.widget = widget
                fields.append(newfield)

        return fields


class PFGFileFieldExtender(object):

    adapts(FGFileField)
    implements(IBrowserLayerAwareExtender)

    layer = ILayer

    fields = [
        XBooleanField(
            'isImage',
            widget=atapi.BooleanWidget(
                label=_(u"Is Image"),
                description=_(u"Only to be used for d2c generated types"),
            )
        )
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
