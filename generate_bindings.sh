#! /bin/sh


h2xml -c -o xkb.xml X11/Xlib.h X11/Xlibint.h X11/XKBlib.h
# The python-ctypeslib packages contains a bug; firstly fix it with the patch
# from https://sourceforge.net/p/ctypes/mailman/message/25291919/
xml2py -k defst -o xkb.py -l X11 xkb.xml


# Stop interpreter from crying

# P.S. X.h has None and Xlib.h has True and False #defines
# To use them without overlapping with the Python keywords just add underscore
# before, like _None, _True and _False

sed -i "s/^None /_None /" xkb.py
sed -i "s/'None'/'_None'/" xkb.py
sed -i "s/^True /_True /" xkb.py
sed -i "s/'True'/'_True'/" xkb.py
sed -i "s/^False /_False /" xkb.py
sed -i "s/'False'/'_False'/" xkb.py
sed -i 's/\( = [0-9]\+\)L/\1/g' xkb.py


# Write this script's contents for reference

(sed 's/\(.*\)/# \1/; s/# $/#/' "$0"; echo; cat xkb.py) > tmp
mv tmp xkbgroup/xkb.py
rm xkb.py
