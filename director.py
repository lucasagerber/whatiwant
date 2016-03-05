"""
whatiwant.director
Lucas A. Gerber
"""


import pandas as pd


class Director(object):

    def __init__(self, first_clip_name, duration_end, text_overlays_num, text_name_list, clip_name_list, clip_interval, text_interval):

        self.first_clip_name = first_clip_name
        self.duration_current = 0
        self.overlays_current = 0
        self.clip_name_list = clip_name_list
        self.text_name_list = text_name_list

        self.outclip_df = pd.DataFrame([['Starting_params',0,duration_end,clip_interval,None]], columns=['clip_name','clip_start','clip_duration','clip_interval','clip_object'])
        self.outtext_df = pd.DataFrame([['Starting_params',0,text_overlays_num,text_interval,None]], columns=['clip_name','clip_start','clip_duration','clip_interval','clip_object'])

    def getEndDuration(self):
        return self.outclip_df.loc[self.outclip_df['clip_name']=='Starting_params', 'clip_duration']

    def getInterval(self, type_):
        assert type_ == 'clip' or type_ == 'text', 'ERROR: type_ must be either "clip" or "text".'
        if type_ == 'clip':
            return self.outclip_df.loc[self.outclip_df['clip_name']=='Starting_params', 'clip_interval'][0]
        elif type_ == 'text':
            return self.outtext_df.loc[self.outtext_df['clip_name']=='Starting_params', 'clip_interval'][0]
     
    def getNameList(self, type_):
        assert type_ == 'clip' or type_ == 'text', 'ERROR: type_ must be either "clip" or "text".'
        if type_ == 'clip':
            return self.clip_name_list
        elif type_ == 'text':
            return self.text_name_list

    def getDf(self, type_):
        assert type_ == 'clip' or type_ == 'text', 'ERROR: type_ must be either "clip" or "text".'
        if type_ == 'clip':
            return self.outclip_df
        elif type_ == 'text':
            return self.outtext_df

    def getCurrDuration(self, type_):
        assert type_ == 'clip' or type_ == 'text', 'ERROR: type_ must be either "clip" or "text".'
        if type_ == 'clip':
            return self.duration_current
        elif type_ == 'text':
            return self.overlays_current

    def addCurrDuration(self, type_, value):
        assert type_ == 'clip' or type_ == 'text', 'ERROR: type_ must be either "clip" or "text".'
        if type_ == 'clip':
            self.duration_current += value
        elif type_ == 'text':
            self.overlays_current += 1
            
    def addRowDf(self, type_, new_row):
        assert type_ == 'clip' or type_ == 'text', 'ERROR: type_ must be either "clip" or "text".'
        if type_ == 'clip':
            self.outclip_df = self.outclip_df.append(new_row, ignore_index=True)
        elif type_ == 'text':
            self.outtext_df = self.outtext_df.append(new_row, ignore_index=True)

    def addClip(self, type_, clip, clip_start, clip_name, clip_interval):           
        if clip:
            self.addCurrDuration(type_, clip.duration)
            new_clip_row = pd.DataFrame([[clip_name,clip_start,clip.duration,clip_interval,clip]], columns=['clip_name','clip_start','clip_duration','clip_interval','clip_object'])
        else:
            new_clip_row = pd.DataFrame([[clip_name,clip_start,0,clip_interval,None]], columns=['clip_name','clip_start','clip_duration','clip_interval','clip_object'])

        self.addRowDf(type_, new_clip_row)
       
    def adjustParams(self, type_):
        df, clip_interval, clip_name_list = self.getDf(type_), self.getInterval(type_), self.getNameList(type_)
            
        adj_clip_interval = adj_fork_interval(df, clip_interval)
        adj_clip_name_list = adj_fork_name(df, clip_name_list)

        if type_ == 'clip':
            adj_clip_name_list = adj_first_clip_name(df, adj_clip_name_list, self.first_clip_name)
        
        return adj_clip_name_list, adj_clip_interval[0], adj_clip_interval[1]

    def writeLog(self, log_destination):
        log_file = self.outclip_df.append(self.outtext_df)[['clip_name','clip_start','clip_duration','clip_interval']]
        log_file.to_csv(log_destination)



def adj_fork_interval(clip_df, clip_interval):
    if clip_df.iloc[-1]['clip_name'] == 'Starting_params' or clip_df.iloc[-1]['clip_interval'] != clip_interval:
        return clip_interval
    elif clip_df.iloc[-1]['clip_duration'] >= clip_interval[1]/2:
        return clip_interval[0], int(clip_interval[1]/2)
    elif clip_df.iloc[-1]['clip_duration'] <= clip_interval[1]/2:
        return int(clip_interval[1]/2), clip_interval[1]


def adj_fork_name(clip_df, clip_name_list):
    if clip_df.iloc[-1]['clip_name'] == 'Starting_params' or len(clip_name_list) <= 1:
        return clip_name_list
    else:
        previous_clip_name = clip_df.iloc[-1]['clip_name']
        return [clip_name for clip_name in clip_name_list if clip_name != previous_clip_name]


def adj_first_clip_name(clip_df, clip_name_list, first_clip_name):
    if clip_df.iloc[-1]['clip_name'] == 'Starting_params' and first_clip_name:
        return [first_clip_name]
    else:
        return clip_name_list







