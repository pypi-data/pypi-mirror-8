The Python EBICS package
========================

This package contains all the functionality that is required to work with
EBICS and SEPA. The usage has been realised as simple as possible but also
as flexible as necessary.

Features
--------

- Obtain bank account statements (CAMT and MT940)
- Submit SEPA credit transfers (pain.001)
- Submit SEPA direct debits CORE, COR1, B2B (pain.008)
- Mostly full SEPA support
- Automatic calculation of the lead time based on holidays and cut-off times
- Integrated mandate manager (beta)
- Validation of IBAN and BIC
- Bankcode/Account to IBAN converter according to the rules of the German Central Bank
- DATEV converter (KNE)

PyEBICS provides you the possibility to manage all of your everyday commercial
banking activities such as credit transfers, direct debits or the retrieval of
bank account statements in a flexible and secure manner.

All modules can be used free of charge. Only the unlicensed version of the
EBICS client has few restrictions. The upload of SEPA documents is limited
to a maximum of five transactions and bank account statements can not be
retrieved for the last three days.

Example
-------

.. sourcecode:: python
    
    from ebics.client import EbicsClient

    client = EbicsClient(
        keys='~/mykeys',
        passphrase='secret',
        url='https://www.mybank.de/ebics',
        hostid='MYBANK',
        partnerid='CUSTOMER123',
        userid='USER1',
        )
    # Send the public electronic signature key to the bank.
    client.INI()
    # Send the public authentication and encryption keys to the bank.
    client.HIA()

    # Create an INI letter that must be printed and sent to the bank.
    client.create_ini_letter('MyBank AG', '~/ini_brief.pdf')

    # After the account has been activated the public bank keys
    # must be downloaded and checked for consistency.
    print client.HPB()
    
    # Finally the bank keys must be activated.
    client.activate_bank_keys()
    
    # Download MT940 bank account statements
    data = client.STA(
        start='2014-02-01',
        end='2014-02-07',
        )


Changelog
---------

v2.0.3 [2014-09-11]
    - Fixed a bug refusing valid creditor ids.
    - Added a test to check DATEV parameters for invalid arguments.

v2.0.2 [2014-09-05]
    - Fixed a bug in some EBICS requests (missing parameter tag).
    - Fixed a bug in the MT940 parser.

v2.0.1 [2014-08-18]
    - Fixed a bug handling XML namespaces.
    - Changed the behaviour of the flag *parsed* of some methods. Now a structure of dictionaries is returned instead of an objectified XML object.
    - Changed the expected type of the *params* parameter. Now it must be a dictionary instead of a list of tuples.
    - Added support for distributed signatures (HVU, HVD, HVZ, HVT, HVE, HVS).

v1.3.0 [2014-07-29]
    - Fixed a few minor bugs.
    - Made the package available for Windows.

v1.2.0 [2014-05-23]
    - Added new DATEV module.
    - Fixed wrong XML position of UltmtCdtr node in SEPA documents.
    - Changed the order of the (BANKCODE, ACCOUNT) tuple to (ACCOUNT, BANKCODE) used by the Account initializer.

v1.1.25 [2014-02-22]
    Minor bug fix of the module loader.

v1.1.24 [2014-02-21]
    First public release.
