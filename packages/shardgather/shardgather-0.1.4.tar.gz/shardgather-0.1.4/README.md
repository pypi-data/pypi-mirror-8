```
   _____ __  _____    ____  ____  _________  ________  ____________ 
  / ___// / / /   |  / __ \/ __ \/ ____/   |/_  __/ / / / ____/ __ \
  \__ \/ /_/ / /| | / /_/ / / / / / __/ /| | / / / /_/ / __/ / /_/ /
 ___/ / __  / ___ |/ _, _/ /_/ / /_/ / ___ |/ / / __  / /___/ _, _/ 
/____/_/ /_/_/  |_/_/ |_/_____/\____/_/  |_/_/ /_/ /_/_____/_/ |_|  
                                                                    
```

A script that runs a SQL statement against a collection of sharded databases and gathers the results


Installation
============

- (optional) Create a virtual environment:

```bash
virtualenv shardgather-env
source shardgather-env/bin/activate
```

From source
-----------

```bash
git clone https://github.com/kevinjqiu/shardgather.git
cd shardgather
pip install -r requirements.txt
python setup.py install
```


From PyPI (not yet)
-------------------

```python
pip install shardgather
```


Usage
=====

Generate a sample config
------------------------

    shardgather -g > config.ini

or

    shardgather --mkcfg > config.ini

Read queries from a SQL file
----------------------------

    shardgather -c config.ini query.sql

Read queries from standard input
--------------------------------

    shardgather -c config.ini -

Press Ctrl+D to terminate the input.
