Sprarkprob - Sparklines for Probability Distributions
=====================================================

This package helps you to print out probability distribution on the
commandline.

Getting Started
---------------

::

    pip install sparkprob

Then in python:

::

    >>> from sparkprob import sparkprob
    >>> print sparkprob([0.2, 0.1, 0.4, 0.15, 0.15])
    ▁ ▁ ▂ ▁ ▁
    >>> print sparkprob([0.05, 0.2, 0.55, 0.1, 0.1])
      ▁ ▃ ▁ ▁
    >>> print sparkprob([0.05, 0.2, 0.7, 0.0, 0.0])
      ▁ ▅
    >>> print sparkprob([0.05, 0.0, 0.95, 0.0, 0.0])
        ▇

