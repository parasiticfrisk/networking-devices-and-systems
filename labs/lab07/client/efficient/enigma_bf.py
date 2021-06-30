#!/usr/bin/env python3
#
# Author: August Frisk
# Course: CmpEt 269 - Spring 2018
# Assign: Lab 07
# File: enigma_bf.py
#
# Description: Attempts a partial brute force attack on Enigma messages.
#              Messages may be created on a real machine, compatible replica,
#              the Cryptoy Android App or any application that accurately
#              reproduces the 3-rotor machine used by the german armed forces.
#              Requires Brian Neal's Py-enigma Python3 library and utilities.
#
#              This code uses Dispy on OctaPi using the recommended method for
#              managing jobs efficiently. For more information, visit the Dispy
#              website.
#
# Brute Force attack: This is a limited brute force attack on the rotor
#                     settings assuming no plugboard and no rotor ring
#                     Using 'THISXISXWORKING' as the crib message
#


# setup machine to be the same as that used for encrypt

character = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotor = [
    "I II III",
    "I II IV",
    "I II V",
    "I III II",
    "I III IV",
    "I III V",
    "I IV II",
    "I IV III",
    "I IV V",
    "I V II",
    "I V III",
    "I V IV",
    "II I III",
    "II I IV",
    "II I V",
    "II III I",
    "II III IV",
    "II III V",
    "II IV I",
    "II IV III",
    "II IV V",
    "II V I",
    "II V III",
    "II V IV",
    "III I II",
    "III I IV",
    "III I V",
    "III II I",
    "III II IV",
    "III II V",
    "III IV I",
    "III IV II",
    "III IV V",
    "IV I II",
    "IV I III",
    "IV I V",
    "IV II I",
    "IV II III",
    "IV I V",
    "IV II I",
    "IV II III",
    "IV II V",
    "IV III I",
    "IV III II",
    "IV III V",
    "IV V I",
    "IV V II",
    "IV V III",
    "V I II",
    "V I III",
    "V I IV",
    "V II I",
    "V II III",
    "V II IV",
    "V III I",
    "V III II",
    "V III IV",
    "V IV I",
    "V IV II",
    "V IV III",
]

ring = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
]

#
# This function does an exhaust search over the list of possible
# rotor selections
#
def find_rotor_start(rotor_choice, ring_choice, ciphertext, cribtext):

    from enigma.machine import EnigmaMachine

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    machine = EnigmaMachine.from_key_sheet(
        rotors=rotor_choice,
        reflector="B",
        ring_settings=ring_choice,
        plugboard_settings="AV BS CG DL FU HZ IN KM OW RX",
    )  # plugboard known

    # do an exhaust search over all possible rotor starting positions
    for i in range(len(alphabet)):  # search for rotor 1 start position
        for j in range(len(alphabet)):  # search for rotor 2 start position
            for k in range(len(alphabet)):  # search for rotor 3 start position
                # generate a possible rotor start position
                start_pos = alphabet[i] + alphabet[j] + alphabet[k]

                # set machine initial starting position and attempt decrypt
                machine.set_display(start_pos)
                plaintext = machine.process_text(ciphertext)

                # check if decrypt is the same as the crib text
                if plaintext == cribtext:
                    # print( start_pos, plaintext, cribtext )
                    return (rotor_choice, ring_choice, start_pos)

    return (rotor_choice, ring_choice, "null")


# dispy calls this function to indicate change in job status
def job_callback(job):  # executed at the client
    global pending_jobs, jobs_cond
    global found

    if job.status == dispy.DispyJob.Finished or job.status in (  # most usual case
        dispy.DispyJob.Terminated,
        dispy.DispyJob.Cancelled,
        dispy.DispyJob.Abandoned,
    ):
        # 'pending_jobs' is shared between two threads, so access it with
        # 'jobs_cond' (see below)
        jobs_cond.acquire()
        if job.id:  # job may have finished before 'main' assigned id
            pending_jobs.pop(job.id)

            # extract the results for each job as it happens
            (
                rotor_choice,
                ring_choice,
                start_pos,
            ) = job.result  # returns results from job
            if start_pos != "null":
                found = True
                dispy.logger.info(
                    'Machine setting found: job "%i" returned "%s" with ring "%s" using "%s", %s jobs pending',
                    job.id,
                    rotor_choice,
                    ring_choice,
                    start_pos,
                    len(pending_jobs),
                )

            if len(pending_jobs) <= lower_bound:
                jobs_cond.notify()

        jobs_cond.release()


# main loop
if __name__ == "__main__":
    import dispy, argparse, resource, threading, logging

    # set lower and upper bounds as appropriate
    # lower_bound is at least num of cpus and upper_bound is roughly 3x lower_bound
    # lower_bound, upper_bound = 352, 1056
    lower_bound, upper_bound = 32, 96

    resource.setrlimit(
        resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY)
    )
    resource.setrlimit(
        resource.RLIMIT_DATA, (resource.RLIM_INFINITY, resource.RLIM_INFINITY)
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "ciphertext", help="cipher text, which is the encrypted text to be broken"
    )
    parser.add_argument("cribtext", help="crib text, which is known message content")
    args = parser.parse_args()

    # extract the cipher and crib texts from the command line
    ciphertext = args.ciphertext
    cribtext = args.cribtext

    server_nodes = "192.168.1.*"

    # use Condition variable to protect access to pending_jobs, as
    # 'job_callback' is executed in another thread
    jobs_cond = threading.Condition()

    pending_jobs = {}
    cluster = dispy.JobCluster(
        find_rotor_start,
        nodes=server_nodes,
        callback=job_callback,
        loglevel=logging.INFO,
    )

    print(
        "Brute force crypt attack on Enigma message %s using crib %s"
        % (ciphertext, cribtext)
    )

    # try all rotor settings (choosing three from five)
    found = False
    i = 1  # job counter
    r0 = 0  # ring 0 counter
    r1 = 0  # ring 1 counter
    r2 = 0  # ring 2 counter
    while (r0 < len(ring)) and (found == False):
        while (r1 < len(ring)) and (found == False):
            while (r2 < len(ring)) and (found == False):

                ring_choice = ring[r0] + " " + ring[r1] + " " + ring[r2]
                rot = 1  # rotor combination counter

                while (rot < len(rotor)) and (found == False):
                    rotor_choice = rotor[rot]

                    print(
                        'Trying rotor "%s" with ring "%s" ...'
                        % (rotor_choice, ring_choice)
                    )

                    # schedule execution of find_rotor_start (running 'dispynode')
                    job = cluster.submit(
                        rotor_choice, ring_choice, ciphertext, cribtext
                    )

                    jobs_cond.acquire()

                    job.id = i  # associate an ID to the job

                    # there is a chance the job may have finished and job_callback called by
                    # this time, so put it in 'pending_jobs' only if job is pending
                    if (
                        job.status == dispy.DispyJob.Created
                        or job.status == dispy.DispyJob.Running
                    ):
                        pending_jobs[i] = job
                        # dispy.logger.info('job "%s" submitted: %s', i, len(pending_jobs))
                        if len(pending_jobs) >= upper_bound:
                            while len(pending_jobs) > lower_bound:
                                jobs_cond.wait()
                    jobs_cond.release()

                    rot += 1  # next rotor combination

                    i += 1  # next job
                r2 += 1  # next ring 2 setting
            r1 += 1  # next ring 1 setting
        r0 += 1  # next ring 0 setting

    cluster.wait()

    if found == False:
        print("Attack unsuccessfull")

    cluster.print_status()
    cluster.close()
