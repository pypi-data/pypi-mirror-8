from django.utils.encoding import force_text
import docutils
from docutils.core import publish_programmatically
from docutils.writers import html4css1

from radpress.readers import BaseReader
from radpress.rst_extensions import register_directives
from radpress.settings import RST_SETTINGS


# register radpress customized directives
register_directives()


class Reader(BaseReader):
    """
    Radpress' default reader. It should be always enabled.
    """
    name = 'reStructuredText'
    enabled = True
    initial = """
        Title here
        ##########
        :slug: title-here
        :tags: world, big bang, sheldon
        :published: no
        :image: not specified

        Content here...
    """
    description = initial

    def _parse_metadata(self, document):
        output = {
            'title': document.get('title'),
            'published': False
        }

        for docinfo in document.traverse(docutils.nodes.docinfo):
            for element in docinfo.children:
                if element.tagname != 'field':
                    continue

                name_elem, body_elem = element.children
                name = name_elem.astext().lower()
                value = body_elem.astext()

                if name == 'tags':
                    value = set([t.strip() for t in value.split(',')])

                elif name == 'published':
                    value = value == 'yes'

                output[name] = value

        return output

    def _get_publisher(self):
        output, pub = publish_programmatically(
            source=self.source,
            source_path=None,
            source_class=docutils.io.StringInput,
            destination_class=docutils.io.StringOutput,
            destination=None,
            destination_path=None,
            reader=None,
            reader_name='standalone',
            parser=None,
            parser_name='restructuredtext',
            writer=html4css1.Writer(),
            writer_name='pseudoxml',
            settings=None,
            settings_spec=None,
            settings_overrides=RST_SETTINGS,
            config_section=None,
            enable_exit_status=False)

        return pub

    def read(self):
        pub = self._get_publisher()
        metadata = self._parse_metadata(pub.document)
        content = force_text(pub.writer.parts.get('body'))

        return content, metadata
