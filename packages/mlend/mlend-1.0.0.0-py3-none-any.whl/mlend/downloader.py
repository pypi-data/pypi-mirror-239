'''
API to download dataset.
Version : 1.0.0.0

'''

from __future__ import absolute_import, division, print_function
name = "MLEnd | data downloader"
import sys

if sys.version_info[:2] < (3, 3):
    old_print = print
    def print(*args, **kwargs):
        flush = kwargs.pop('flush', False)
        old_print(*args, **kwargs)
        if flush:
            file = kwargs.get('file', sys.stdout)
            # Why might file=None? IDK, but it works for print(i, file=None)
            file.flush() if file is not None else sys.stdout.flush()

import sys, os, six, time, collections, glob
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import urlopen, urlretrieve
import tarfile

from pathlib import Path

try:
    import queue
except ImportError:
    import Queue as queue

import spkit as sp
import pandas as pd
import numpy as np


A=['\\','-','/','|']

def ProgBar_JL(i,N,title='',style=2,L=100,selfTerminate=True,delta=None,sym='▓',color='green'):
    c1 = sp.utils.bcolors.ENDC
    if color.lower() in ['green','blue','cyan','red']:
        if color.lower()=='green':
            c1 = sp.utils.bcolors.OKGREEN
        elif color.lower()=='blue':
            c1 = sp.utils.bcolors.OKBLUE
        elif color.lower()=='cyan':
            c1 = sp.utils.bcolors.OKCYAN
        elif color.lower()=='red':
            c1 = sp.utils.bcolors.CRED

    c2 = sp.utils.bcolors.ENDC


    pf = int(100*(i+1)/float(N))
    st = '\r'+' '*(3-len(str(pf))) + str(pf) +'%|'

    if L==50:
        pb = sym*int(pf//2)+' '*(L-int(pf//2))
    else:
        L = 100
        pb = sym*pf+' '*(L-pf)

    pb = c1 + pb + c2 +'|'

    if style==1:
        print(st+A[i%len(A)]+'|'+pb+title,end='', flush=True)
    elif style==2:
        print(st+pb+str(N)+'\\'+str(i+1)+'|'+title,end='', flush=True)
    if pf>=100 and selfTerminate:
        print('\nDone..')

def ProgBar(i,N,title='',style=2,L=100,selfTerminate=False,sym='▓',color='green'):

    c1 = sp.utils.bcolors.ENDC
    if color.lower() in ['green','blue','cyan','red']:
        if color.lower()=='green':
            c1 = sp.utils.bcolors.OKGREEN
        elif color.lower()=='blue':
            c1 = sp.utils.bcolors.OKBLUE
        elif color.lower()=='cyan':
            c1 = sp.utils.bcolors.OKCYAN
        elif color.lower()=='red':
            c1 = sp.utils.bcolors.CRED

    c2 = sp.utils.bcolors.ENDC

    pf = int(100*(i+1)/float(N))
    st = ' '*(3-len(str(pf))) + str(pf) +'%|'

    if L==50:
        pb = sym*int(pf//2)+' '*(L-int(pf//2))
    else:
        L = 100
        pb = sym*pf+' '*(L-pf)
    pb = c1 + pb + c2 +'|'
    if style==1:
        print(st+A[i%len(A)]+'|'+pb+title,end='\r', flush=True)
    elif style==2:
        print(st+pb+str(N)+'\\'+str(i+1)+'|'+title,end='\r', flush=True)
    if pf>=100 and selfTerminate:
        print('\nDone..')


def _download_file(origin,fpath,bar=True):
    ff = origin.split('/')[-1].split('.')[0]
    class ProgressTracker(object):
        progbar = None

    def dl_progress(count, block_size, total_size):
        #print(count, block_size, count * block_size, total_size)
        if bar:
            #sp.utils.ProgressBar(count * block_size,total_size,title=sub)
            sp.utils.ProgBar(count * block_size,total_size,L=50,title=f'{ff}')
        else:
            pass

    error_msg = 'URL fetch failure on {} : {} -- {}'
    try:
        try:
            urlretrieve(origin, fpath, dl_progress)
        except HTTPError as e:
            raise Exception(error_msg.format(origin, e.code, e.msg))
        except URLError as e:
            raise Exception(error_msg.format(origin, e.errno, e.reason))
    except (Exception, KeyboardInterrupt):
        if os.path.exists(fpath):
            os.remove(fpath)
        raise
    ProgressTracker.progbar = None

    return fpath


def download_spoken_numerals(save_to = '../MLEnd', subset = {},verbose=1,overwrite=False,pbar_style='colab'):
    """Download Spoken Numerals Dataset.

    # Arguments
        save_to: loacal path where you want to store the data
                  relative to `../MLEnd/spoken_numerals/`).
        subset: subset of data to download. {'attribute_name':list_of_values to select}
                 subset = {'Numeral':[1,2]}, will download audio files of numerals 1 and 2 only
                 subset = {'Numeral':[1,2], 'Intonation':['excited','question'], 'Speaker':[1,2,3,4,5,6]}

    # Raises
        ValueError:
         - in case keys in subset are not in ['Numeral', 'Intonation', 'Speaker']
         - in case values of any keys are not valid

    # Returns

    path: path where data is saved


    """
    #DataPath = 'https://github.com/Nikeshbajaj/PhyaatDataset/raw/master/Signals/'
    repo_path = 'https://github.com/MLEndDatasets/SpokenNumerals'
    audio_files_path  = repo_path + '/raw/main/MLEndSND_audiofiles/'
    attributes_file   = repo_path + '/raw/main/MLEndSND_audio_attributes_benchmark.csv'
    speaker_demog_file = repo_path + '/raw/main/MLEndSND_speakers_demographics_benchmark.csv'


    D = pd.read_csv(attributes_file)
    S = pd.read_csv(speaker_demog_file)


    # Keys in subset should be one of ['Numeral', 'Intonation', 'Speaker']
    D_attr = list(D)
    if len(subset):
        for key in subset:
            if key not in D_attr:
                raise ValueError(f"Invalid attribute, {key}. Should be one of ['Numeral', 'Intonation', 'Speaker']")
            D_valu = set(list(D[key]))
            values = set(subset[key])

            # Values of any keys are not valid
            # Values of key
            if len(values - D_valu)>0:
                raise ValueError(f"Invalid value of attribute {key}: {values - D_valu}")

    try:
        datadir_main = os.path.join(save_to, 'spoken_numerals')
        datadir = os.path.join(datadir_main, 'MLEndSND_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError:
        print('NOTE:: Path :  \"'+ save_to +'\" is not accessible. Creating  \"spoken_numerals\" in  "/tmp\" directory for dataset' )
        save_to = os.path.join('/tmp','MLEnd')
        datadir_main = os.path.join(save_to, 'spoken_numerals')
        datadir = os.path.join(datadir_main, 'MLEndSND_audiofiles')
        path    = Path(datadir)
        path.mkdir(parents=True, exist_ok=True)

    #print(datadir1,datadir,path)

    D.to_csv(datadir_main+'/MLEndSND_audio_attributes_benchmark.csv')
    S.to_csv(datadir_main+'/MLEndSND_speakers_demographics_benchmark.csv')

    Di = D.copy()
    Di['select'] = 0
    for key in subset:
        values = subset[key]
        for value in values:
            Di.loc[Di[key]==value,'select'] = 1

        Di = Di[Di['select']==1]
        Di['select'] = 0

    N = Di.shape[0]
    if verbose: print(f'Downloading {N} audio files from {repo_path}')

    filenames = list(Di['filename'])

    for k,filename in enumerate(filenames):
        #sp.utils.ProgBar(k,len(filenames),L=50,title=f'{filename}')
        if verbose:
            if pbar_style==None:
                ProgBar(k,len(filenames),style=2,L=50,color='blue',title=f'{filename}')
            elif pbar_style == 'colab':
                ProgBar_JL(k,len(filenames),style=2,L=50,color='blue',title=f'{filename}')
            elif pbar_style=='spkit_JL':
                sp.utils.ProgBar_JL(k,len(filenames),style=2,L=50,title=f'{filename}')

        origin = audio_files_path + filename
        fpath =  datadir +'/'+ filename
        if not(os.path.isfile(fpath)) or overwrite:
            ifpath = _download_file(origin,fpath,bar=False)

    return datadir_main
