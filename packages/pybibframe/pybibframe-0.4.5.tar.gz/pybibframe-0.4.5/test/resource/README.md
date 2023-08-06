# Test files

Thanks to alumni of Zepheira's BIBFRAME training <http://zepheira.com/solutions/library/training/> for the following:

George Washington University Libraries (GW_bf_test10.mrx)

----

lcc-u.mrx - Downloaded from [this LC record](http://catalog2.loc.gov/cgi-bin/Pwebrecon.cgi?v1=1&ti=1,1&Search_Arg=ogbuji&Search_Code=GKEY%5E%2A&CNT=100&type=quick&PID=oYjcPLW0bI3X2GzwJr6jJF3VSR9&SEQ=20141018081442&SID=1) based on an [LC catalogue search for Ogbuji](http://catalog2.loc.gov/cgi-bin/Pwebrecon.cgi?DB=local&Search_Arg=ogbuji&Search_Code=GKEY%5E*&CNT=100&hist=1&type=quick), then converted to MARC/XML as follows:

    yaz-marcdump -i marc -o marcxml -t UTF-8 /tmp/record.mrc > /tmp/record.mrx

TODO: Go back to get non Unicode version when LC.gov is not timing out.

