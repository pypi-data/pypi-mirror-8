============
``gs.dmarc``
============
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Look up and report on the DMARC status of a domain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-09-29
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
============

This product allows systems look up and report on the DMARC
(Domain-based Message Authentication, Reporting and Conformance)
status of a domain [#dmarc]_. DMARC allows the owner of a domain
to publish a key that is used to verify if an email message
actually originated from the domain, and to publish what to do if
the verification fails. It is an extension of DKIM (DomainKeys
Identified Mail [#dkim]_) and SPF (Sender Policy Framework
[#spf]_).

Specifically this product supplies ``gs.dmarc.ReceiverPolciy``
for enumerating [#enum34]_ the different DMARC policies, and the
``receiver_policy`` function for querying the policy for a
given domain.

Resources
=========

- Documentation: http://gsdmarc.readthedocs.org/
- Code repository: https://github.com/groupserver/gs.dmarc
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver
 
.. [#dmarc] See `the internet-draft`_ Domain-based Message
            Authentication, Reporting and Conformance (DMARC)
.. _the internet-draft: https://datatracker.ietf.org/doc/draft-kucherawy-dmarc-base/?include_text=1
.. [#dkim] See `RFC 6376`_: DomainKeys Identified Mail (DKIM) Signatures
.. _RFC 6376: http://tools.ietf.org/html/rfc6376
.. [#spf] See `RFC 4408`_: Sender Policy Framework (SPF) for
          Authorizing Use of Domains in E-Mail, Version 1
.. _RFC 4408: http://tools.ietf.org/html/rfc4408
.. [#enum34] `The enum34 package`_ is used to provide `Enum`_
           support for releases of Python prior to 3.4.
.. _The enum34 package: https://pypi.python.org//pypi/enum34
.. _Enum: https://docs.python.org/3/library/enum.html
.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  LocalWords:  DMARC DKIM DomainKeys dkim groupserver spf enum
..  LocalWords:  lookup
