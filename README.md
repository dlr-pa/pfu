# README: pfu -- Python File Utilities

## intro

'pfu' is an acronym for Python File Utilities.

At the moment it combines a few tools described quickly in the next subsections.
'pfu' is designed to work on each platform supported by
[Python](https://www.python.org/) (python3).

Using [checksums](https://en.wikipedia.org/wiki/Checksum)
for data exchange helps to verify the
[data integrity](https://en.wikipedia.org/wiki/Data_integrity).

The command line program(s) provide help output by using the common flag '-h'.

You can find more information on the web:

* [source code of pfu](https://gitlab.com/dlr-pa/pfu)

### pfu create_checksum

This command will create (missing) checksums in a directory tree.
The checksums can be stored for each file, in each directory or in one file.
Also you can choose different codings (e. g. base16 or base64).

For example, it is compatible with the format produced by
sha256sum (GNU version) and sha256 (BSD version).

Further it is compatible with the checksum format used in
PK-4 [^a] [^b] and was/is used in this project.

[^a]: https://en.wikipedia.org/wiki/PK-4_(ISS_experiment)
[^b]: https://doi.org/10.1063/1.4962696

In the projects PlasmaLab/Ekoplasma [^c] [^d] and COMPACT [^e] [^f]
it was used and developed in python2.

[^c]: https://complex-plasmas.dlr.de/index.php/plasmalab.html
[^d]: https://dx.doi.org/10.1063/1.5020392
[^e]: https://sciences.ucf.edu/physics/microgravity/iss-compact/
[^f]: https://doi.org/10.1063/5.0062165

### pfu check_checksum

This command will check checksums. We assume relative paths in each hash file.

It can detect the used format and/or coding and supports the following
formats (and more):

* sha256sum (GNU version)
* sha256 (BSD version)
* format used in PK-4
* format used in PlasmaLab/Ekoplasma and COMPACT

### pfu simscrub

This script read every file in the given directory tree.

If you do this regularly (e. g. via crontab every month) you can
simulate a scrubbing and give the file system or storage device
(e. g. firmware of SSD) the chance to detect error and to fix them.

### pfu speed_test

This script tries to measure the read and write speed of a storage.

It works on top of a file system and therefore measures the complete storage
system. To get a significant measure you should read and write more data
than the system could buffer in the main memory.

### pfu replicate

This is the command to copy/replicate data/files from one directory to other
directories (one or more). In parallel to copying it creates checksums and
checks the checksums in the target directories after copying. It uses the
command line programs e. g. "rsync" and "sha256sum". Although we use by
default rsync, the source and destination paths have to be local. If copy is
done by "rsync" and this script is run on a windows system, the drive letters
will be replaced by "/cygdrive/[drive letter]/".

It was used and developed in the project PlasmaLab/Ekoplasma [^c] [^d] [^f].

It was used 2015 and 2016 on the parabolic flight campaigns of PlasmaLab.

## history

'pfu' is a software combining:

* simscrub.py
* plecs_replicate.py
* pk4_checksums.py

The project simscrub.py is a private project of Daniel Mohr under the GPL.
(This is already integrated.)

The project pk4_checksums.py is also licensed by Daniel Mohr under the GPL.
(This is already integrated.)

'plecs_replicate.py' is a part of plecs, which is under the GPL. This part
has the only author Daniel Mohr.
(This is partly already integrated. The other part is not necessary.)

'pfu' was used and developed in python2. But 2021 it was ported to python3.

## install

see [INSTALL](INSTALL.md)

## copyright + license

Author: Daniel Mohr.

Date: 2023-04-20 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007

Copyright (C) 2015-2023 Daniel Mohr and
Deutsches Zentrum fuer Luft- und Raumfahrt e. V., D-51170 Koeln

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation; either version 3 of
 the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy (see [LICENSE.txt](LICENSE.txt)) of the
 GNU General Public License along with this program.
 If not, see <http://www.gnu.org/licenses/>.

### Contact Informations

* Daniel Mohr, daniel.mohr@dlr.de

### Territory

This license applies to all components/files of the software.
