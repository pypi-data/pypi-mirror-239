import pandas as pd
import math
import csv
from lstpressure import observable, Observation, LSTCalendar, LSTIntervalType as I


class csv_getter:

    def __init__(self, inputfile, outputfile) -> None:
        self.inputfile : str = inputfile
        self.outputfile: str = outputfile

    def get_formatted(self, inputfile) -> list:

        '''Extracting only night time observations from a 
        given file of observational information
        '''
        
        data = pd.read_csv(self.inputfile)
        
        night_obs = data['night_obs']
        avoid_sun = data['avoid_sunrise_sunset']
        LST_s = data['lst_start']
        LST_e = data['lst_start_end']
        durations = data['simulated_duration']
        duration = [0 if math.isnan(x) else x for x in durations]
        proposal_id = data['proposal_id']
        #proposal_id = sorted(proposal_id)
        ID = data['id']
        
        obs = []
        duration_ = []
        LST_starts = []
        LST_ends = []

        for ind in range(len(ID)):
            duration_.append(round(duration[ind]/3600,2))
            
            h1,m1 = LST_s[ind].split(':')
            f1 = round((int(h1) * 3600 + int(m1) * 60)/3600,2)
            LST_starts.append(f1)
            
            h2,m2 = LST_e[ind].split(':')
            f2 = round((int(h2) * 3600 + int(m2) * 60)/3600,2)
            LST_ends.append(f2)
        
        for i in range(len(proposal_id)):
            if night_obs[i] == 'Yes':
                obs.append([proposal_id[i],LST_starts[i],LST_ends[i],[I.NIGHT_ONLY, I.AVOID_SUNSET_SUNRISE],duration_[i]])
            elif avoid_sun[i] == 'Yes':
                obs.append([proposal_id[i],LST_starts[i],LST_ends[i],[I.AVOID_SUNRISE_SUNSET, I.AVOID_SUNSET_SUNRISE],duration_[i]])
            else:
                obs.append([proposal_id[i],LST_starts[i],LST_ends[i],[I.ALL_DAY],duration_[i]])
                
        return obs

    def get_csvfile(self):
        pass