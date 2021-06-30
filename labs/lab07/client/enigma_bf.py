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
#              This code uses Dispy on OctaPi in standard form.
#
# Brute Force attack: This is a limited brute force attack on the rotor
#                     settings assuming no plugboard and no rotor ring
#                     Using 'THISXISXWORKING' as the crib message
#


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


# main loop
if __name__ == "__main__":
    import argparse, dispy, resource

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
    parser.add_argument("ring_choice", help="slip ring setting to use, eg '1 1 1'")
    args = parser.parse_args()

    # extract the cipher and crib texts from the command line
    ciphertext = args.ciphertext
    cribtext = args.cribtext
    ring_choice = args.ring_choice

    cluster = dispy.JobCluster(find_rotor_start, nodes="192.168.1.*")
    jobs = []
    id = 1  # job id

    print(
        (
            "Brute force crypt attack on Enigma message %s using crib %s"
            % (ciphertext, cribtext)
        )
    )

    # try all rotor settings (choosing three from five)
    print('Trying all rotor setings for ring choice "%s" ...' % (ring_choice))

    # submit the jobs for this ring choice
    for rotor_choice in rotor:
        job = cluster.submit(rotor_choice, ring_choice, ciphertext, cribtext)
        job.id = id  # associate an ID to the job
        jobs.append(job)
        id += 1  # next job

    print("Waiting...")
    cluster.wait()
    print("Collecting job results")

    # collect and check through the jobs for this ring setting
    found = False
    for job in jobs:
        (
            rotor_setting,
            ring_setting,
            start_pos,
        ) = job()  # waits for job to finish and returns results
        if start_pos != "null":
            found = True
            print(
                (
                    "Machine setting found: rotors %s, ring %s, message key was %s, using crib %s"
                    % (rotor_setting, ring_setting, start_pos, cribtext)
                )
            )

    if found == False:
        print("Attack unsuccessfull")

    cluster.print_status()
    cluster.close()
