from guardian.shortcuts import get_objects_for_user
from geonode.people.models import Profile
from geonode.layers.models import Layer

profiles = Profile.objects.filter(is_superuser=False)
authorized = list(get_objects_for_user(profiles[0], 'base.view_resourcebase').values('id'))
layers = Layer.objects.filter(id__in= [d['id'] for d in authorized])
protected_layers = Layer.objects.all().exclude(id__in= [d['id'] for d in authorized])
for index, layer in enumerate(protected_layers):
    print "[%s / %s] Deleting Layer [%s] ..." % ((index + 1), len(protected_layers), layer.name)
    try:
        layer.delete()
    except:
        print "[ERROR] Layer [%s] couldn't be deleted" % (layer.name)

