PyLawful is a small tool converting user inputs into SNMP messages to activate and manage 
Lawful Intercept Mediation Device and Tap configuration in routers.

The implementation is well proven to work against Cisco IOS-XR routers. It may also work
against Cisco IOS, IOS-XE routers or even other vendors. (MIB implementation may vary.)

PyLawful integrates the `pysnmp <https://pypi.python.org/pypi/pysnmp>`_ package to build
and parse SNMP messages.

The tool allows:

* Setting the Target router IP address
* Setting the SNMPv3 credentials
* Walk the ciscoTap2MIB and ciscoIpTapMIB MIBs
* Configure LI MD 
* Confirure IPv4/IPv6 Tap
* Remove MD and/or Taps
* List configured Taps
* Check cTap2StreamInterceptedPackets stats for configured Taps

PyLawful
--------

1. Install PyLawful from PyPI:

   If your default Python installation is v3.x

   .. code-block:: console

        $ pip install PyLawful

   If your default Python installation is v2.x

   .. code-block:: console

        $ pip3 install PyLawful
        
        
2. Running PyLawful:
   
   Start the python code to enter the menu
   
   .. code-block:: console

        $ python3 PyLawful
        
3. Example:

   .. code-block:: console

		python PyLawful.py

		####################################################

		Target router: 0.0.0.0

		Select operation:
		----------------------------------------------------
    		1. Set target router
    		2. Set SNMP Security
    		3. Walk LI MIBs
    		------------------------------------------------
    		4. Create and set Mediation Device
    		5. Delete Mediation Device
    		------------------------------------------------
    		6. Add and activate new LI Stream TAP(s)
    		7. Delete LI Stream TAP
    		------------------------------------------------
    		8. Show configured TAPs
    		9. Show Intercept Counters
    		------------------------------------------------
    		0. Exit
