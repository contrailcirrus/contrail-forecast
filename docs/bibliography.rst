.. this snippet avoids duplicating the bibliography in two places
.. raw:: latex

   \cleardoublepage
   \begingroup
   \renewcommand\chapter[1]{\endgroup}
   \phantomsection

Bibliography
============

.. bibliography::
    :all:

.. can remove :all: in the future to only include cited references
