|vera|

`wq.db: vera <http://wq.io/vera>`__ is the reference implementation of
the Entity-Record-Attribute-Value (`ERAV <http://wq.io/docs/erav>`__)
data model. ERAV is an extension to Entity-Attribute-Value (EAV) that
adds support for maintaining multiple versions of an entity with
different provenance  [1]_.

The implementation of ERAV provided by vera is optimized for storing and
tracking changes to *time series data* as it is exchanged between
disparate technical platforms (e.g. mobile devices, Excel spreadsheets,
and third-party databases). In this context, ERAV can be interpreted to
mean Event-Report-Attribute-Value, as it represents a series of *events*
being described by the *reports* submitted about them by various
contributors in e.g. an environmental monitoring or citizen science
project.

Getting Started
===============

.. code:: bash

    pip install vera

See `the documentation <http://wq.io/docs/>`__ for more information. See
https://github.com/wq/vera to report any issues. Note that the vera
codebase is contained within
`wq.db.contrib <https://github.com/wq/wq.db/blob/master/contrib/vera>`__.
The vera PyPI package simplifies the installation of additional
third-party libraries needed for vera but not required by wq.db core.

References
----------

.. [1]
   Sheppard, S. A., Wiggins, A., and Terveen, L. `Capturing Quality:
   Retaining Provenance for Curated Volunteer Monitoring
   Data <http://wq.io/research/provenance>`__. To appear in Proceedings
   of the 17th ACM Conference on Computer Supported Cooperative Work and
   Social Computing (CSCW 2014). ACM. February 2014.

.. |vera| image:: https://raw.github.com/wq/wq/master/images/256/vera.png
   :target: http://wq.io/vera
