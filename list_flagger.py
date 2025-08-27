import re
import pandas as pd
from tqdm.auto import tqdm

def Flag_phrase(phrase):
    phrase = phrase.lower()
    flags_broad = []
    flags_exact = []
    for flag in flags:
        any_search = re.search('.*' + flag + '.*', phrase)
        left_search = re.search('^' + flag + '\W.*', phrase)
        mid_search = re.search('.*\W' + flag + '\W.*', phrase)
        right_search = re.search('.*' + flag + '$', phrase)

        flag_score = 0
        if any_search:
            flag_score += 1
        if left_search or mid_search or right_search:
            flag_score += 1

        if flag_score == 2:
            flags_broad.append(flag)
            flags_exact.append(flag)
        elif flag_score == 1:
            flags_broad.append(flag)

    flags_broad_string = ';'.join(flags_broad)
    flags_exact_string = ';'.join(flags_exact)
    return [flags_broad_string, flags_exact_string]

#Open Files
df_flags = pd.read_csv(r'flags.csv',encoding='utf-8')
df_phrases = pd.read_csv(r'phrases.csv',encoding='utf-8')

#Make flags set
flags = []
for i in df_flags.index:
    flag = df_flags[df_flags.columns[0]][i].lower()
    flags.append(flag)
flags = set(flags)

#Flag phrases
tqdm.pandas(desc='Flagging Phrases', colour='green')
df_phrases['All Flags'] = df_phrases.progress_apply(lambda x: Flag_phrase(x['Phrases']),axis=1)
tqdm.pandas(desc='Marking Broad Flags', colour='green')
df_phrases['Flags Broad'] = df_phrases.progress_apply(lambda x: x['All Flags'][0],axis=1)
tqdm.pandas(desc='Marking Exact Flags', colour='green')
df_phrases['Flags Exact'] = df_phrases.progress_apply(lambda x: x['All Flags'][1],axis=1)

#Write File
header = ['Phrases','Flags Broad','Flags Exact']
df_phrases.to_csv('phrases_flagged.csv', columns = header, index = False)

print('Done!')
