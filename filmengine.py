"""
whatiwant.filmengine
Lucas A. Gerber
"""


import moviepy.editor as mpy
import random, string
from .tools import verbosePrint, numGen, createDestination, collectFiles, yesInput
from .config import OUT_DIREC, TXT_DIREC, FIRST_CLIP
import whatiwant.mimic as mimicry
import whatiwant.director as director


def randomFilm ( path_s,
                 first_clip_option=False,
                 result_path=None,
                 result_name=None,
                 text_overlays_on=True,
                 text_path_s=None,
                 text_overlays_num=None,
                 text_method_s=['twitter','lecture','poem'], #,'translate'
                 text_interval=(1,30),
                 fontsize_interval=(50,300),
                 duration_end=None,
                 duration_interval=(1, 600),
                 clip_interval=(1, 30),
                 accepted_fps=None,
                 accepted_input_types = ['avi', 'mp4', 'MTS', 'mov','dv','mpg'],
                 output_type = 'mp4',
                 output_codec='libx264',
                 verbose=True):
    """

    Returns none.  Outputs a random film given a folder with video files.

    DEFAULTS:
    path_s >>> (str/list) directory of video file(s) to be compiled into output file
    first_clip_option >>> (T/F) True, first clip will be FIRST_CLIP imported above
    result_path >>> (str) OUT_DIREC directory imported above, directory of output file
    result_name >>> (str) randomly generated from text files, name of output file
    text_overlays_on >>> (T/F) True, overlays are on
    text_path_s >>> (str/list) TXT_DIREC directory imported above, directory of text file(s) for overlays
    text_overlays_num >>> (int) random.randint(1,1+int(duration_end/8)), number of text overlays
    text_method >>> (str/list) 'twitter', 'lecture', 'poem', 'translate', method(s) of generating text overlays
    text_interval >>> (tuple) (1,30), range of duration interval for text overlays
    fontsize_interval >>> (tuple) (50,300), range of font size for text overlays
    duration_end >>> (int) random selection from duration interval, duration of output film
    duration_interval >>> (tuple) (1, 600), range of duration interval for output film
    clip_interval >>> (tuple) (1, 30), range of duration interval for clips for output film
    accepted_fps >>> (int) all framerates, specifies a framerate for clips to be accepted for the film
    accepted_input_types >>> (list) ['avi', 'mp4', 'MTS', 'mov','dv','mpg'], list of accepted input file types
    output_type >>> (str) 'mp4', output file type
    output_codec >>> (str) 'libx264', output file codec
    
    """
    global OUT_DIREC, TXT_DIREC, FIRST_CLIP
    
    if not result_path:
        result_path = OUT_DIREC # use OUT_DIREC if no directory is provided

    if not text_path_s:
        text_path_s = TXT_DIREC # use TXT_DIREC if no directory is provided
        
    text_name_list = collectFiles(text_path_s, 'txt')
    
    clip_name_list = collectFiles(path_s, accepted_input_types, weighted=True)
    
    if not duration_end:
        duration_end = random.randint(duration_interval[0], duration_interval[1])
    verbosePrint(verbose, 'Duration of output film: ' + str(duration_end))

    if not text_overlays_on:
        text_overlays_num = 0
    elif not text_overlays_num:
        text_overlays_num = random.randint(1,1+int(duration_end/8))

    if first_clip_option:
        first_clip_name = FIRST_CLIP
    else:
        first_clip_name = None

    tarkovsky = director.Director(first_clip_name, duration_end, text_overlays_num, text_name_list, clip_name_list, clip_interval, text_interval)


    while tarkovsky.getCurrDuration('clip') < duration_end:
        adj_clip_name_list, adj_clip_low, adj_clip_high = tarkovsky.adjustParams('clip')
        new_clip, new_clip_start, new_clip_name = generateClip(adj_clip_name_list, duration=random.randint(adj_clip_low, adj_clip_high),
                                               accepted_fps=accepted_fps, verbose=verbose)
        tarkovsky.addClip('clip', new_clip, new_clip_start, new_clip_name, (adj_clip_low, adj_clip_high))

        verbosePrint(verbose, 'Current duration of film: ' + str(tarkovsky.getCurrDuration('clip')))

    output_clip = mpy.concatenate_videoclips([ clip for clip in tarkovsky.outclip_df['clip_object'] if clip ])
    verbosePrint(verbose, 'Clips concatenated...')


    if text_overlays_on:
            
        verbosePrint(verbose, 'Number of text overlays: ' + str(text_overlays_num))
        
        while tarkovsky.getCurrDuration('text') < text_overlays_num:
            adj_text_name_list, adj_text_low, adj_text_high = tarkovsky.adjustParams('text')
            text_clip, text_clip_name = generateTextOverlay(adj_text_name_list, text_method_s=text_method_s,
                                                            duration=random.randint(adj_text_low, adj_text_high),
                                                            fontsize=random.randint(fontsize_interval[0],fontsize_interval[1]), verbose=verbose)
            if text_clip:
                text_clip_start = random.randint(1, max(int(duration_end - text_clip.duration), 1))
                verbosePrint(verbose, 'Text overlay will start at: ' + str(text_clip_start))
                text_clip = text_clip.set_start(text_clip_start)
            else:
                text_clip_start = 0

            tarkovsky.addClip('text', text_clip, text_clip_start, text_clip_name, (adj_text_low, adj_text_high))

        text_clip_list = [ clip for clip in tarkovsky.outtext_df['clip_object'] if clip ]
        text_clip_list.insert(0, output_clip)
        output_clip = mpy.CompositeVideoClip(text_clip_list)
        verbosePrint(verbose, 'Text overlays added...')


    if output_clip.duration > duration_end:
        output_clip = output_clip.subclip(0, duration_end)
        verbosePrint(verbose, 'Film cut to duration end')

        
    try:
        verbosePrint(verbose, 'Output film framerate: ' + str(output_clip.fps))
    except AttributeError:
        verbosePrint(verbose, 'ERROR: the framerates of the clips did not all match, changed fps to 25')
        output_clip = output_clip.set_fps(25)


    if not result_name:
        result_name = generateTitle(text_name_list, verbose)

    destination, log_destination = createDestination(result_path, output_name=result_name, output_type=output_type)

    tarkovsky.writeLog(log_destination)
    verbosePrint(verbose, 'Log file written to destination, ' + log_destination)

    if yesInput('>>Would you like to write this film?\n'):
        output_clip.write_videofile(destination, fps=output_clip.fps, codec=output_codec)
        verbosePrint(verbose, 'Video file written to destination, ' + destination)


def generateClip(clip_name_list, duration=None, accepted_fps=None, verbose=True):
    """

    Returns random VideoFileClip given a list of fully-specified names of clips.
    
    """

    verbosePrint(verbose, 'Generating new clip...')
    clip_name = random.choice(clip_name_list)
    try:
        verbosePrint(verbose, 'New clip name: ' + clip_name)
    except:
        verbosePrint(verbose, 'New clip name had "charmap_error"')
        
    clip_audio_flag = random.randint(0,3) > 0
    clip = mpy.VideoFileClip(filename=clip_name, audio=clip_audio_flag)

    clip_start = random.randint(0, int(clip.duration))

    if not duration:
        clip_end = random.randint(clip_start, int(clip.duration))
    else:
        clip_end = min(clip_start+duration, clip.duration)

    clip_volume = random.randint(0,15) / 10.0

    clip = clip.subclip(clip_start, clip_end)
    clip = clip.volumex(clip_volume)

    verbosePrint(verbose, 'New clip fps as integer: ' + str(int(clip.fps)))
    if clip.duration > 0 and (int(clip.fps) == accepted_fps or not accepted_fps):
        verbosePrint(verbose, 'New clip duration: ' + str(clip.duration))
        verbosePrint(verbose, 'New clip was returned')
        return clip, clip_start, clip_name
    else:
        verbosePrint(verbose, 'None was returned')
        return None, clip_start, clip_name


def generateTextOverlay(text_name_list, text_method_s=None, duration=None, fontsize=None, verbose=True):
    """

    Returns random TextClip given fully-specified names of textfiles, and the method(s) for creating the text.

    ACCEPTED METHODS:  'twitter', 'lecture', 'poem', 'translate'
    
    """
    
    verbosePrint(verbose, 'Generating new text overlay...')
    if not duration:
        duration = random.randint(1, 10)

    if not fontsize:
        fontsize = random.randint(50, 100)

    text_name = random.choice(text_name_list)

    mimic = mimicry.Mimic(text_name, verbose=verbose)

    if not text_method_s:
        text_method_s = 'twitter'
    elif type(text_method_s) is list:
        text_method = random.choice(text_method_s)
    else:
        text_method = text_method_s
    
    if text_method == 'twitter':
        text_for_clip = mimic.tweet()
    elif text_method == 'lecture':
        text_for_clip = mimic.lecture(limit=random.randint(1,15))
    elif text_method == 'poem':
        text_for_clip = mimic.poem(limit=random.randint(1,15))
    elif text_method == 'translate':
        text_for_clip = mimic.translate(limit=random.randint(1,15))
    
    text_clip = mpy.TextClip(text_for_clip, fontsize=fontsize, font='Ubuntu-Regular', color='white')
    text_clip = text_clip.set_pos('center').set_duration(duration)

    if text_clip.duration > 0:
        verbosePrint(verbose, 'New text overlay duration: ' + str(text_clip.duration))
        verbosePrint(verbose, 'New text overlay was returned')
        return text_clip, text_name
    else:
        verbosePrint(verbose, 'None was returned')
        return None, text_name


def generateTitle(text_name_list, verbose=True):
    """

    Returns random title as string given fully-specified names of textfiles.
    
    """
    
    verbosePrint(verbose, 'Generating title...')

    text_name = random.choice(text_name_list)
    title = ''

    while not title:
        mimic = mimicry.Mimic(text_name, verbose=verbose)
        delete_strings = string.punctuation + '\t\n\r'
        start_word = random.choice(list(mimic.get_mimic_dict().keys()))
        title = mimic.poem(starting_word=start_word, limit=1)

        for char in list(delete_strings):
            title = title.replace(char, '')

        title = title.replace(' ', '_')

    return title
    

def main():
    pass


if __name__ == '__main__':
    main()
