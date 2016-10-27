import six

from django.conf import settings
from django.forms import widgets
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

GOOGLE_MAPS_V3_APIKEY = getattr(settings, 'GOOGLE_MAPS_V3_APIKEY', None)
GOOGLE_MAPS_LIBRARIES = getattr(settings, 'GOOGLE_MAPS_LIBRARIES', None)

GOOGLE_MAPS_LANGUAGE = getattr(settings, 'GOOGLE_MAPS_LANGUAGE', 'en')
GOOGLE_MAPS_REGION = getattr(settings, 'GOOGLE_MAPS_REGION', 'US')

GOOGLE_API_JS = '//maps.google.com/maps/api/js?'

if GOOGLE_MAPS_V3_APIKEY:
    GOOGLE_API_JS = '{0}&key={1}'.format(GOOGLE_API_JS, GOOGLE_MAPS_V3_APIKEY)

if GOOGLE_MAPS_LIBRARIES:
    GOOGLE_API_JS = '{0}&libraries={1}'.format(GOOGLE_API_JS, ','.join(GOOGLE_MAPS_LIBRARIES))

GOOGLE_API_JS = '{0}&language={1}&region={2}'.format(GOOGLE_API_JS, GOOGLE_MAPS_LANGUAGE, GOOGLE_MAPS_REGION)


class LocationWidget(widgets.HiddenInput):
    def __init__(self, **kwargs):
        attrs = kwargs.pop('attrs', None)

        self.address_field = kwargs.pop('address_field', None)
        self.zoom = kwargs.pop('zoom', None) or 7
        self.suffix = kwargs.pop('suffix', '')

        super(LocationWidget, self).__init__(attrs)

    @property
    def is_hidden(self):
        return False

    def render(self, name, value, attrs=None):
        if value is not None:
            try:
                if isinstance(value, six.string_types):
                    lat, lng = value.split(',')
                else:
                    lng = value.x
                    lat = value.y

                value = '%s,%s' % (
                    float(lat),
                    float(lng),
                )
            except ValueError:
                value = ''
        else:
            value = ''

        if '-' not in name:
            prefix = ''
        else:
            prefix = name[:name.rindex('-') + 1]

        address_field = '#id_' + prefix + self.address_field

        attrs = attrs or {}
        attrs['data-location-widget'] = name
        attrs['data-address-field'] = address_field
        attrs['data-zoom'] = self.zoom
        attrs['data-suffix'] = self.suffix
        attrs['data-map'] = '#map_' + name

        text_input = super(LocationWidget, self).render(name, value, attrs)

        return render_to_string('location_field/map_widget.html', {
            'field_name': name,
            'field_input': mark_safe(text_input)
        })

    class Media:
        # Use schemaless URL so it works with both, http and https websites
        js = (
            GOOGLE_API_JS,
            settings.STATIC_URL + 'location_field/js/jquery.livequery.js',
            settings.STATIC_URL + 'location_field/js/form.js',
        )
