How To Use Ravenc
=================

Ravenc has five tabs: source, subtitle, audio, video and format. The order 
of the tabs is that which is normally followed when ripping a DVD title.

Source tab
----------

This is where you choose which video title to copy. 
Ravenc will automatically detect DVDs when they are inserted and display 
them on the source tab. After 
a brief pause the DVD icon will expand to show all 
video titles on the DVD. Select the one you want to copy, typically 
this will be the longest title which is shown in bold text.

Alternatively you can choose a title from your filesystem.

Once you have selected the title you can see audio and subtitle data
in the lower panel.

Subtitle tab
------------

Here you choose the subtitles you want to transcode and the encoding type.
You can choose to encode more than one subtitle but please note that not 
all subtitle codecs can be accepted by the container
format you choose. Generally it is safer choosing the "copy" codec if 
you're not sure.

Audio tab
---------

This is where you choose which audio tracks you want to transcode. You
can choose more than one track.

You can choose which codec you want to use to transcode the audio. The 
encoders presented will be those that your installation of avlib is
able to use.

You can set the bit-rate of the audio encoding. The format you can use
in this field is decribed in 
`Expressions Evaluation <https://libav.org/avconv.html#Expression-Evaluation>`_. 
Next you can choose to re-sample the audio at a different sample rate. 
By choosing '0' or a blank field your are electing not to change the 
audio sample rate.
Please note that avconv will reject bit-rates that are set too low.

Video tab
---------

This is where you choose which video tracks you want to transcode. You
can choose more than one track but normal DVDs will normally present 
only one video track.

You can choose which codec you want to use to transcode the video. The 
encoders presented will be those that your installation of avlib is
able to use.

The "Config" button can be used to set up further encoder parameters. At
present only the h264 encoder has this facility.

You can set the bit-rate of the video encoding. The format you can use
in this field is decribed in 
`Expressions Evaluation <https://libav.org/avconv.html#Expression-Evaluation>`_.

Ravenc allows either one-pass or two-pass encoding:

Passes
^^^^^^

There are two types of encoding:

#. Single Pass

   The video is encoded in one pass. This is the fastest option
   but the encoder makes all its decisions in this pass hence
   it does not provide the best quality / size trade-off.

#. Two Pass

   The first pass is used to collect data about the source video which
   is then used to inform the second pass when the encoded video
   is produced. This provides for a better quality / size
   trade-off than single pass.

It is also possible to crop and scale the video:

If using the "copy" encoder then the number of passes is not relevant and 
cropping and scaling will not be posssible.

Cropping
^^^^^^^^

Cropping is the removal of black borders around the video. Many 
modern video titles have these borders. Encoding these will waste
many bits causing your encoded video to have larger file sizes and
lower quality. If your source video has these it's usually a good
idea to remove them.

Ravenc has a crop-detect option which will try to automatically 
detect these borders by taking a number of video samples. So should
be aware that this process is not infallable but usually provides
crop values you should use.

Scaling
^^^^^^^

Generally scaling is not recommended as it degrades the quality of 
the video. However, if you have cropped the video (good idea) you 
may also need to scale it. You can choose to lock the aspect ratio 
and just choose the width of the encoded video. In this case 
the height will be 
automatically calculated from the source aspect ratio. The width value 
is pre-selected by Ravenc to be the width of the source video and 
you can change this if you want.

Format tab
----------

Here you choose the container format for your file, you can also choose 
the output directory and the file-name. If you choose both then the 
selction made by radio button wil take precidence.

Output Directory and Filename
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can choose where you want to save the output files and the 
name of the video file itself. The following substitutions will be
made in both fields:

* %T - Title of the track
* %N - Number of the selected track (always 0 for a file)
* %L - Length of the selected track
* %f - The first letter of the title

Format Selection
^^^^^^^^^^^^^^^^

There are two ways to select the container format, you can do either 
of the following:

        * Select the container format from the list
        * Add a file extension to the file-name and avconv will
          guess the format

Please note that many formats can accept only a small sub-set of 
encoded media. If you are unsure about this then for video 
transcodes it's usually safe to choose either Matroska (mkv) or 
Audio Video Interleave (avi).

When ready to start the rip you can press the "Start" button.

Ripping
^^^^^^^

A window will open giving you the status of 
the encode job. This window can be docked to the bottom of the main 
Ravenc window.

As well as some data the window will show a progress bar and a 
quality bar. The quality bar attempts to give a visual 
representation of the video quality of the encoded video: if there is
more green than red then the video will be of a higher quality. However, 
having *less* green than red is not always a bad thing as this 
represents a video that is more compressed, so if having a small file
size is important to you then this is what you should see. Only if you see 
no green at all should you be concened about the video quality.

You affect the video quality by changing the bit-rate on the video tab.

If you want to abandon the rip you can press the "Stop" button; the rip 
will stop but the window will remain open. This allows you to 
examine any messages from avconv. To do this press the "More" button.

You can have more than one encode job going at once with Ravenc but 
be aware that if you have more than one job going on a single 
DVD drive then it's likely going to slow down the rip as the DVD 
drive hunts around for the data it needs.
