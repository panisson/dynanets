## $Dyna^2$: Dynamic Processes over Dynamic Networks

---

Description
-----------
This is a python library for simulation and evaluation of dynamic processes over dynamic networks.

The following models that simulate node contacts are available:

- Dynamic G(n,p), a dynamic version of the Erdős–Rényi model.
- Dynamic G(n,m), another dynamic version of the Erdős–Rényi model.
- The edge-Markovian dynamic graph model [[1]](#references)
- The continuous-time edge-Markovian dynamic graph model [[2]](#references)

In addition to simulated models, some datasets from the SocioPatterns collaboration (http://www.sociopatterns.org/)
are also packaged in this library.

Installation
------------

setuptools - from Git repository

```bash
> git clone git://github.com/panisson/dynanets.git
> cd dynanets
> python setup.py install
```

Dependencies
------------
NumPy, Pandas and Matplotlib

Examples
--------
See the Jupyter notebooks in the notebooks folder.

Contributing
------------
If you have a Github account please fork the repository,
create a topic branch, and commit your changes.
Then submit a pull request from that branch.

License
-------
Written by André Panisson <panisson@gmail.com>  
Copyright (C) 2018 Istituto per l'Interscambio Scientifico I.S.I.  
You can contact us by email (isi@isi.it) or write to:  
ISI Foundation, Via Chisola 5, 10126 Torino, Italy.  

The Model B was implemented with the contribution of Juliette Stehle.

References
----------

[1] Andrea E.F. Clementi, Claudio Macci, Angelo Monti, Francesco Pasquale, and Riccardo Silvestri. 2008. 
    Flooding time in edge-Markovian dynamic graphs. In Proceedings of the 
    twenty-seventh ACM symposium on Principles of distributed computing (PODC '08). 
    ACM, New York, NY, USA, 213-222.

[2] Augustin Chaintreau, Abderrahmen Mtibaa, Laurent Massoulie, and Christophe Diot. 2007. 
    The diameter of opportunistic mobile networks. In Proceedings of the 
    2007 ACM CoNEXT conference (CoNEXT '07). ACM, New York, NY, USA, , Article 12 , 12 pages.
