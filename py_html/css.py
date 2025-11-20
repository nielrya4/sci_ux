class CSSRule:
    """Base class for CSS rules."""
    
    def __init__(self, selector, **properties):
        self.selector = selector
        self.properties = properties
    
    def _convert_property_name(self, name):
        """Convert Python property names to CSS property names."""
        # Convert snake_case to kebab-case
        return name.replace('_', '-')
    
    def _render_properties(self):
        """Render CSS properties as a string."""
        if not self.properties:
            return ""
        
        prop_strings = []
        for name, value in self.properties.items():
            css_name = self._convert_property_name(name)
            prop_strings.append(f"{css_name}: {value}")
        
        return "; ".join(prop_strings)
    
    def to_css(self, indent=0):
        """Render the rule as CSS string."""
        indent_str = "  " * indent
        properties = self._render_properties()
        
        if not properties:
            return ""
        
        return f"{indent_str}{self.selector} {{\n{indent_str}  {properties};\n{indent_str}}}"
    
    def __str__(self):
        return self.to_css()


class MediaQuery:
    """CSS media query container."""
    
    def __init__(self, condition):
        self.condition = condition
        self.rules = []
    
    def add(self, *rules):
        """Add CSS rules to this media query."""
        for rule in rules:
            if isinstance(rule, (CSSRule, MediaQuery)):
                self.rules.append(rule)
        return self
    
    def to_css(self, indent=0):
        """Render the media query as CSS string."""
        if not self.rules:
            return ""
        
        indent_str = "  " * indent
        css_parts = [f"{indent_str}@media ({self.condition}) {{"]
        
        for rule in self.rules:
            rule_css = rule.to_css(indent + 1)
            if rule_css:
                css_parts.append(rule_css)
        
        css_parts.append(f"{indent_str}}}")
        return "\n".join(css_parts)
    
    def __str__(self):
        return self.to_css()


class CSS:
    """CSS builder class with static methods for creating selectors."""
    
    @staticmethod
    def element(tag_name, **properties):
        """Create a CSS rule for an HTML element."""
        return CSSRule(tag_name, **properties)
    
    @staticmethod
    def class_(class_name, **properties):
        """Create a CSS rule for a class selector."""
        # Add dot prefix if not present
        selector = f".{class_name}" if not class_name.startswith('.') else class_name
        return CSSRule(selector, **properties)
    
    @staticmethod
    def id(id_name, **properties):
        """Create a CSS rule for an ID selector."""
        # Add hash prefix if not present
        selector = f"#{id_name}" if not id_name.startswith('#') else id_name
        return CSSRule(selector, **properties)
    
    @staticmethod
    def selector(selector_string, **properties):
        """Create a CSS rule for any custom selector."""
        return CSSRule(selector_string, **properties)
    
    @staticmethod
    def media(condition):
        """Create a media query."""
        return MediaQuery(condition)


class CSSBuilder:
    """CSS builder for collecting and rendering multiple CSS rules."""
    
    def __init__(self):
        self.rules = []
    
    def add(self, *rules):
        """Add CSS rules or media queries."""
        for rule in rules:
            if isinstance(rule, (CSSRule, MediaQuery)):
                self.rules.append(rule)
            elif isinstance(rule, str):
                # Allow raw CSS strings
                self.rules.append(RawCSS(rule))
        return self
    
    def to_css(self):
        """Render all rules as CSS string."""
        css_parts = []
        for rule in self.rules:
            rule_css = rule.to_css()
            if rule_css:
                css_parts.append(rule_css)
        return "\n\n".join(css_parts)
    
    def __str__(self):
        return self.to_css()


class RawCSS:
    """Container for raw CSS strings."""
    
    def __init__(self, css_string):
        self.css_string = css_string
    
    def to_css(self, indent=0):
        """Return the raw CSS string."""
        return self.css_string
    
    def __str__(self):
        return self.css_string