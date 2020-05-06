"""



0900 to 1700 
ashley roland
november 2019



"""


import subprocess
from math import floor

breaks = [8,16,17,24]

def getFileName(chunk):
	"""

	Take a timechunk and return a properly-formatted file string

	Chunk 0 : 0900 - 0915.flac
	Chunk 1 : 0915 - 0930.flac
	...
	etc.

	"""

	# Calculate start time
	timeA = (floor(chunk / 4) * 100) + ((chunk * 15) % 60) + 900

	# End time is just next index value, increase and recalc
	timeB = (floor((chunk + 1) / 4) * 100) + (((chunk + 1) * 15) % 60) + 900

	# Convert to string
	timeA = "%d" % timeA
	timeB = "%d" % timeB

	# If output times are only three digits long, left-pad a 0
	if len(timeA) == 3:
		timeA = "0%s" % timeA
	if len(timeB) == 3:
		timeB = "0%s" % timeB

	# Format output filename. Check for special cases -- breaks
	if chunk in breaks:
		if chunk == 8:
			return "%s to %s (First Paid Rest Break).flac" % (timeA, timeB)
		elif chunk == 24:
			return "%s to %s (Second Paid Rest Break).flac" % (timeA, timeB)
		else:
			return "%s to %s (Unpaid Meal Break).flac" % (timeA, timeB)
	return "%s to %s.flac" % (timeA, timeB)
	


if __name__ == "__main__":

	prefix = "/full/path/to/"
	infile = prefix + "timestretched.ogg"

	chunk_dur = 900 # there are nine-hundred seconds in fifteen minutes.
	chunks = 32 # there are thirty-two fiteen-minute chunks in an eight-hour work day

	for i in range(chunks): 
		filename = getFileName(i)

		# Set metadata.
		# I really, really do not like this from a legibility standpoint
		# but subprocess.run *really* wants one long list of arguments. 
		# Meanwhile ffmpeg expects each piece of metadata to be declared 
		# with a metadata flag so ¯\_(ツ)_/¯
		metadata = []
		md_title = ["-metadata", "title=%s" % filename]
		md_track = ["-metadata", "track=%s/%s" % (str(i+1), chunks)]
		md_album = ["-metadata", "album=0900 to 1700"]
		md_artist = ["-metadata", "artist=Ashley Roland"]
		md_albumartist = ["-metadata", "album_artist=Ashley Roland"]
		md_comments = ["-metadata", "comments=ilu dolly pls don't sue"]
		metadata += md_title
		metadata += md_track
		metadata += md_album
		metadata += md_artist
		metadata += md_albumartist
		metadata += md_comments

		# Prep ffmpeg command
		ffcmd = ["ffmpeg"]

		# are we at a break time? if so, encode silence
		if i in breaks:
			# ffcmd = "ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t %s %s" % (chunk_dur, filename)
			ffcmd += [ "-f",
				"lavfi",
				"-i",
				"anullsrc=channel_layout=stereo:sample_rate=44100",
				"-t",
				str(chunk_dur),
				"-v",
				"quiet"
			]
			ffcmd += metadata
			ffcmd += ["%s/%s" % (prefix, filename)]
		else:
			starttime = 0
			
			# Because we are using the chunk pointer to keep track of breaks,
			# and because breaks are a separate operation, we need to occasionally 
			# realign our 'read head position' to the previous chunk in the sourcefile. 
			# Otherwise we will skip regions of audio. 

			if i < 8:
				starttime = i * chunk_dur
			elif i > 8 and i < 16:
				starttime = (i - 1) * chunk_dur
			elif i > 17 and i < 24:
				starttime = (i - 3) * chunk_dur
			elif i > 24:
				starttime = (i - 4) * chunk_dur

			# ffmpeg must re-encode in order to write valid track length metadata,
			# otherwise bandcamp uploads fail
			# ffcmd = "ffmpeg -i \"%s\" -ss %d -t %d %s \"%s/%s\"" % (infile, starttime, chunk_dur, metadata, prefix, filename)
			ffcmd += [
				"-i",
				infile,
				"-ss",
				str(starttime),
				"-t",
				str(chunk_dur),
				"-v",
				"quiet"
			]
			ffcmd += metadata
			ffcmd += ["%s/%s" % (prefix, filename)]
		
		subprocess.run(ffcmd)

	print("Done!")