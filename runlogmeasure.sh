#!/bin/bash

buildozer android_new adb -- logcat -c
buildozer android_new run
buildozer android_new adb -- logcat -v time | tee /tmp/ee.log | awk '
    function tdi(a,b) {
        split(a, ary, /[:\.]/);
        asec = 3600*ary[1]+60*ary[2]+ary[3];
        split(b, bry, /[:\.]/);
        bsec = 3600*bry[1]+60*bry[2]+bry[3];
        return bsec - asec;
    };
    /KivEnt.*We will need.*for game/ {S=$2;print "start "$2;}
    /WIN DEATH.*PythonActivity/ {print "end "$2" duration="tdi(S,$2);exit;}
'

