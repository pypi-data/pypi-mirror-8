DreamTools
==========
Overview
---------

**dreamtools** aims at sharing code related to `DREAM <http://dreamchallenges.org>`_ challenges.

This repository is meant to contain (small) data sets and codes related to the scoring of the 
`DREAM challenges <http://dreamchallenges.org>`_. 

It was created at the time of DREAM8-9 and contains only Dream8 HPN challenge code for now. 
Note however that **dreamtools** contains information about DREAM6-7 (parameter estimation). 
More code/scripts about other challenges will be added later. 

The main goals are:

#. provide user a scoring function for the challenges
#. provide developer a place to share-reuse code used before/during/after the challenges

dreamtools-scoring executable
-------------------------------

For users, **dreamtools** provide one executable called **dreamtools-scoring**, which should be installed automatically
when installing dreamtools. Knowing the name of the challenge (and possibly sub-challenge), it works as  follows::

    dreamtools-scoring --challenge d8c1 --sub-challenge sc1a --submission ~/alphabeta-Network.zip
    
It prints some information and the score of the submision for instance for the example above::

     Solution for alphabeta-Network.zip in challenge d8c1 (sub-challenge sc1a) is :
     AUROC: 0.781937275711

Scoring functions available so far:


* Dream8 HPN (D8C1) sub challenges named sc1a, sc1b, sc2a, sc2b. 
  See `Synapse page <https://www.synapse.org/#!Synapse:syn1720047>`_ for details


Installation
---------------

::

    pip install dreamtools
    
    


