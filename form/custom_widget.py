
class PlaceholderInput(forms.widgets.Input):
    template_name = 'about/placeholder.html'
    input_type = 'text'
    def get_context(self, name, value, attrs):
        context = super(PlaceholderInput, self).get_context(name, value, attrs)
        context['widget']['attrs']['maxlength'] = 50
        context['widget']['attrs']['placeholder'] = name.title()
        return context
    
# about/placeholder.html
"""
<input type="{{ widget.type }}" name="{{ widget.name }}"{% if widget.value != None %}
value="{{ widget.value }}"{% endif %}{% include "django/forms/widgets/attrs.html" %} />

# django/forms/widgets/attrs.html
{% for name, value in widget.attrs.items %}{% if value is not False %} {{ name }}{% if value
is not True %}="{{ value }}"{% endif %}{% endif %}{% endfor %}
"""
