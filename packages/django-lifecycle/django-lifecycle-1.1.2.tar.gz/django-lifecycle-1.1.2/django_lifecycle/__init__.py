__version__ = "1.1.2"
__author__ = "Robert Singer"
__author_email__ = "robertgsinger@gmail.com"


class NotSet(object):
    pass


from .decorators import hook
from .hooks import *
from .mixins import LifecycleModelMixin
from .models import LifecycleModel
