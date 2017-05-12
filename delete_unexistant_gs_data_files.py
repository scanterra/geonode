import os, shutil
from guardian.shortcuts import get_objects_for_user
from geonode.people.models import Profile
from geonode.layers.models import Layer

profiles = Profile.objects.filter(is_superuser=False)
authorized = list(get_objects_for_user(profiles[0], 'base.view_resourcebase').values('id'))
layers = [l.name for l in Layer.objects.filter(id__in=[d['id'] for d in authorized])]

folder = '/data/geoserver-data/data/geonode/'

for the_file in os.listdir(folder):
    file_path = os.path.join(folder, the_file)
    try:
        if os.path.isdir(file_path):
            dir_name = os.path.basename(file_path)
            if not dir_name in layers:
                print "Purging Folder [%s] ..." % (dir_name)
                shutil.rmtree(file_path)
            else:
                print "Preserving Folder [%s] ..." % (dir_name)
    except Exception as e:
        print(e)

