TimeDiff and TimeDiffPlot
=========================

This repository contains two programs, TimeDiff and TimeDiffPlot. Both take log-files in the form of streams as input. TimeDiff then outputs the difference in time between log entries, TimeDiffPlot uses Matplotlib, Numpy and Scipy to graph the differences in the log-files. Both allow any syntax for the time through python [datetime.strftime() and datetime.strptime()](https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior "Syntax for entering time formats"). Formatting presets for bothes time-diff and time-diff-plot can be set in /etc/timediff/timediff.json.

TimeDiffPlot requires Matplotlib, Numpy and Scipy.

TimeDiff and TimeDiffPlot are both written in python 2.7 and compatile with Mac OSX and Linux.

TimeDiff 0.9.37

Installing TimeDiff
===================

TimeDiff can be installed through pip by calling

    # pip install timediff

Running TimeDiff
================

TimeDiff can be run by calling

    $ cat <file_to_parse> | ./<path_to_TimeDiff>/time_diff/bin/time-diff <arguments>

You may also want to pipe in data from grep

    $ grep <data_to_grep> <grep's_args> | ./<path_to_TimeDiff>/time_diff/bin/time-diff <arguments>

TimeDiff will then output the following

    <difference_from_time_of_first_line> <difference_from_time_of_previous_line> <line_processed>

Example of of running TimeDiff
------------------------------

Command entered:

    $ cat /var/log/messages | ./time_diff/bin/time-diff -F linux1
    
Output:

    
             0 s          0 s : Oct  7 10:17:21 zaphod kernel: [ 2801.031111] scsi6 : usb-storage 1-2:1.0
     
             0 s          0 s : Oct  7 10:17:21 zaphod kernel: [ 2801.031328] usbcore: registered new interface driver usb-storage
     
             0 s          0 s : Oct  7 10:17:21 zaphod kernel: [ 2801.031334] USB Mass Storage support registered.
     
             1 s          1 s : Oct  7 10:17:22 zaphod kernel: [ 2802.102076] scsi 6:0:0:0: Direct-Access     Kingston DT 101 G2        PMAP PQ: 0 ANSI: 0 CCS
     
             1 s          0 s : Oct  7 10:17:22 zaphod kernel: [ 2802.104902] sd 6:0:0:0: Attached scsi generic sg1 type 0
     
             3 s          2 s : Oct  7 10:17:24 zaphod kernel: [ 2803.969196] sd 6:0:0:0: [sdb] 15495168 512-byte logical blocks: (7.93 GB/7.38 GiB)
     
             3 s          0 s : Oct  7 10:17:24 zaphod kernel: [ 2803.973449] sd 6:0:0:0: [sdb] Write Protect is off
     
             3 s          0 s : Oct  7 10:17:24 zaphod kernel: [ 2804.031763]  sdb: sdb1
     
             3 s          0 s : Oct  7 10:17:24 zaphod kernel: [ 2804.045140] sd 6:0:0:0: [sdb] Attached SCSI removable disk
     
             4 s          1 s : Oct  7 10:17:25 zaphod kernel: [ 2804.831579] FAT-fs (sdb1): utf8 is not a recommended IO charset for FAT filesystems, filesystem will be case sensitive!


Usage of TimeDiff
-----------------

    usage: time-diff [-h] [--format [FORMAT]] [--format-preset [{linux1,custom1}]]
                 [--locale [LOCALE]] [--verbose] [--cancel-padding]
                 [--round-to {s,ms,min,h,d}]

    Calculate differences in time of log entries and output them into the console.

    optional arguments:
    -h, --help            show this help message and exit
    --format [FORMAT], -f [FORMAT]
                        Sets datetime format options, defaults to
                        "%Y%m%d_%H%M%S" overrides given presets.
    --format-preset [{linux1,custom1}], -F [{linux1,custom1}]
                        Set datetime formatting preset, defaults to custom1.
                        Values are: linux1 -> %b %d %H:%M:%S, custom1 ->
                        %Y%m%d_%H%M%S
    --locale [LOCALE], -l [LOCALE]
                        Sets locale to be used with parsing month and weekday
                        names, defaults to American English (en_US).
    --verbose, -v         Sets program to verbose mode. This will result in
                        loger descriptions of errors being written to the
                        stderr.
    --cancel-padding, -p  Cancels adding zero-padding, eg. without -p 2 would
                        become 02.
    --round-to {s,ms,min,h,d}, -r {s,ms,min,h,d}
                        Sets what time-unit to round to while doing
                        formatting.

Running TimeDiffPlot
====================

TimeDiffPlot can be run by calling

    $ cat <file_to_parse> | ./<path_to_TimeDiff>/time_diff/bin/time-diff-plot <arguments>

You may also want to pipe in data from grep

    $ grep <data_to_grep> <grep's_args> | ./<path_to_TimeDiff>/time_diff/bin/time-diff-plot <arguments>

TimeDiffPlot outputs nothing. Using TimeDiffPlot with logs of over 50 000 lines may take some time.

Usage of TimeDiffPlot
---------------------

    usage: time-diff-plot [-h] [--format [FORMAT]]
                          [--format-preset [{linux1,custom1}]] [--locale [LOCALE]]
                          [--verbose] [--cancel-padding] [--logarithmic]

    Calculate differences in time of log entries and output them into the console.

    optional arguments:
      -h, --help            show this help message and exit
      --format [FORMAT], -f [FORMAT]
                            Sets datetime format options, overrides given presets.
      --format-preset [{linux1,custom1}], -F [{linux1,custom1}]
                            Set datetime formatting preset, defaults to custom1.
                            Values are: linux1 -> %b %d %H:%M:%S, custom1 ->
                            %Y%m%d_%H%M%S
      --locale [LOCALE], -l [LOCALE]
                            Sets locale to be used with parsing month and weekday
                            names, defaults to American English (en_US).
      --verbose, -v         Sets program to verbose mode. This will result in
                            loger descriptions of errors being written to the
                            stderr.
      --cancel-padding, -p  Cancels adding zero-padding, eg. without -p 2 would
                            become 02.
      --logarithmic, -L     Sets y-axis of plots to be on a logarithmic scale


