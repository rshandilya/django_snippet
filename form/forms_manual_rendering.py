
{{ form.non_field_errors }}
<div class="fieldWrapper">
    {{ form.subject.errors }}
    <label for="{{ form.subject.id_for_label }}">Email subject:</label>
    {{ form.subject }}
</div>
<div class="fieldWrapper">
    {{ form.message.errors }}
    <label for="{{ form.message.id_for_label }}">Your message:</label>
    {{ form.message }}
</div>
<div class="fieldWrapper">
    {{ form.sender.errors }}
    <label for="{{ form.sender.id_for_label }}">Your email address:</label>
    {{ form.sender }}
</div>
<div class="fieldWrapper">
    {{ form.cc_myself.errors }}
    <label for="{{ form.cc_myself.id_for_label }}">CC yourself?</label>
    {{ form.cc_myself }}
</div>

<!--------------------------------------------------------------------->

<div class="fieldWrapper">
    {{ form.subject.errors }}
    {{ form.subject.label_tag }}
    {{ form.subject }}
</div>

<!------------------------------------------------------------------------->

{% if form.subject.errors %}
    <ol>
    {% for error in form.subject.errors %}
        <li><strong>{{ error|escape }}</strong></li>
    {% endfor %}
    </ol>
{% endif %}
<!-------------------------------------------------------------------------->
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
        {% if field.help_text %}
        <p class="help">{{ field.help_text|safe }}</p>
        {% endif %}
    </div>
{% endfor %}

<!-------------------------------------------------------------------------->

{# Include the hidden fields #}
{% for hidden in form.hidden_fields %}
{{ hidden }}
{% endfor %}
{# Include the visible fields #}
{% for field in form.visible_fields %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
    
##### Reusable form templates #############
# In your form template:
{% include "form_snippet.html" %}

# In form_snippet.html:
{% for field in form %}
    <div class="fieldWrapper">
        {{ field.errors }}
        {{ field.label_tag }} {{ field }}
    </div>
{% endfor %}
#  forms with different name in context
{% include "form_snippet.html" with form=comment_form %}
    
    
########### SIMPLEISBETTERTHANCOMPLEX ######################

class ContactForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(),
        help_text='Write here your message!'
    )
    source = forms.CharField(       # A hidden input for internal use
        max_length=50,              # tell from which page the user sent the message
        widget=forms.HiddenInput()
    )

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        message = cleaned_data.get('message')
        if not name and not email and not message:
            raise forms.ValidationError('You have to write something!')

"""
<form method="post" novalidate>
  {% csrf_token %}
  {{ form }}
  <button type="submit">Submit</button>
</form>
<!------------------------------------------------>
<form method="post" novalidate>
  {% csrf_token %}
  <table border="1">
    {{ form }}
  </table>
  <button type="submit">Submit</button>
</form>
<!--------------------------------------------------------->
<form method="post" novalidate>
  {% csrf_token %}

  {{ form.non_field_errors }}

  {% for hidden_field in form.hidden_fields %}
    {{ hidden_field.errors }}
    {{ hidden_field }}
  {% endfor %}

  <table border="1">
    {% for field in form.visible_fields %}
      <tr>
        <th>{{ field.label_tag }}</th>
        <td>
          {{ field.errors }}
          {{ field }}
          {{ field.help_text }}
        </td>
      </tr>
    {% endfor %}
  </table>

  <button type="submit">Submit</button>
</form>

<!--------------------------------------------------------->

<form method="post" novalidate>
  {% csrf_token %}

  {% if form.non_field_errors %}
    <ul>
      {% for error in form.non_field_errors %}
        <li>{{ error }}</li>
      {% endfor %}
    </ul>
  {% endif %}

  {% for hidden_field in form.hidden_fields %}
    {% if hidden_field.errors %}
      <ul>
        {% for error in hidden_field.errors %}
          <li>(Hidden field {{ hidden_field.name }}) {{ error }}</li>
        {% endfor %}
      </ul>
    {% endif %}
    {{ hidden_field }}
  {% endfor %}

  <table border="1">
    {% for field in form.visible_fields %}
      <tr>
        <th>{{ field.label_tag }}</th>
        <td>
          {% if field.errors %}
            <ul>
              {% for error in field.errors %}
                <li>{{ error }}</li>
              {% endfor %}
            </ul>
          {% endif %}
          {{ field }}
          {% if field.help_text %}
            <br />{{ field.help_text }}
          {% endif %}
        </td>
      </tr>
    {% endfor %}
  </table>

  <button type="submit">Submit</button>
</form>


########### ACCESSING FORM FIELDS INDIVIDUALLY ############

<form method="post" novalidate>
  {% csrf_token %}

  {{ form.non_field_errors }}

  {{ form.source.errors }}
  {{ form.source }}

  <table border="1">

      <tr>
        <th>{{ form.name.label_tag }}</th>
        <td>
          {{ form.name.errors }}
          {{ form.name }}
        </td>
      </tr>

      <tr>
        <th>{{ form.email.label_tag }}</th>
        <td>
          {{ form.email.errors }}
          {{ form.email }}
        </td>
      </tr>

      <tr>
        <th>{{ form.message.label_tag }}</th>
        <td>
          {{ form.message.errors }}
          {{ form.message }}
          <br />
          {{ form.message.help_text }}
        </td>
      </tr>

  </table>

  <button type="submit">Submit</button>
</form>
"""
#### Expanding the Form Fields #####
"""
<input type="text"
       name="{{ form.name.name }}"
       id="{{ form.name.id_for_label }}"
       {% if form.name.value != None %}value="{{ form.name.value|stringformat:'s' }}"{% endif %}
       maxlength="{{ form.name.field.max_length }}"
       {% if form.name.field.required %}required{% endif %}>
"""
##### Using Custom HTML Attributes ######

class ColorfulContactForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Write your name here'
            }
        )
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'style': 'border-color: green;'})
    )
    message = forms.CharField(
        max_length=2000,
        widget=forms.Textarea(attrs={'style': 'border-color: orange;'}),
        help_text='Write here your message!'
    )
