from cornice import Service
from daybed import __version__ as VERSION


hello = Service(name="hello", path='/', description="Welcome")


@hello.get()
def get_hello(request):
    """Return information regarding the current instance."""
    return dict(daybed='hello',
                version=VERSION,
                url=request.host_url)
