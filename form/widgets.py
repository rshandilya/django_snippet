#### TO ITERATE OVER CHOICES IN RADIOSELECT ####

{% for choice in form.pc_type %}
  {{ choice.choice_label }}
  <span class="radio">{{ choice.tag }}</span>
{% endfor %}
