import pandas as pd                                                             
import os                                                                       
import re                                                                 
import numpy as np                                                               
import json
import sys



state_map_file = 'state_maps.json'
with open(state_map_file, 'r') as f:
    state_maps = json.load(f)

ambiguous_cities = ['san antonio', 'san jose', 'sj', 'la']


def loc_to_state(locstring):
    orig_locstring = locstring
    # print(locstring)
    if not isinstance(locstring, str): 
        return np.nan
    locstring = re.sub(r'\.', '', locstring) # remove dots in `D.C.` or `U.S.`
    locstring = re.sub(r'[^\w\s]', ' ', locstring) 
    locstring = re.sub(' +', ' ', locstring) # remove multiple spaces
    locstring = re.sub('\sof\s', ' ', locstring) # remove `of`
    locstring = locstring.split()
    # print(locstring)
    match = None
    
    matched_strings = []
    double_checked = False
    is_washington = False
            
    for i in range(len(locstring)):
        s1 = locstring[i]
        if i < len(locstring) - 1:
            s1s2 = locstring[i] + ' ' + locstring[i + 1]
        else:
            s1s2 = ''
        for s in [s1, s1s2]:
            if s.lower() in state_maps:
                # if len(s) == 2, then it is a statecode.                       
                # check that it was written in uppercase                        
                if len(s) == 2 and s.upper() != s:  
                    continue
                s = s.lower()
                matched_strings.append(s)
                if match is None:
                    match = state_maps[s]
                elif match == state_maps[s]:
                    double_checked = True
                elif all([st in [match, state_maps[s]] for st in ['LA', 'CA']]):
                    # if dispute is between LA and CA
                    match = 'CA'
                elif 'washington' in matched_strings and 'dc' in matched_strings:
                    # washington and dc are both present in the string, 
                    # and the only conflict is between wa/dc
                    # then the state must be DC
                    if match in ['WA', 'DC'] and state_maps[s] in ['WA', 'DC']:
                        match = 'DC'
                    else:
                        return None
                elif s == 'virginia' and 'west virginia' in matched_strings:
                    match = 'WV'
                else:# match != state_map[s], conflicting matches
                    # print('cnflict')
                    return None
                
    #print(match, matched_strings, double_checked)
    if any(ms in ambiguous_cities for ms in matched_strings):
        if loc_is_usa(orig_locstring) or double_checked:
            return match
        # sj and la are both ambiguous, but put together they must mean CA
        if 'sj' in matched_strings and 'la' in matched_strings:
            return 'CA'
            
        return None
    
    # Special double checks for WA
    if match == 'WA':
        if 'seattle' in matched_strings or 'wa' in matched_strings:
            return 'WA'
        if 'state' in locstring:
            return 'WA'
        if re.search(r',\s*washington', orig_locstring) != None:
            # find the pattern 'xxx, washington'
            return 'WA'
        return None
    
    if 'la' in matched_strings and match == 'CA':
        return match
        # elif only LA is matched but not to CA, then inconclusive
        
        
    # If LA is matched and is preceded by a comma, then it should be the state
    if match == 'LA' and 'louisiana' not in matched_strings:
        return 'LA' if re.search(r',\s*LA', orig_locstring) else None
    
    if match == 'DC' and 'colombia' in orig_locstring.lower():
        return None
    return match

           

if __name__ == '__main__':
    locstring = sys.argv[1]
    state = loc_to_state(locstring)
    if state is None:
        print('No matching US state for', locstring)
    else:
        print('US State for %s is %s' % (locstring, state))

