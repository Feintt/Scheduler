from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

# Register your models here.

# This app is running on docker, so we need to unregister and then register the models,
# otherwise we get an error each time we try to run the server saying that the models
# are already registered.
try:
    # This is an example of how to unregister a model
    # admin.site.unregister(User)
    pass
except NotRegistered:
    pass

# After unregistering the models, we can register them again
# admin.site.register(User)
