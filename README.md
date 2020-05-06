# 0900 to 1700
    a twitch stream / ambient noise record
    ashley roland
    december 2019

## what

Dolly's smash-hit, media-crossover moment, but time-stretched to fit the duration of an eight-hour work day. [listen on bandcamp](https://xxylecomputer.bandcamp.com/https://xxylecomputer.bandcamp.com/album/0900-to-1700).

Some caveats:

Oregon law requires an employer-paid rest period of not less than 10 minutes for every segment of four hours or major part thereof (two hours and one minute through four hours) worked in one work period.  This time must be taken in addition to and separately from required meal periods. The rest period should be taken as nearly as possible in the middle of the work segment.  It is prohibited for an employer to allow employees to add the rest period to a meal period or to deduct rest periods from the beginning or end of the employee’s work shift.

Furthermore, Meal periods of not less than 30 minutes must be provided to non-exempt employees who work 6 or more hours in one work period.  No meal period is required if the work period is less than 6 hours.  Additional meal periods are required to be provided to employees who work 14 hours or more. Ordinarily, employees are required to be relieved of all duties during the meal period.  Under exceptional circumstances, however, the law allows an employee to perform duties during a meal period.  When that happens, the employer must pay the employee for the whole meal period.


## wait what

we're wrapping ffmpeg in python to output a series of flacs with a runtime of precisely eight hours, with allocated breaks throughout. 

this script assumes python 3.5+ and that you have a seven-hour long audio file sitting on the disk. i recommend [Paul's Extreme Sound Stretch](http://hypermammut.sourceforge.net/paulstretch/) for that sort of work. export to OGG to avoid the WAV container 4gb cap.

you must have a recent version of ffmpeg sitting on your $PATH.

change lines 61 and 62 to reflect the full path to your audio and the file itself. save and invoke on the command line with `python 0900to1700.py`. this will start a long list of encoding tasks, and the subprocess module buffers all output including print statments, so you won't see anything happen for a while. grab a coffee, pull up youtube, do what you gotta do. 

the output will appear in the path you specified, as a series of 32 FLAC files. congratulations! now get to work

### license
GPLv3. lmk if u use this. trans rights are human rights.