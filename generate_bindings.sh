#! /bin/sh


h2xml -c -o xkb.xml X11/Xlib.h X11/Xlibint.h X11/XKBlib.h
# The python-ctypeslib packages contains a bug; firstly fix it with the patch
# from https://sourceforge.net/p/ctypes/mailman/message/25291919/
xml2py -k defst -o xkb.py -l X11 xkb.xml


# Stop interpreter from crying

# P.S. X.h has None and Xlib.h has True and False #defines
# To use them without overlapping with the Python keywords just add trailing
# underscores, like None_, True_ and False_

sed -i "s/^None /None_ /" xkb.py
sed -i "s/'None'/'None_'/" xkb.py
sed -i "s/^True /True_ /" xkb.py
sed -i "s/'True'/'True_'/" xkb.py
sed -i "s/^False /False_ /" xkb.py
sed -i "s/'False'/'False_'/" xkb.py
sed -i 's/\( = [0-9]\+\)L/\1/g' xkb.py


# Write this script's contents for reference

(echo '# -*- coding: utf-8 -*-'; echo;
 sed 's/\(.*\)/# \1/; s/# $/#/' "$0"; echo; cat xkb.py) > tmp
mv tmp xkbgroup/xkb.py
rm xkb.py
