import logging
from urlparse import urlparse
import urllib2

from django.core.files import File
from django.forms.widgets import ClearableFileInput
from django.core.files.storage import default_storage
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext


logger = logging.getLogger(__name__)


class S3FileInput(ClearableFileInput):
    needs_multipart_form = False
    signing_url = reverse_lazy('s3file-sign')
    template = (
        '<div class="s3file" data-url="{signing_url}" data-target="{element_id}">\n'
        '    <a class="link" target="_blank" href="{file_url}">{file_url}</a>\n'
        '    <a class="remove" href="javascript: void(0)">{remove}</a>\n'
        '    <input type="hidden" value="{value}" id="{element_id}" name="{name}" />\n'
        '    <input type="file" class="fileinput" id="s3-{element_id}" />\n'
        '    <div class="progress progress-striped active">\n'
        '        <div class="progress-bar"></div>\n'
        '    </div>\n'
        '</div>'
    )

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs)
        element_id = final_attrs.get('id')

        if isinstance(value, File):
            file_url = default_storage.url(value.name)
        else:
            file_url = ''

        if file_url:
            input_value = 'initial'
        else:
            input_value = ''

        output = self.template.format(
            signing_url=self.signing_url,
            file_url=file_url,
            element_id=element_id or '',
            name=name,
            value=input_value,
            remove=ugettext('remove')
        )

        return mark_safe(output)

    def value_from_datadict(self, data, files, name):
        filename = data.get(name)
        if not filename:
            return None
        elif filename == 'initial':
            return False
        else:
            f = default_storage.open(filename)
            return f

    class Media:
        js = (
            's3file/js/jquery.iframe-transport.js',
            's3file/js/jquery.ui.widget.js',
            's3file/js/jquery.fileupload.js',
            's3file/js/s3file.js',
        )
        css = {
            'all': (
                's3file/css/s3file.css',
            )
        }
