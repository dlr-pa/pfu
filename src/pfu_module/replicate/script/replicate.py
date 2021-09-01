"""
Author: Daniel Mohr.
Date: 2017-02-14, 2021-05-25 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import datetime
import logging
import os
import platform
import re
import subprocess
import time

from pfu_module.replicate.tools import *

__date__ = "2017-02-14"


def replicate(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2015-10-05, 2017-02-14, 2021-05-25 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    In this function the command line parameter/command 'replicate' is handled.
    """
    if not isinstance(args.source, str):
        args.source = args.source[0]
    if not isinstance(args.copy_program1, str):
        args.copy_program1 = args.copy_program1[0]
    if not isinstance(args.copy_parameter1, str):
        args.copy_parameter1 = args.copy_parameter1[0]
    if not isinstance(args.copy_program2, str):
        args.copy_program2 = args.copy_program2[0]
    if not isinstance(args.copy_parameter2, str):
        args.copy_parameter2 = args.copy_parameter2[0]
    if not isinstance(args.checksum_program, str):
        args.checksum_program = args.checksum_program[0]
    if not isinstance(args.checksum_create_parameter, str):
        args.checksum_create_parameter = args.checksum_create_parameter[0]
    if not isinstance(args.checksum_check_parameter, str):
        args.checksum_check_parameter = args.checksum_check_parameter[0]
    if not isinstance(args.checksum_check_method, int):
        args.checksum_check_method = args.checksum_check_method[0]
    if not isinstance(args.checksum_file_name, str):
        args.checksum_file_name = args.checksum_file_name[0]
    if not isinstance(args.checksum_file_name_destination, str):
        args.checksum_file_name_destination = \
            args.checksum_file_name_destination[0]
    if not isinstance(args.overwrite_checksum_file, int):
        args.overwrite_checksum_file = args.overwrite_checksum_file[0]
    if not isinstance(args.checksum_log_file_name, str):
        args.checksum_log_file_name = args.checksum_log_file_name[0]
    if not isinstance(args.checksum_status_file_name, str):
        args.checksum_status_file_name = args.checksum_status_file_name[0]
    if not isinstance(args.use_relpath, int):
        args.use_relpath = args.use_relpath[0]
    if not isinstance(args.use_normcase, int):
        args.use_normcase = args.use_normcase[0]
    if not isinstance(args.use_normpath, int):
        args.use_normpath = args.use_normpath[0]
    if not isinstance(args.number_of_processes, int):
        args.number_of_processes = args.number_of_processes[0]
    if not isinstance(args.limit_number_of_processes_to_distinations, int):
        args.limit_number_of_processes_to_distinations = \
            args.limit_number_of_processes_to_distinations[
                0]
    if not isinstance(args.sleeptime, float):
        args.sleeptime = args.sleeptime[0]
    if not isinstance(args.extrasleeptime, float):
        args.extrasleeptime = args.extrasleeptime[0]
    if args.use_relpath == 1:
        args.source = os.path.relpath(args.source)
        for i in range(len(args.destination)):
            args.destination[i] = os.path.relpath(args.destination[i])
    if args.use_normcase == 1:
        args.source = os.path.normcase(args.source)
        for i in range(len(args.destination)):
            args.destination[i] = os.path.normcase(args.destination[i])
    if args.use_normpath == 1:
        args.source = os.path.normpath(args.source)
        for i in range(len(args.destination)):
            args.destination[i] = os.path.normpath(args.destination[i])
    today = datetime.datetime.utcnow()
    args.checksum_log_file_name = re.sub("%date", today.strftime(
        "%Y-%m-%dT%H%M%S"), args.checksum_log_file_name)
    args.checksum_status_file_name = re.sub("%date", today.strftime(
        "%Y-%m-%dT%H%M%S"), args.checksum_status_file_name)
    # logging
    log = logging.getLogger('pfu.replicate')
    log.setLevel(logging.DEBUG)  # logging.DEBUG = 10
    # create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # logging.DEBUG = 10
    console_handler.setFormatter(
        logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S'))
    # add the handlers to log
    log.addHandler(console_handler)
    # print settings and informations
    log.info("pfu from %s\n" % __date__)
    log.info("setting:")
    log.info(" source: '%s'" % args.source)
    log.info(" source (absolut path): '%s'" % os.path.abspath(args.source))
    dests = ""
    for dest in args.destination:
        dests += "'" + dest + "'" + " "
    dests = dests.strip()
    if len(args.destination) <= 1:
        log.info(" destination: %s" % dests)
    else:
        log.info(" %d destinations: %s" % (len(args.destination), dests))
    dests = ""
    for dest in args.destination:
        dests += "'" + os.path.abspath(dest) + "'" + " "
    dests = dests.strip()
    if len(args.destination) <= 1:
        log.info(" destination (absolut path): %s" % dests)
    else:
        log.info(" %d destinations (absolut paths): %s" %
                 (len(args.destination), dests))
    log.info(" copy program1: %s" % args.copy_program1)
    log.info(" parameter for the copy program1: %s" % args.copy_parameter1)
    log.info(" copy program2: %s" % args.copy_program2)
    log.info(" parameter for the copy program2: %s" % args.copy_parameter2)
    log.info(" checksum program: %s" % args.checksum_program)
    log.info(" parameter for %s to create checksums: %s" %
             (args.checksum_program, args.checksum_create_parameter))
    log.info(" parameter for %s to check: %s" %
             (args.checksum_program, args.checksum_check_parameter))
    log.info(" checksum file name: %s" % args.checksum_file_name)
    log.info(" checksum log file name: %s" % args.checksum_log_file_name)
    log.info(" checksum status file name: %s" % args.checksum_status_file_name)
    log.info(" number of processes in parallel: %s" % args.number_of_processes)
    log.info(" platform: %s" % platform.platform())
    log.info(" system: %s" % platform.system())
    log.info(" release: %s" % platform.release())
    log.info("")
    # create commands to run
    warning_creating_checksums = ""
    commands_copy1 = []
    for dest in args.destination:
        source = os.path.abspath(args.source)
        destination = os.path.abspath(dest)
        if ((platform.system() == "Windows") and
                (args.copy_program1 == "rsync")):
            # e. g. "C:" have to be transformed to "/cygdrive/c/"
            drive_letter = re.findall(r'([a-zA-Z]{1}):[\\\/]{1}', source)
            if len(drive_letter) == 1:
                source = re.sub(r"[a-zA-Z]{1}:[\\\/]{1}",
                                ("/cygdrive/%s/" % drive_letter[0]),
                                source)
            drive_letter = re.findall(r'([a-zA-Z]{1}):[\\\/]{1}', destination)
            if len(drive_letter) == 1:
                destination = re.sub(r"[a-zA-Z]{1}:[\\\/]{1}",
                                     ("/cygdrive/%s/" % drive_letter[0]),
                                     destination)
        if ((platform.system() == "Windows") and
                (args.copy_program1 == "xcopy")):
            commands_copy1 += [args.copy_program1 + " " +
                               args.copy_parameter1 + " " +
                               source + " " +
                               destination]
        else:
            commands_copy1 += [args.copy_program1 + " " +
                               args.copy_parameter1 + " " +
                               source + "/" + " " +
                               destination + "/"]
    commands_copy2 = []
    for dest in args.destination:
        source = os.path.abspath(args.source)
        destination = os.path.abspath(dest)
        if ((platform.system() == "Windows") and
                (args.copy_program2 == "rsync")):
            # e. g. "C:" have to be transformed to "/cygdrive/c/"
            drive_letter = re.findall(r'([a-zA-Z]{1}):[\\\/]{1}', source)
            if len(drive_letter) == 1:
                source = re.sub(r"[a-zA-Z]{1}:[\\\/]{1}",
                                ("/cygdrive/%s/" % drive_letter[0]),
                                source)
            drive_letter = re.findall(r'([a-zA-Z]{1}):[\\\/]{1}', destination)
            if len(drive_letter) == 1:
                destination = re.sub(r"[a-zA-Z]{1}:[\\\/]{1}",
                                     ("/cygdrive/%s/" % drive_letter[0]),
                                     destination)
        commands_copy2 += [args.copy_program2 + " " +
                           args.copy_parameter2 + " " +
                           source + "/" + " " +
                           destination + "/"]
    commands_create_checksums = []
    if (not args.dryrun) and (args.overwrite_checksum_file == 1):
        for (dirpath, dirnames, filenames) in os.walk(args.source):
            if ((os.path.exists(
                os.path.join(dirpath, args.checksum_file_name))) and
                    (args.overwrite_checksum_file == 1)):
                os.remove(os.path.join(dirpath, args.checksum_file_name))
    for (dirpath, dirnames, filenames) in os.walk(args.source):
        if ((not os.path.exists(
            os.path.join(dirpath, args.checksum_file_name))) or
                (args.overwrite_checksum_file == 1)):
            # create commands to create checksums
            file_list = create_file_list(dirpath, filenames)
            if len(file_list) > 0:
                # sha256 sum will wait for stdin, if no files are given
                change_dir = create_change_dir_command(dirpath)
                commands_create_checksums += [
                    change_dir + dirpath + " && " +
                    args.checksum_program + " " +
                    args.checksum_create_parameter + " " +
                    file_list + " > " +
                    args.checksum_file_name]
        elif ((os.path.exists(
                os.path.join(dirpath, args.checksum_file_name))) and
                (args.overwrite_checksum_file == 2)):
            # create commands to create checksums for missing ones
            stat = "WARNING: '%s' " % args.checksum_file_name
            stat += "already exists in '%s', " % dirpath
            stat += "but missing checksums will be created"
            log.info(stat)
            warning_creating_checksums += stat + "\n"
            # read checksums to find missing checksums
            files_with_checksum = []
            f = open(os.path.join(dirpath, args.checksum_file_name), 'r')
            for line in f:
                line = line.strip()
                m = re.findall(r'[^ ]+ \((.+)\) = [^ ]+\Z', line)
                if m:
                    files_with_checksum += m
            f.close()
            # find missing checksums
            filenames = set(filenames).difference(files_with_checksum)
            filenames = filenames.difference([args.checksum_file_name])
            file_list = create_file_list('', list(filenames))
            if len(file_list) > 0:  # create command
                change_dir = create_change_dir_command(dirpath)
                commands_create_checksums += [
                    change_dir + dirpath + " && " +
                    args.checksum_program + " " +
                    args.checksum_create_parameter + " " +
                    file_list + " >> " +
                    args.checksum_file_name]
        else:
            # do not create commands to create checksums
            stat = "WARNING: '%s' already exists in '%s'" % (
                args.checksum_file_name, dirpath)
            log.info(stat)
            warning_creating_checksums += stat + "\n"
    commands_check_checksums = []
    for dest in args.destination:
        if args.checksum_check_method == 1:
            # Do not check the checksums, but instead calculate new ones.
            cmds = []
            for (dirpath, dirnames, filenames) in os.walk(args.source):
                p = os.path.join(dest, os.path.relpath(dirpath, args.source))
                p = os.path.normpath(p)
                file_list = create_file_list(dirpath, filenames)
                if len(file_list) > 0:
                    change_dir = create_change_dir_command(p)
                    cmds += [change_dir + p + " && " +
                             args.checksum_program + " " +
                             args.checksum_create_parameter + " " +
                             file_list + " > " +
                             args.checksum_file_name_destination]
            commands_check_checksums += [cmds]
        else:  # args.checksum_check_method == 0
            # Check the checksums by the program creating checksums.
            cmds = []
            for (dirpath, dirnames, filenames) in os.walk(args.source):
                p = os.path.join(dest, os.path.relpath(dirpath, args.source))
                p = os.path.normpath(p)
                file_list = create_file_list(dirpath, filenames)
                if len(file_list) > 0:
                    change_dir = create_change_dir_command(p)
                    cmds += [change_dir + p + " && " +
                             args.checksum_program + " " +
                             args.checksum_check_parameter + " " +
                             args.checksum_file_name + " " +
                             "> " + args.checksum_log_file_name + " "
                             "2> " + args.checksum_status_file_name]
            commands_check_checksums += [cmds]
    log.info("the following commands will be run:\n")
    for c in commands_copy1:
        log.info(" %s" % c)
    for c in commands_create_checksums:
        log.info(" %s" % c)
    log.info(" # wait until above commands are ready")
    for c in commands_copy2:
        log.info(" %s" % c)
    log.info(" # wait until above commands are ready")
    for cc in commands_check_checksums:
        for c in cc:  # these ones should run sequential
            log.info(" %s" % c)
    if args.dryrun:
        log.info("")
        log.info("dryrun finished.")
        exit()
    log.info("")
    log.info("###########")
    log.info("### run ###")
    log.info("###########\n")
    # step 1/3 (copy + create checksum)
    log.info(
        "### run step 1/3 (copy with %s + create checksum with %s) ###\n" %
        (args.copy_program1, args.checksum_program))
    summary = ""
    # run copy program1 and create checksums
    create_checksums_errors = ""
    runs = dict()
    runs['processes'] = [None] * args.number_of_processes
    runs['cmd'] = [None] * args.number_of_processes
    cri = 0
    ccc = 0
    while ((cri < len(commands_copy1)) or
           (ccc < len(commands_create_checksums))):
        i = wait_for_free_slot(
            runs['processes'], args.number_of_processes, args.sleeptime)
        if not (runs['processes'][i] is None):
            stat = "process '%s' terminated with %d" % (
                runs['cmd'][i], runs['processes'][i].returncode)
            log.info(stat)
            summary += stat + "\n"
            if runs['processes'][i].returncode != 0:
                create_checksums_errors += stat + "\n"
            runs['processes'][i] = None
        # start subprocess
        if cri < len(commands_copy1):
            runs['processes'][i] = subprocess.Popen(
                commands_copy1[cri], bufsize=-1, shell=True)
            runs['cmd'][i] = commands_copy1[cri]
            log.info("started '%s'" % commands_copy1[cri])
            cri += 1
        elif ccc < len(commands_create_checksums):
            runs['processes'][i] = subprocess.Popen(
                commands_create_checksums[ccc], bufsize=-1, shell=True)
            runs['cmd'][i] = commands_create_checksums[ccc]
            log.info("started '%s'" % commands_create_checksums[ccc])
            ccc += 1
    # wait until all processes are ready
    log.info(
        "all processes started for step 1/3 " +
        "(copy with %s + create checksum with %s)" %
        (args.copy_program1, args.checksum_program))
    for i in range(args.number_of_processes):
        if not (runs['processes'][i] is None):
            runs['processes'][i].wait()
            stat = "process '%s' terminated with %d" % (
                runs['cmd'][i], runs['processes'][i].returncode)
            log.info(stat)
            summary += stat + "\n"
            if runs['processes'][i].returncode != 0:
                create_checksums_errors += stat + "\n"
            runs['processes'][i] = None
    time.sleep(args.extrasleeptime)
    # run step 2/3 (copy)
    log.info("")
    log.info("### run step 2/3 (copy with %s) ###\n" % args.copy_program2)
    copy_errors = ""
    cri = 0
    while cri < len(commands_copy2):
        i = wait_for_free_slot(
            runs['processes'], args.number_of_processes, args.sleeptime)
        if not (runs['processes'][i] is None):
            stat = "process '%s' terminated with %d" % (
                runs['cmd'][i], runs['processes'][i].returncode)
            log.info(stat)
            summary += stat + "\n"
            if runs['processes'][i].returncode != 0:
                copy_errors += stat + "\n"
            runs['processes'][i] = None
        # start subprocess
        if cri < len(commands_copy2):
            runs['processes'][i] = subprocess.Popen(
                commands_copy2[cri], bufsize=-1, shell=True)
            runs['cmd'][i] = commands_copy2[cri]
            log.info("started '%s'" % commands_copy2[cri])
            cri += 1
    # wait until all processes are ready
    log.info("all processes started for step 2/3 (copy with %s)" %
             args.copy_program2)
    for i in range(args.number_of_processes):
        if not (runs['processes'][i] is None):
            runs['processes'][i].wait()
            stat = "process '%s' terminated with %d" % (
                runs['cmd'][i], runs['processes'][i].returncode)
            log.info(stat)
            summary += stat + "\n"
            if runs['processes'][i].returncode != 0:
                copy_errors += stat + "\n"
            runs['processes'][i] = None
    time.sleep(args.extrasleeptime)
    # run step 3/3 (check checksums)
    log.info("")
    log.info("### run step 3/3 (check checksums with %s) ###\n" %
             args.checksum_program)
    summary, check_checksums_errors = run_check_checksums(
        args, log, commands_check_checksums,
        text="all processes started for step 3/3 (check checksums with %s)" %
        args.checksum_program,
        summary=summary)
    # print/log summary
    log.info("")
    log.info("###############")
    log.info("### summary ###")
    log.info("###############\n")
    log.info(summary)
    log.info("##################################")
    log.info("### warning creating checksums ###")
    log.info("##################################\n")
    if warning_creating_checksums != "":
        log.info(warning_creating_checksums)
    log.info("######################################")
    log.info("### copy + create checksum errors ###")
    log.info("######################################\n")
    if create_checksums_errors != "":
        log.info(create_checksums_errors)
    log.info("####################")
    log.info("### copy errors ###")
    log.info("####################\n")
    if copy_errors != "":
        log.info(copy_errors)
    log.info("#######################")
    log.info("### checksum errors ###")
    log.info("#######################\n")
    if check_checksums_errors != "":
        log.info(check_checksums_errors)
    log.info("finished.")
