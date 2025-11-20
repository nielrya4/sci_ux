class HTMLElement:
    """Base class for HTML elements with common global attributes."""
    
    def __init__(self, content=None, **kwargs):
        # Global attributes available to all HTML elements
        self.id = kwargs.get('id')
        self.class_ = kwargs.get('class_')
        self.style = kwargs.get('style')
        self.title = kwargs.get('title')
        self.lang = kwargs.get('lang')
        self.dir = kwargs.get('dir')  # ltr, rtl, auto
        self.hidden = kwargs.get('hidden')
        self.tabindex = kwargs.get('tabindex')
        self.accesskey = kwargs.get('accesskey')
        self.contenteditable = kwargs.get('contenteditable')
        self.draggable = kwargs.get('draggable')
        self.spellcheck = kwargs.get('spellcheck')
        self.translate = kwargs.get('translate')
        self.role = kwargs.get('role')  # ARIA role
        self.data = kwargs.get('data', {})  # data-* attributes
        self.aria = kwargs.get('aria', {})  # aria-* attributes
        
        # Content management
        self.children = []
        self.text_content = ""
        
        # Handle content parameter
        if content is not None:
            if isinstance(content, str):
                self.text_content = content
            elif isinstance(content, HTMLElement):
                self.children.append(content)
            elif hasattr(content, '__iter__') and not isinstance(content, str):
                for item in content:
                    self.add(item)
    
    def add(self, *items):
        """Add child elements or text content. Returns self for method chaining."""
        for item in items:
            if isinstance(item, str):
                if self.text_content:
                    self.text_content += item
                else:
                    self.text_content = item
            elif isinstance(item, HTMLElement):
                self.children.append(item)
            elif hasattr(item, '__iter__') and not isinstance(item, str):
                for subitem in item:
                    self.add(subitem)
        return self
    
    
    def _get_tag_name(self):
        """Get the HTML tag name from the class name."""
        return self.__class__.__name__.lower()
    
    def _render_attributes(self):
        """Render HTML attributes as a string."""
        attrs = []
        
        if self.id:
            attrs.append(f'id="{self.id}"')
        if self.class_:
            attrs.append(f'class="{self.class_}"')
        if self.style:
            attrs.append(f'style="{self.style}"')
        if self.title:
            attrs.append(f'title="{self.title}"')
        if self.lang:
            attrs.append(f'lang="{self.lang}"')
        if self.dir:
            attrs.append(f'dir="{self.dir}"')
        if self.hidden is not None:
            attrs.append('hidden' if self.hidden else '')
        if self.tabindex is not None:
            attrs.append(f'tabindex="{self.tabindex}"')
        if self.accesskey:
            attrs.append(f'accesskey="{self.accesskey}"')
        if self.contenteditable is not None:
            attrs.append(f'contenteditable="{str(self.contenteditable).lower()}"')
        if self.draggable is not None:
            attrs.append(f'draggable="{str(self.draggable).lower()}"')
        if self.spellcheck is not None:
            attrs.append(f'spellcheck="{str(self.spellcheck).lower()}"')
        if self.translate is not None:
            attrs.append(f'translate="{str(self.translate).lower()}"')
        if self.role:
            attrs.append(f'role="{self.role}"')
        
        # Data attributes
        for key, value in self.data.items():
            attrs.append(f'data-{key}="{value}"')
        
        # ARIA attributes
        for key, value in self.aria.items():
            attrs.append(f'aria-{key}="{value}"')
        
        return ' '.join(filter(None, attrs))
    
    def to_html(self, indent=0):
        """Render the element as HTML string."""
        tag_name = self._get_tag_name()
        attrs = self._render_attributes()
        indent_str = '  ' * indent
        
        # Handle void elements (self-closing tags)
        if tag_name in ['img', 'input', 'br', 'hr', 'meta', 'link', 'track', 'source', 'col', 'area', 'base']:
            if attrs:
                return f'{indent_str}<{tag_name} {attrs}>'
            else:
                return f'{indent_str}<{tag_name}>'
        
        # Build opening tag
        if attrs:
            opening = f'{indent_str}<{tag_name} {attrs}>'
        else:
            opening = f'{indent_str}<{tag_name}>'
        
        # Handle content
        content_parts = []
        
        # Add text content
        if self.text_content:
            content_parts.append(self.text_content)
        
        # Add child elements
        if self.children:
            for child in self.children:
                content_parts.append('\n' + child.to_html(indent + 1))
            if content_parts and not self.text_content:
                content_parts.append('\n' + indent_str)
        
        # Close tag
        closing = f'</{tag_name}>'
        
        if content_parts:
            content = ''.join(content_parts)
            return f'{opening}{content}{closing}'
        else:
            return f'{opening}{closing}'
    
    def __str__(self):
        """Return HTML representation."""
        return self.to_html()


class Div(HTMLElement):
    """Division element for grouping content."""
    pass


class Span(HTMLElement):
    """Inline text container."""
    pass


class P(HTMLElement):
    """Paragraph element."""
    pass


class H1(HTMLElement):
    """Heading level 1."""
    pass


class H2(HTMLElement):
    """Heading level 2."""
    pass


class H3(HTMLElement):
    """Heading level 3."""
    pass


class H4(HTMLElement):
    """Heading level 4."""
    pass


class H5(HTMLElement):
    """Heading level 5."""
    pass


class H6(HTMLElement):
    """Heading level 6."""
    pass


class A(HTMLElement):
    """Anchor/link element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.href = kwargs.get('href')
        self.target = kwargs.get('target')  # _blank, _self, _parent, _top
        self.download = kwargs.get('download')
        self.rel = kwargs.get('rel')  # nofollow, noopener, noreferrer, etc.
        self.type = kwargs.get('type')  # MIME type
        self.hreflang = kwargs.get('hreflang')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.href:
            element_attrs.append(f'href="{self.href}"')
        if self.target:
            element_attrs.append(f'target="{self.target}"')
        if self.download is not None:
            element_attrs.append(f'download="{self.download}" ' if self.download else 'download')
        if self.rel:
            element_attrs.append(f'rel="{self.rel}"')
        if self.type:
            element_attrs.append(f'type="{self.type}"')
        if self.hreflang:
            element_attrs.append(f'hreflang="{self.hreflang}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Img(HTMLElement):
    """Image element."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.src = kwargs.get('src')
        self.alt = kwargs.get('alt')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.loading = kwargs.get('loading')  # lazy, eager
        self.srcset = kwargs.get('srcset')
        self.sizes = kwargs.get('sizes')
        self.usemap = kwargs.get('usemap')
        self.ismap = kwargs.get('ismap')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.src:
            element_attrs.append(f'src="{self.src}"')
        if self.alt is not None:
            element_attrs.append(f'alt="{self.alt}"')
        if self.width:
            element_attrs.append(f'width="{self.width}"')
        if self.height:
            element_attrs.append(f'height="{self.height}"')
        if self.loading:
            element_attrs.append(f'loading="{self.loading}"')
        if self.srcset:
            element_attrs.append(f'srcset="{self.srcset}"')
        if self.sizes:
            element_attrs.append(f'sizes="{self.sizes}"')
        if self.usemap:
            element_attrs.append(f'usemap="{self.usemap}"')
        if self.ismap:
            element_attrs.append('ismap')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Button(HTMLElement):
    """Button element."""
    
    def __init__(self, content=None, **kwargs):
        # Extract button-specific attributes before calling super().__init__()
        self.type = kwargs.pop('type', 'button')  # button, submit, reset
        self.disabled = kwargs.pop('disabled', None)
        self.form = kwargs.pop('form', None)
        self.formaction = kwargs.pop('formaction', None)
        self.formenctype = kwargs.pop('formenctype', None)
        self.formmethod = kwargs.pop('formmethod', None)
        self.formnovalidate = kwargs.pop('formnovalidate', None)
        self.formtarget = kwargs.pop('formtarget', None)
        self.name = kwargs.pop('name', None)
        self.value = kwargs.pop('value', None)
        
        # Call parent with remaining kwargs (including class_, id, etc.)
        super().__init__(content, **kwargs)
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.type:
            element_attrs.append(f'type="{self.type}"')
        if self.disabled:
            element_attrs.append('disabled')
        if self.form:
            element_attrs.append(f'form="{self.form}"')
        if self.formaction:
            element_attrs.append(f'formaction="{self.formaction}"')
        if self.formenctype:
            element_attrs.append(f'formenctype="{self.formenctype}"')
        if self.formmethod:
            element_attrs.append(f'formmethod="{self.formmethod}"')
        if self.formnovalidate:
            element_attrs.append('formnovalidate')
        if self.formtarget:
            element_attrs.append(f'formtarget="{self.formtarget}"')
        if self.name:
            element_attrs.append(f'name="{self.name}"')
        if self.value is not None:
            element_attrs.append(f'value="{self.value}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Input(HTMLElement):
    """Input element for form controls."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = kwargs.get('type', 'text')  # text, password, email, number, etc.
        self.name = kwargs.get('name')
        self.value = kwargs.get('value')
        self.placeholder = kwargs.get('placeholder')
        self.required = kwargs.get('required')
        self.disabled = kwargs.get('disabled')
        self.readonly = kwargs.get('readonly')
        self.maxlength = kwargs.get('maxlength')
        self.minlength = kwargs.get('minlength')
        self.min = kwargs.get('min')
        self.max = kwargs.get('max')
        self.step = kwargs.get('step')
        self.pattern = kwargs.get('pattern')
        self.autocomplete = kwargs.get('autocomplete')
        self.autofocus = kwargs.get('autofocus')
        self.checked = kwargs.get('checked')
        self.multiple = kwargs.get('multiple')
        self.size = kwargs.get('size')
        self.form = kwargs.get('form')
        self.list = kwargs.get('list')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.type:
            element_attrs.append(f'type="{self.type}"')
        if self.name:
            element_attrs.append(f'name="{self.name}"')
        if self.value is not None:
            element_attrs.append(f'value="{self.value}"')
        if self.placeholder:
            element_attrs.append(f'placeholder="{self.placeholder}"')
        if self.required:
            element_attrs.append('required')
        if self.disabled:
            element_attrs.append('disabled')
        if self.readonly:
            element_attrs.append('readonly')
        if self.maxlength is not None:
            element_attrs.append(f'maxlength="{self.maxlength}"')
        if self.minlength is not None:
            element_attrs.append(f'minlength="{self.minlength}"')
        if self.min is not None:
            element_attrs.append(f'min="{self.min}"')
        if self.max is not None:
            element_attrs.append(f'max="{self.max}"')
        if self.step is not None:
            element_attrs.append(f'step="{self.step}"')
        if self.pattern:
            element_attrs.append(f'pattern="{self.pattern}"')
        if self.autocomplete:
            element_attrs.append(f'autocomplete="{self.autocomplete}"')
        if self.autofocus:
            element_attrs.append('autofocus')
        if self.checked:
            element_attrs.append('checked')
        if self.multiple:
            element_attrs.append('multiple')
        if self.size is not None:
            element_attrs.append(f'size="{self.size}"')
        if self.form:
            element_attrs.append(f'form="{self.form}"')
        if self.list:
            element_attrs.append(f'list="{self.list}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Form(HTMLElement):
    """Form element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.action = kwargs.get('action')
        self.method = kwargs.get('method', 'get')  # get, post
        self.enctype = kwargs.get('enctype')  # application/x-www-form-urlencoded, multipart/form-data, text/plain
        self.target = kwargs.get('target')
        self.novalidate = kwargs.get('novalidate')
        self.autocomplete = kwargs.get('autocomplete')
        self.name = kwargs.get('name')


class Label(HTMLElement):
    """Label element for form controls."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.for_ = kwargs.get('for')  # ID of associated form control
        self.form = kwargs.get('form')


class Select(HTMLElement):
    """Select dropdown element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.name = kwargs.get('name')
        self.multiple = kwargs.get('multiple')
        self.size = kwargs.get('size')
        self.disabled = kwargs.get('disabled')
        self.required = kwargs.get('required')
        self.autofocus = kwargs.get('autofocus')
        self.form = kwargs.get('form')


class Option(HTMLElement):
    """Option element for select dropdowns."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.value = kwargs.get('value')
        self.selected = kwargs.get('selected')
        self.disabled = kwargs.get('disabled')
        self.label = kwargs.get('label')


class Textarea(HTMLElement):
    """Textarea element for multi-line text input."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.name = kwargs.get('name')
        self.rows = kwargs.get('rows')
        self.cols = kwargs.get('cols')
        self.placeholder = kwargs.get('placeholder')
        self.required = kwargs.get('required')
        self.disabled = kwargs.get('disabled')
        self.readonly = kwargs.get('readonly')
        self.maxlength = kwargs.get('maxlength')
        self.minlength = kwargs.get('minlength')
        self.wrap = kwargs.get('wrap')  # soft, hard
        self.autofocus = kwargs.get('autofocus')
        self.form = kwargs.get('form')


class Table(HTMLElement):
    """Table element."""
    pass


class Tr(HTMLElement):
    """Table row element."""
    pass


class Td(HTMLElement):
    """Table data cell element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.colspan = kwargs.get('colspan')
        self.rowspan = kwargs.get('rowspan')
        self.headers = kwargs.get('headers')


class Th(HTMLElement):
    """Table header cell element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.colspan = kwargs.get('colspan')
        self.rowspan = kwargs.get('rowspan')
        self.scope = kwargs.get('scope')  # row, col, rowgroup, colgroup
        self.headers = kwargs.get('headers')


class Thead(HTMLElement):
    """Table head element."""
    pass


class Tbody(HTMLElement):
    """Table body element."""
    pass


class Tfoot(HTMLElement):
    """Table foot element."""
    pass


class Ul(HTMLElement):
    """Unordered list element."""
    pass


class Ol(HTMLElement):
    """Ordered list element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.start = kwargs.get('start')
        self.reversed = kwargs.get('reversed')
        self.type = kwargs.get('type')  # 1, A, a, I, i


class Li(HTMLElement):
    """List item element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.value = kwargs.get('value')  # For ordered lists


class Nav(HTMLElement):
    """Navigation element."""
    pass


class Header(HTMLElement):
    """Header element."""
    pass


class Footer(HTMLElement):
    """Footer element."""
    pass


class Main(HTMLElement):
    """Main content element."""
    pass


class Section(HTMLElement):
    """Section element."""
    pass


class Article(HTMLElement):
    """Article element."""
    pass


class Aside(HTMLElement):
    """Aside element for sidebar content."""
    pass


class Video(HTMLElement):
    """Video element."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.src = kwargs.get('src')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.controls = kwargs.get('controls')
        self.autoplay = kwargs.get('autoplay')
        self.loop = kwargs.get('loop')
        self.muted = kwargs.get('muted')
        self.poster = kwargs.get('poster')
        self.preload = kwargs.get('preload')  # auto, metadata, none


class Audio(HTMLElement):
    """Audio element."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.src = kwargs.get('src')
        self.controls = kwargs.get('controls')
        self.autoplay = kwargs.get('autoplay')
        self.loop = kwargs.get('loop')
        self.muted = kwargs.get('muted')
        self.preload = kwargs.get('preload')  # auto, metadata, none


class Canvas(HTMLElement):
    """Canvas element for graphics."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')


class Iframe(HTMLElement):
    """Iframe element for embedding content."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.src = kwargs.get('src')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.name = kwargs.get('name')
        self.sandbox = kwargs.get('sandbox')
        self.allow = kwargs.get('allow')
        self.loading = kwargs.get('loading')  # lazy, eager


class Html(HTMLElement):
    """Root HTML element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.lang = kwargs.get('lang', 'en')


class Head(HTMLElement):
    """Document head element."""
    pass


class Body(HTMLElement):
    """Document body element."""
    pass


class Title(HTMLElement):
    """Document title element."""
    pass


class Meta(HTMLElement):
    """Meta information element."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.charset = kwargs.get('charset')
        self.name = kwargs.get('name')
        self.content = kwargs.get('content')
        self.http_equiv = kwargs.get('http_equiv')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.charset:
            element_attrs.append(f'charset="{self.charset}"')
        if self.name:
            element_attrs.append(f'name="{self.name}"')
        if self.content:
            element_attrs.append(f'content="{self.content}"')
        if self.http_equiv:
            element_attrs.append(f'http-equiv="{self.http_equiv}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Link(HTMLElement):
    """Link element for external resources."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rel = kwargs.get('rel')
        self.href = kwargs.get('href')
        self.type = kwargs.get('type')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.rel:
            element_attrs.append(f'rel="{self.rel}"')
        if self.href:
            element_attrs.append(f'href="{self.href}"')
        if self.type:
            element_attrs.append(f'type="{self.type}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Style(HTMLElement):
    """Style element for CSS."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.css_rules = []
    
    def add(self, *items):
        """Add CSS rules, raw CSS strings, or text content."""
        from css import CSSRule, MediaQuery, CSSBuilder
        
        for item in items:
            if isinstance(item, (CSSRule, MediaQuery)):
                self.css_rules.append(item)
            elif isinstance(item, str):
                if self.text_content:
                    self.text_content += item
                else:
                    self.text_content = item
            elif hasattr(item, 'to_css'):
                # Any object with to_css method
                self.css_rules.append(item)
        return self
    
    def to_html(self, indent=0):
        """Render the style element as HTML with CSS content."""
        # Build CSS content from rules
        css_content = ""
        if self.css_rules:
            css_parts = []
            for rule in self.css_rules:
                rule_css = rule.to_css()
                if rule_css:
                    css_parts.append(rule_css)
            css_content = "\n".join(css_parts)
        
        # Combine with any text content
        if self.text_content and css_content:
            combined_content = f"{self.text_content}\n{css_content}"
        elif css_content:
            combined_content = css_content
        else:
            combined_content = self.text_content
        
        # Temporarily store the combined content
        original_text = self.text_content
        original_children = self.children[:]
        
        self.text_content = combined_content
        self.children = []
        
        # Render as normal HTML element
        result = super().to_html(indent)
        
        # Restore original state
        self.text_content = original_text
        self.children = original_children
        
        return result


class Script(HTMLElement):
    """Script element for JavaScript."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.src = kwargs.get('src')
        self.type = kwargs.get('type', 'text/javascript')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.src:
            element_attrs.append(f'src="{self.src}"')
        if self.type:
            element_attrs.append(f'type="{self.type}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Br(HTMLElement):
    """Line break element."""
    pass


class Hr(HTMLElement):
    """Horizontal rule element."""
    pass


# Text formatting elements
class B(HTMLElement):
    """Bold text element."""
    pass


class I(HTMLElement):
    """Italic text element."""
    pass


class Strong(HTMLElement):
    """Strong emphasis element."""
    pass


class Em(HTMLElement):
    """Emphasis element."""
    pass


class U(HTMLElement):
    """Underlined text element."""
    pass


class S(HTMLElement):
    """Strikethrough text element."""
    pass


class Small(HTMLElement):
    """Small text element."""
    pass


class Mark(HTMLElement):
    """Marked/highlighted text element."""
    pass


class Del(HTMLElement):
    """Deleted text element."""
    pass


class Ins(HTMLElement):
    """Inserted text element."""
    pass


class Sub(HTMLElement):
    """Subscript element."""
    pass


class Sup(HTMLElement):
    """Superscript element."""
    pass


class Code(HTMLElement):
    """Inline code element."""
    pass


class Pre(HTMLElement):
    """Preformatted text element."""
    pass


class Kbd(HTMLElement):
    """Keyboard input element."""
    pass


class Samp(HTMLElement):
    """Sample output element."""
    pass


class Var(HTMLElement):
    """Variable element."""
    pass


class Cite(HTMLElement):
    """Citation element."""
    pass


class Q(HTMLElement):
    """Short quotation element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.cite = kwargs.get('cite')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.cite:
            element_attrs.append(f'cite="{self.cite}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Abbr(HTMLElement):
    """Abbreviation element."""
    pass


class Dfn(HTMLElement):
    """Definition element."""
    pass


class Time(HTMLElement):
    """Time element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.datetime = kwargs.get('datetime')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.datetime:
            element_attrs.append(f'datetime="{self.datetime}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


# Structural elements
class Blockquote(HTMLElement):
    """Block quotation element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.cite = kwargs.get('cite')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.cite:
            element_attrs.append(f'cite="{self.cite}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Address(HTMLElement):
    """Contact information element."""
    pass


class Figure(HTMLElement):
    """Figure element."""
    pass


class Figcaption(HTMLElement):
    """Figure caption element."""
    pass


class Details(HTMLElement):
    """Details disclosure element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.open = kwargs.get('open')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.open:
            element_attrs.append('open')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Summary(HTMLElement):
    """Summary element for details."""
    pass


class Dialog(HTMLElement):
    """Dialog element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.open = kwargs.get('open')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.open:
            element_attrs.append('open')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


# Form elements
class Fieldset(HTMLElement):
    """Fieldset element for grouping form controls."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.disabled = kwargs.get('disabled')
        self.form = kwargs.get('form')
        self.name = kwargs.get('name')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.disabled:
            element_attrs.append('disabled')
        if self.form:
            element_attrs.append(f'form="{self.form}"')
        if self.name:
            element_attrs.append(f'name="{self.name}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Legend(HTMLElement):
    """Legend element for fieldsets."""
    pass


class Datalist(HTMLElement):
    """Datalist element for input suggestions."""
    pass


class Output(HTMLElement):
    """Output element for calculation results."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.for_ = kwargs.get('for')
        self.form = kwargs.get('form')
        self.name = kwargs.get('name')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.for_:
            element_attrs.append(f'for="{self.for_}"')
        if self.form:
            element_attrs.append(f'form="{self.form}"')
        if self.name:
            element_attrs.append(f'name="{self.name}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Progress(HTMLElement):
    """Progress indicator element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.value = kwargs.get('value')
        self.max = kwargs.get('max')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.value is not None:
            element_attrs.append(f'value="{self.value}"')
        if self.max is not None:
            element_attrs.append(f'max="{self.max}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Meter(HTMLElement):
    """Scalar measurement element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.value = kwargs.get('value')
        self.min = kwargs.get('min')
        self.max = kwargs.get('max')
        self.low = kwargs.get('low')
        self.high = kwargs.get('high')
        self.optimum = kwargs.get('optimum')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.value is not None:
            element_attrs.append(f'value="{self.value}"')
        if self.min is not None:
            element_attrs.append(f'min="{self.min}"')
        if self.max is not None:
            element_attrs.append(f'max="{self.max}"')
        if self.low is not None:
            element_attrs.append(f'low="{self.low}"')
        if self.high is not None:
            element_attrs.append(f'high="{self.high}"')
        if self.optimum is not None:
            element_attrs.append(f'optimum="{self.optimum}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


# Description list elements
class Dl(HTMLElement):
    """Description list element."""
    pass


class Dt(HTMLElement):
    """Description term element."""
    pass


class Dd(HTMLElement):
    """Description definition element."""
    pass


# Additional table elements
class Caption(HTMLElement):
    """Table caption element."""
    pass


class Colgroup(HTMLElement):
    """Column group element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.span = kwargs.get('span')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.span is not None:
            element_attrs.append(f'span="{self.span}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Col(HTMLElement):
    """Column element."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.span = kwargs.get('span')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.span is not None:
            element_attrs.append(f'span="{self.span}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


# Media elements
class Track(HTMLElement):
    """Track element for media captions/subtitles."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kind = kwargs.get('kind', 'subtitles')
        self.src = kwargs.get('src')
        self.srclang = kwargs.get('srclang')
        self.label = kwargs.get('label')
        self.default = kwargs.get('default')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.kind:
            element_attrs.append(f'kind="{self.kind}"')
        if self.src:
            element_attrs.append(f'src="{self.src}"')
        if self.srclang:
            element_attrs.append(f'srclang="{self.srclang}"')
        if self.label:
            element_attrs.append(f'label="{self.label}"')
        if self.default:
            element_attrs.append('default')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Source(HTMLElement):
    """Source element for media resources."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.src = kwargs.get('src')
        self.type = kwargs.get('type')
        self.media = kwargs.get('media')
        self.srcset = kwargs.get('srcset')
        self.sizes = kwargs.get('sizes')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.src:
            element_attrs.append(f'src="{self.src}"')
        if self.type:
            element_attrs.append(f'type="{self.type}"')
        if self.media:
            element_attrs.append(f'media="{self.media}"')
        if self.srcset:
            element_attrs.append(f'srcset="{self.srcset}"')
        if self.sizes:
            element_attrs.append(f'sizes="{self.sizes}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Picture(HTMLElement):
    """Picture element for responsive images."""
    pass


# Interactive elements
class Map(HTMLElement):
    """Image map element."""
    
    def __init__(self, content=None, **kwargs):
        super().__init__(content, **kwargs)
        self.name = kwargs.get('name')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.name:
            element_attrs.append(f'name="{self.name}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Area(HTMLElement):
    """Area element for image maps."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shape = kwargs.get('shape', 'rect')
        self.coords = kwargs.get('coords')
        self.href = kwargs.get('href')
        self.alt = kwargs.get('alt')
        self.target = kwargs.get('target')
        self.download = kwargs.get('download')
        self.ping = kwargs.get('ping')
        self.rel = kwargs.get('rel')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.shape:
            element_attrs.append(f'shape="{self.shape}"')
        if self.coords:
            element_attrs.append(f'coords="{self.coords}"')
        if self.href:
            element_attrs.append(f'href="{self.href}"')
        if self.alt:
            element_attrs.append(f'alt="{self.alt}"')
        if self.target:
            element_attrs.append(f'target="{self.target}"')
        if self.download is not None:
            element_attrs.append(f'download="{self.download}" ' if self.download else 'download')
        if self.ping:
            element_attrs.append(f'ping="{self.ping}"')
        if self.rel:
            element_attrs.append(f'rel="{self.rel}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


# Document structure
class Base(HTMLElement):
    """Base URL element."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.href = kwargs.get('href')
        self.target = kwargs.get('target')
    
    def _render_attributes(self):
        attrs = super()._render_attributes()
        element_attrs = []
        
        if self.href:
            element_attrs.append(f'href="{self.href}"')
        if self.target:
            element_attrs.append(f'target="{self.target}"')
        
        all_attrs = [attrs] + element_attrs if attrs else element_attrs
        return ' '.join(filter(None, all_attrs))


class Noscript(HTMLElement):
    """Noscript element for when JavaScript is disabled."""
    pass