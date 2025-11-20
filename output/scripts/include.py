
from py_html.elements import H1, P, Div

def hi():
    """Return a greeting as a py_html element."""
    return Div().add(
        H1("Hello from include.py!"),
        P("This function was imported from the scripts/include.py module.")
    )