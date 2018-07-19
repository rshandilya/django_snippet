# widget.py
class MarkdownEditor(forms.Widget):
    """
    Code Editor built upon Javascript editor:CodeMirror
    """
    class Media:
        css = {
            'all': (
                'codemirror/codemirror.css',
                'codemirror/mdn-like.css',
            )
        }

        js = ('codemirror/codemirror.js', 'codemirror/mode/markdown/markdown.js')

    def render(self, name, value, attrs=None, renderer=None):

        template = '''
            <textarea name="%(name)s" id="id_%(name)s" required="" class="vLargeTextField">%(value)s
            <style>
                .CodeMirror {
                    height: auto;
                }
                .CodeMirror-scroll {
                    min-height: 300px;
                }
            </style>
            <script>
                var editorElem = document.querySelector("#id_%(name)s");
                var editor = CodeMirror.fromTextArea(editorElem, {
                    lineWrapping: true,
                    theme: 'mdn-like',
                    lineNumbers: true,
                });
            </script>
        '''
        context = {'name': name, 'value': escape(value) if value else ''}
        return mark_safe(template % context)
    
# admin.py
from django.contrib import admin

from .forms import PostForm
from blog.models import Post


class PostAdmin(admin.ModelAdmin):
    form = PostForm

    list_display = ('title', 'created_on', 'is_draft')

admin.site.register(Post, PostAdmin)
    
        
# forms.py

from django import forms

from .models import Post
from .widgets import MarkdownEditor


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'content': MarkdownEditor,
        }
