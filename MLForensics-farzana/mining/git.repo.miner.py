'''
Akond Rahman 
Nov 19, 2020 
Mine Git-based repos 
'''

import pandas as pd 
import csv 
import subprocess
import numpy as np
import shutil
from git import Repo
from git import exc 
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import time 
import  datetime 
import os 
import logging

# ----------------------------------------------------
# Logging configuration (Forensic logging requirement)
# ----------------------------------------------------
logging.basicConfig(
    filename="forensics.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


def deleteRepo(dirName, type_):
    logger.info(f"deleteRepo() called with dirName={dirName}, type_={type_}")
    print(':::' + type_ + ':::Deleting ', dirName)
    try:
        if os.path.exists(dirName):
            shutil.rmtree(dirName)
            logger.info(f"Successfully deleted repo at {dirName}")
        else:
            logger.info(f"Directory {dirName} does not exist")
    except OSError as e:
        logger.error(f"Failed deleting {dirName}: {e}", exc_info=True)
        print('Failed deleting, will try manually')        


def makeChunks(the_list, size_):
    for i in range(0, len(the_list), size_):
        yield the_list[i:i+size_]


def cloneRepo(repo_name, target_dir):
    logger.info(f"cloneRepo() called with repo_name={repo_name}, target_dir={target_dir}")
    cmd_ = "git clone " + repo_name + " " + target_dir 
    try:
        subprocess.check_output(['bash','-c', cmd_]) 
        logger.info(f"Successfully cloned repo: {repo_name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error cloning repo {repo_name}: {e}", exc_info=True)
        print('Skipping this repo ... trouble cloning repo:', repo_name )


def dumpContentIntoFile(strP, fileP):
    logger.info(f"dumpContentIntoFile() called with fileP={fileP}")
    try:
        fileToWrite = open(fileP, 'w')
        fileToWrite.write(strP)
        fileToWrite.close()
        size = os.stat(fileP).st_size
        logger.info(f"Wrote {size} bytes to file {fileP}")
        return str(size)
    except Exception as e:
        logger.error(f"Error writing to file {fileP}: {e}", exc_info=True)
        raise


def getPythonCount(path2dir): 
    logger.info(f"getPythonCount() called with path2dir={path2dir}")
    usageCount = 0
    try:
        for root_, dirnames, filenames in os.walk(path2dir):
            for file_ in filenames:
                full_path_file = os.path.join(root_, file_) 
                if file_.endswith('py'):
                    usageCount += 1

        logger.info(f"Python file count for {path2dir}: {usageCount}")
    except Exception as e:
        logger.error(f"Error counting python files in {path2dir}: {e}", exc_info=True)

    return usageCount                         


def cloneRepos(repo_list): 
    counter = 0     
    str_ = ''
    for repo_batch in repo_list:
        for repo_ in repo_batch:
            counter += 1 
            print('Cloning ', repo_ )
            dirName = '/Users/arahman/FSE2021_ML_REPOS/GITHUB_REPOS/' + repo_.split('/')[-2] + '@' + repo_.split('/')[-1] 
            cloneRepo(repo_, dirName )

            all_fil_cnt = sum([len(files) for r_, d_, files in os.walk(dirName)])
            if (all_fil_cnt <= 0):
               deleteRepo(dirName, 'NO_FILES')
            else: 
               py_file_count = getPythonCount(dirName)
               prop_py = float(py_file_count) / float(all_fil_cnt)
               if(prop_py < 0.25):
                   deleteRepo(dirName, 'LOW_PYTHON_' + str(round(prop_py, 5)))
            print("So far we have processed {} repos".format(counter))
            if((counter % 10) == 0):
                dumpContentIntoFile(str_, 'tracker_completed_repos.csv')
            elif((counter % 100) == 0):
                print(str_)                
            print('#'*100)


def getMLStats(repo_path):
    repo_statLs = []
    repo_count  = 0 
    all_repos = [f.path for f in os.scandir(repo_path) if f.is_dir()]
    print('REPO_COUNT:', len(all_repos))    

    for repo_ in all_repos:
        repo_count += 1 
        ml_lib_cnt = getMLLibraryUsage(repo_) 
        repo_statLs.append((repo_, ml_lib_cnt))
        print(repo_count, ml_lib_cnt)

    return repo_statLs 


def getMLLibraryUsage(path2dir): 
    logger.info(f"getMLLibraryUsage() called with path2dir={path2dir}")
    usageCount = 0 

    try:
        for root_, dirnames, filenames in os.walk(path2dir):
            for file_ in filenames:
                full_path_file = os.path.join(root_, file_) 
                if os.path.exists(full_path_file) and file_.endswith('py'):
                    try:
                        f = open(full_path_file, 'r', encoding='latin-1')
                        fileContent = f.read().split('\n')
                        f.close()
                    except Exception as e:
                        logger.error(f"Error reading {full_path_file}: {e}", exc_info=True)
                        continue

                    fileContents = [z_.lower() for z_ in fileContent if z_ != '\n']

                    for line in fileContents:
                        if any(key in line for key in ['sklearn', 'keras', 'gym.', 'pyqlearning', 'tensorflow', 'torch']):
                            usageCount += 1
                        elif any(key in line for key in ['rl_coach', 'tensorforce', 'stable_baselines', 'tf.']):
                            usageCount += 1

        logger.info(f"ML library usage count for {path2dir}: {usageCount}")
    except Exception as e:
        logger.error(f"Error scanning directory {path2dir} for ML libs: {e}", exc_info=True)

    return usageCount      


def deleteRepos():
    repos_df = pd.read_csv('DELETE_CANDIDATES_GITHUB_V2.csv')
    repos = np.unique(repos_df['REPO'].tolist()) 
    for x_ in repos:
        deleteRepo(x_, 'ML_LIBRARY_THRESHOLD')
