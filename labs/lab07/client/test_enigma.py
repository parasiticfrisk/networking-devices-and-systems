#!/usr/bin/env python3
#
# Py-enigma: Brian Neal
#            http://py-enigmareadthedocs.org/
#            License: MIT License
#
# This code is the original example provided with the Py-enigma
# Python3 library and utilities. It is included here to confirm
# correct operation of Py-enigma on your system before proceeding
# with the brute force attack code.
#


from enigma.machine import EnigmaMachine

################################
# Decrypt
################################

# setup machine to be the same as that used for encrypt

machine = EnigmaMachine.from_key_sheet(
    rotors="II V III",
    reflector="B",
    ring_settings="1 1 1",
    plugboard_settings="AV BS CG DL FU HZ IN KM OW RX",
)

# set machine initial starting position
machine.set_display("UYT")

# decrypt the message key
msg_key = machine.process_text("PWE")

# decrypt the cipher text with the unencrypted message key
machine.set_display(msg_key)

ciphertext = "YJPYITREDSYUPIU"
plaintext = machine.process_text(ciphertext)

print(plaintext)
