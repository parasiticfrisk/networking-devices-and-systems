Assumes message was encrypted as follows:

STEP 1: Choose a start position and message key
        where:
        UYT is initial rotor position (chosen 'randomly')
        SCC is unencrypted message key (chosen 'randomly')

STEP 2: Encrypyt the message key
        pyenigma.py -r II V III -i 1 1 1 -p AV BS CG DL FU HZ IN KM OW RX -u B --start=UYT --text='SCC'
        PWE
        where:
        PWE is encrypted message key

        Note: We use a one-to-one relation for the rotor ring for compatability with Cryptoy

STEP 3: Encrypt the message using the unencrypted message key
	    pyenigma.py --key-file=keys.txt --start='SCC' --text='THISXISXWORKING'
 	    YJPYITREDSYUPIU
        where:
 	    SCC is the unencrypted message key
 	    YJPYITREDSYUPIU is the cypher text produced

STEP 4: Operator sends (usually in Morse):
 	    STNA DE STNB 1104 = 15 = UYT PWE = BNUGZ YJPYI TREDS YUPIU
        where:
 	    STNA is callsign of destination station
 	    DE means 'from' in Morse abreviation
 	    STNB is callsign of originating station
 	    = is the 'break' Morse character, which is used as a delimiter
 	    1104 is time message is sent (presumably UTC)
 	    BNUGZ contains UGZ 'Kenngruppen' (day indicator for confirmation of correct key sheet entry on decrypt)