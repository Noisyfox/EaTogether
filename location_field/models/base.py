class BaseLocationField(object):
    def __init__(self, **kwargs):
        self._address_field = kwargs.pop('address_field', [])
        self._zoom = kwargs.pop('zoom', 2)
        self._default = kwargs.pop('default', None)

        self.default = self._default

    def formfield(self, **kwargs):
        return super(BaseLocationField, self).formfield(
            form_class=self.formfield_class,
            address_field=self._address_field,
            zoom=self._zoom,
            default=self._default,
            **kwargs)
