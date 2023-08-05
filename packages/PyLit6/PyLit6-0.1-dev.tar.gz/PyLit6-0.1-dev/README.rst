PyLit6 - A Literate Programming Tool Using reStructuredText
###########################################################

:author: Roie Black
:version: 0.1-dev

..  include::   /references.inc

..  image:: https://travis-ci.org/rblack42/PyLit6.svg?branch=master

..  image:: https://pypip.in/v/pylit6/badge.png
    :target: https://pypi.python.org/pypi/pylit6/
    :alt: Latest Version
    :
..  image:: https://pypip.in/license/pylit6/badge.png
    :target: http://pypi.python.org/pypi/pylit6/
    :alt: License

This is the *PyLit6* project, designed to create an environment that supports
software development using Dr. Donald Knuth's :term:`Literate Programming`
concepts (See :cite:`Knuth:1984:LP`). However, rather than simply building a
tool that recreates Dr. Knuth's ideas, I have added a few ideas of my own.
These additions to |LP| are based on my teaching work, and my goal to produce
students who are familiar with modern tools used in software engineering, and
who are ready to produce code worthy of including in real-world projects.

Project History
***************

The PyLit_ project began as a personal research project when Dr. Knuth's first
papers on |LP| were published in 1984. I was then, and remain today,
convinced that |LP| had a real place in the academic world, even if it did take
off as a mainstream development technique. At the time, I was serving in the
USAF, and was assigned as a computer science instructor at the `Air Force
Institute of Technology <www.afit.edu>`_, the USAF's graduate school. I was
working to find a way to understand why students wrote their lab projects the
way they did, when all I had to go by was a final printed program listing. It
struck me that having students use |LP| to explain their code would be
extremely useful. They would have to think more and code less, and their
writings would help me identify deficiencies in their thinking, and ultimately
help build better software engineers.

The project originally had a different name. I thought `nLITEn` was a good name
for what I had in mind for the tool. By the time I thought about registering a
domain name for the project, some years later, `nliten.org` had already been
taken, so that name languished.

The first development language used in this project was Pascal, then widely
used in academia.  Over the years, I switched to C, then C++. In 2003, the
development language switched again to Python, and I renamed the project to
PyLit_, a contraction of "Python Literate Programming". The first Python
version of the PyLit_ software was written in 2003 as part of my master's
thesis project in software engineering at Texas State University (see
:cite:`Black:2005`). (My first degrees were in Aerospace Engineering, but I
wanted to get back into teaching computer science after retiring from the
USAF). The software went live on the Internet in 2004, and I registered two
domains to support further work: `pylit.org` in 2005 for the core project, and
`co-pylit.org` in 2009 for supporting tools I was thinking of including in the
project. (I am a pilot, so these two names seemed appropriate to me, beyond
their obvious "Python Literate Programming" genesis.) 

The original PyLit_ tool was a web application based on the :term:`wiki` system
developed by Ward Cunningham. I added instrumentation that helped track how
developers spent their time and ended up with a management tool based on the
`Personal Software Process` and `Team Software Process` concepts popular at the
time. 

Today, PyLit_ is still a web application, but has now been reengineered using
Flask_ and reStructuredText_, with a little help from Git_.

For more information on the project, contact the author.

Roie Black
Professor, Computer Science
Austin Community College
Austin, Texas

email: rblack@austincc.edu
web: www.austincc.edu/rblack
