pyramid_httpauth
================

This is an authentication policy for __pyramid__ that verifies credentials
using either HTTP-Digest-Auth or HTTP-Basic-Auth protocol.

With a reference to https://github.com/mozilla-services/pyramid_digestauth/

with extras:

    1. Add support for HTTP Basic Authentication
    2. Add support for Python 3
    3. Tested with Python 2.7 and Python 3.4

Usage
-----

To use this package, in the app function, just include it.

    config.include("pyramid_httpauth")

In you *development.ini*

    * httpauth.schema:          default schema to challenge client (digest
                                or basic), default=digest
    * httpauth.realm:           realm string for auth challenge header
    * httpauth.qop:             qop string for auth challenge header
                                (used for Digest Auth only)
    * httpauth.nonce_manager:   name of NonceManager class to use
                                (used for Digest Auth only)
    * httpauth.nonce_manager_secret: The secret key used to sign on nounce, used
                                     for built-in SignedNonceManager (if httpauth.nonce_manager
                                     is not provided).
    * httpauth.domain:          domain string for auth challenge header
    * httpauth.get_password:    name of password-retrieval function
    * httpauth.groupfinder:     name of group-finder callback function
