#!/usr/bin/python

import itertools
import multiprocessing
import os
import sys
import shutil
import subprocess
from threading import Timer
import sys
from argparse import ArgumentParser
from subprocess import Popen, PIPE, STDOUT, call


def get_immediate_subdirectories(a_dir):
    return [(os.path.join(a_dir, name)) for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


TMP_DIR = ""


def ParallelExtractDir(args, dir):
    if dir.endswith("Positive"):
        print('Processing dir with sample type 1: ' + dir)
        ExtractFeaturesForDir(args, dir, "", sample_type=1)
    elif dir.endswith("Negative"):
        print('Processing dir with sample type 2: ' + dir)
        ExtractFeaturesForDir(args, dir, "", sample_type=2)
    else:
        print('Processing dir: ' + dir)
        ExtractFeaturesForDir(args, dir, "")


def ExtractFeaturesForDir(args, dir, prefix, sample_type=0):
    if sample_type > 0:
        print('ExtractFeaturesForDir - Processing dir {0} with sample type {1}'.format(dir, str(sample_type)))
        command = ['dotnet', 'run', '--project', args.csproj,
                   '--max_length', str(args.max_path_length), '--max_width', str(args.max_path_width),
                   '--path', dir, '--threads', str(args.num_threads), '--ofile_name', str(args.ofile_name),
                   '--sample_type', str(sample_type)]
    else:
        print('ExtractFeaturesForDir - Processing dir without sample type ' + dir)
        exit(1)
        command = ['dotnet', 'run', '--project', args.csproj,
                   '--max_length', str(args.max_path_length), '--max_width', str(args.max_path_width),
                   '--path', dir, '--threads', str(args.num_threads), '--ofile_name', str(args.ofile_name)]

    # print command
    # os.system(command)
    kill = lambda process: process.kill()
    sleeper = subprocess.Popen(command, stderr=subprocess.PIPE)
    # timer = Timer(60000000, kill, [sleeper])

    # try:
    # timer.start()
    _, stderr = sleeper.communicate()
    # finally:
    # timer.cancel()

    if len(stderr) > 0:
        print(sys.stderr, stderr)
    else:
        print('went well ...')
    # if sleeper.poll() == 0:
    #     if len(stderr) > 0:
    #         print(sys.stderr, stderr)
    # else:
    #     print(sys.stderr, 'dir: ' + str(dir) + ' was not completed in time')
    #     failed = True
    #     subdirs = get_immediate_subdirectories(dir)
    #     for subdir in subdirs:
    #         ExtractFeaturesForDir(args, subdir, prefix + dir.split('/')[-1] + '_')


def ExtractFeaturesForDirsList(args, dirs):
    global TMP_DIR
    TMP_DIR = "./tmp/feature_extractor%d/" % (os.getpid())
    if os.path.exists(TMP_DIR):
        shutil.rmtree(TMP_DIR, ignore_errors=True)
    os.makedirs(TMP_DIR)
    try:
        # p = multiprocessing.Pool(4)
        # p.starmap(ParallelExtractDir, zip(itertools.repeat(args), dirs))
        for dir in dirs:
            # ExtractFeaturesForDir(args, dir, '')
            ParallelExtractDir(args, dir)
        # p.close()
        # p.join()

        output_files = os.listdir(TMP_DIR)
        print('Total output files: ' + str(len(output_files)))
        for f in output_files:
            os.system("cat %s/%s" % (TMP_DIR, f))
    finally:
        shutil.rmtree(TMP_DIR, ignore_errors=True)


if __name__ == '__main__':
    print('---C# extractor start')
    parser = ArgumentParser()
    parser.add_argument("-maxlen", "--max_path_length", dest="max_path_length", required=False, default=8)
    parser.add_argument("-maxwidth", "--max_path_width", dest="max_path_width", required=False, default=2)
    parser.add_argument("-threads", "--num_threads", dest="num_threads", required=False, default=64)
    parser.add_argument("--csproj", dest="csproj", required=True)
    parser.add_argument("-dir", "--dir", dest="dir", required=False)
    parser.add_argument("-ofile_name", "--ofile_name", dest="ofile_name", required=True)
    args = parser.parse_args()

    if args.dir is not None:
        subdirs = get_immediate_subdirectories(args.dir)
        print('Subdirs: ' + str(subdirs))
        to_extract = subdirs
        if len(subdirs) == 0:
            to_extract = [args.dir.rstrip('/')]
        ExtractFeaturesForDirsList(args, to_extract)
    print('---C# extractor end')
