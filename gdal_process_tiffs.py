#!/usr/bin/python

import sys, os, subprocess

# sudo id tomcat8
#   uid=112(tomcat8) gid=119(tomcat8) groups=119(tomcat8)
uid = 112
gid = 119

proc_ext = '.out'
old_ext = '.org'
autoclean = False

if len(sys.argv) < 4:
    print 'Usage: python gdal_process_tiffs.py <input_dir> <uid> <gid>'
    print ' - to get <uid> <gid> use command "id <username>"'
    print ' - optional args:'
    print '     autoclean      Will automatically delete "' + old_ext + '" files'
    sys.exit()
else:
    inputdir = sys.argv[1]
    uid = int(sys.argv[2])
    gid = int(sys.argv[3])

if len(sys.argv) == 5 and sys.argv[4] == 'autoclean':
    autoclean = True
    print 'autoclean avtivated'

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk(inputdir):
    path = root.split(os.sep)
    # print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        # print(len(path) * '---', file)
        filename, fileext = os.path.splitext(file)
        if "tif" in fileext:

            # gdal_translate -co COMPRESS=DEFLATE -co TILED=YES <src> <trg>
            base_name = os.path.join(root, filename)
            src_file = "%s%s" % (base_name, fileext)
            org_file = "%s%s" % (base_name, ("%s%s" % (fileext, old_ext)))
            trg_file = "%s%s" % (base_name, ("%s%s" % (fileext, proc_ext)))

            gdal_translate_cmd = ['gdal_translate',
                                  '-co',
                                  'COMPRESS=DEFLATE',
                                  '-co',
                                  'TILED=YES',
                                  src_file,
                                  trg_file
                                 ]

            print 'Now processing: ' + src_file # + ' --> ' + trg_file
            subprocess.call(gdal_translate_cmd)

            if not os.path.exists(org_file):
                os.rename(src_file, org_file)

            if not os.path.exists(src_file):
                os.rename(trg_file, src_file)
                os.chown(src_file, uid, gid)

            if os.path.exists(org_file):

                # gdaladdo --config COMPRESS_OVERVIEW DEFLATE -r average <src> 2 4 8 16
                gdal_addo_cmd = ['gdaladdo',
                                 '--config',
                                 'COMPRESS_OVERVIEW',
                                 'DEFLATE',
                                 '-r',
                                 'average',
                                 src_file,
                                 '2', '4', '8', '16'
                                ]

                print 'Adding internal overviews: ' + src_file
                subprocess.call(gdal_addo_cmd)

                if autoclean:
                    print 'Deleting: ' + org_file
                    os.remove(org_file)

                    if os.path.exists(org_file):
                        print '[ERROR] - Could not delete: ' + org_file
