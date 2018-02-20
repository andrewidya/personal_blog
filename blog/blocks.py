from django.utils.safestring import mark_safe

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtail.wagtailcore.blocks import (CharBlock, ChoiceBlock, RichTextBlock,
                                        TextBlock, StructBlock, RawHTMLBlock)
from wagtail.wagtailimages.blocks import ImageChooserBlock
from wagtail.wagtaildocs.blocks import DocumentChooserBlock
from wagtail.wagtailembeds.blocks import EmbedBlock
from wagtail.wagtailcore.rich_text import (RichText as DefaultRichText, expand_db_html)
from wagtail.contrib.table_block.blocks import TableBlock

from smartstream.blocks import StreamBlock


class CustomRichText(DefaultRichText):

    def __html__(self):
        return expand_db_html(self.source)


class CustomRichTextBlock(RichTextBlock):

    def get_default(self):
        if isinstance(self.meta.default, CustomRichText):
            return self.meta.default
        else:
            return CustomRichText(self.meta.default)

    def to_python(self, value):
        # convert a source-HTML string from the JSONish representation
        # to a RichText object
        return CustomRichText(value)

    def value_from_form(self, value):
        # Rich text editors return a source-HTML string; convert to a RichText object
        return CustomRichText(value)


class ImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    caaption = CharBlock(required=False)
    attribute = CharBlock(required=False)

    class Meta:
        icon = 'image'
        template = 'blog/blocks/image_block.html'


class HeadingBlock(StructBlock):
    SIZE_CHOICES = (
        ('h2', 'H2'),
        ('h3', 'H3'),
        ('h4', 'H4'),
        ('h5', 'H5'),
        ('h6', 'H6')
    )
    text = CharBlock(required=True)
    size = ChoiceBlock(choices=SIZE_CHOICES, blank=True, required=False)

    class Meta:
        icon = 'title'
        template = 'blog/blocks/heading_block.html'


class BlockQuoteBlock(StructBlock):
    text = TextBlock()
    attribute = CharBlock(blank=True, required=False)

    class Meta:
        icon = 'openquote'
        template = 'blog/blocks/blockquote_block.html'


class CodeBlock(StructBlock):
    LANGUAGE_CHOICES = (
        ('python', 'Python'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('scss', 'SCSS'),
        ('json', 'JSON'),
        ('sh', 'Shell'),
    )

    STYLE_CHOICES = (
        ('syntax', 'default'),
        ('monokai', 'monokai'),
        ('xcode', 'xcode'),
    )

    language = ChoiceBlock(choices=LANGUAGE_CHOICES)
    style = ChoiceBlock(choices=STYLE_CHOICES, default='syntax')
    code = TextBlock()

    def render(self, value, context=None):
        src = value['code'].strip('\n')
        lang = value['language']
        lexer = get_lexer_by_name(lang)
        css_classes = ['code', value['style']]

        formatter = get_formatter_by_name(
            'html', lineos=None, cssclass=' '.join(css_classes), noclasses=False)

        return mark_safe(highlight(src, lexer, formatter))

    class Meta:
        icon = 'code'


class BodyStreamBlock(StreamBlock):
    heading = HeadingBlock()
    paragraph = CustomRichTextBlock(
        features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link'])
    image = ImageBlock()
    blockquote = BlockQuoteBlock()
    embed = EmbedBlock()
    document = DocumentChooserBlock()
    code = CodeBlock()
    raw_html = RawHTMLBlock()
    table = TableBlock()


class CarouselImageBlock(StructBlock):
    image = ImageChooserBlock()
    heading = CharBlock(required=False)
    text = CharBlock(required=False)

    class Meta:
        icon = 'image'

    def render(self, value, context=None):
        image = value['image'].get_rendition('width-800')
        heading = value['heading'] if value['heading'] else ""
        text = value['text'] if value['heading'] else ""

        html = '<div class="carouesl-item">'
        html += '<img src="{}" alt="{}">'.format(image.url, image.alt)
        html += '<div class="carousel-caption">'
        html += '<h3>{}</h3>'.format(heading)
        html += '<p>{}</p>'.format(text)
        html += '</div></div>'

        return mark_safe(html)


class CarouselVidoeBlock(StructBlock):
    video = EmbedBlock()
    heading = CharBlock(required=False)
    text = CharBlock(required=False)

    class Meta:
        icon = 'media'

    def render(self, value, context=None):
        import pdb
        pdb.set_trace()

        video = value['video']
        heading = value['heading'] if value['heading'] else ""
        text = value['text'] if value['heading'] else ""

        html = '<div class="carouesl-item">'
        html += '<video src="{}">'.format(video.url)
        html += '<div class="carousel-caption">'
        html += '<h3>{}</h3>'.format(heading)
        html += '<p>{}</p>'.format(text)
        html += '</div></div>'

        return mark_safe(html)


class CarouselBlock(StreamBlock):
    image = CarouselImageBlock()
    # video = CarouselVidoeBlock()
