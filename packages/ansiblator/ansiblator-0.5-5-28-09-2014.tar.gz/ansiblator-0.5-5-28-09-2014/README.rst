
Ansiblator
==========

This wrapper allows more quicker and easier way to use ansible in python
ansible without playbooks, so more like fabric.

Ansible is then more powerfull and it will allow to chain commands with
python commands. Ansible documentation is on http://docs.ansible.com/

Get started
===========

For instalation you can download package and then just unpack and use

    python setup.py install

or

    pip install ansiblator


Quick use case
==============

For most quickest example you can just create your ansible file named
ansible_hosts inside your home directory or full path.

Ansiblater is mainly using file such as in ~/ansible_hosts

code::

    from ansiblator.api import Ansiblator
    ans = Ansiblator()
    ret = ans.local("uname -a", now=True, use_shell=True)
    ans.run("uname -a", now=True)
    ans.runner("uptime")
    ans.run_all()
    ans.copy(src="/tmp/aabc.csv", dest="/tmp/",pattern="pc",now=True)

use dictionary to create ::

    inv = {'pc':[{'ssh_host':'192.168.0.10', 'ssh_user':'test_user', 'su_user':'root'},
                {'ssh_host':'192.168.0.12', 'ssh_user':'test_user2', 'su_pass':'paasswd','su_user':'root'}]}
    ans = Ansiblator(inventory=inv)
    ans.run("uname -a", now=True)


More useable way
================

Ansiblator automatically save return json values for actuall runs, so
you can use them for testing and conditions. For example

testing::

    return_code = ans.local("uname -a", now=True, use_shell=True)
    return_code['contacted']

    or

    return_code = ans.local(["uname", "-a"], now=True, use_shell=False)
    return_code['contacted']

Info
====
For more information consult functions or ansible documentation.
more information can be also used on http://www.pripravto.cz. You can also
contact us there.


