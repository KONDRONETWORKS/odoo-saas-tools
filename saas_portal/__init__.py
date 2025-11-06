from . import controllers
from . import models
from . import wizard
from . import hooks

# Exporter la fonction post_init_hook pour qu'elle soit accessible
from .hooks import post_init_hook
