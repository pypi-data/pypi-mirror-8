from tendenci.core.registry import site
from tendenci.core.registry.base import CoreRegistry, lazy_reverse
from tendenci.apps.navs.models import Nav


class NavRegistry(CoreRegistry):
    version = '1.0'
    author = 'Schipul - The Web Marketing Company'
    author_email = 'programmers@schipul.com'
    description = 'Create navs for navigation'

    url = {
        'add': lazy_reverse('navs.add'),
        'search': lazy_reverse('navs.search'),
    }

site.register(Nav, NavRegistry)
