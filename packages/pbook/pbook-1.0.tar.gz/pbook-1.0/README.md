PBook
=====

LDAP phone book written in Python.


Output examples
---------------

Default search result:

    $ pbook john
    First name: John
     Last name: Doe
        E-mail: john.doe@example.com
     Telephone: +44123456789
                123
         Title: Placeholder name
          City: London
     User name: jdoe

Default search results using pattern search filter recognition:

    $ pbook 789
    First name: John
     Last name: Doe
        E-mail: john.doe@example.com
     Telephone: +44123456789
                123
         Title: Placeholder name
          City: London
     User name: jdoe

Default search result using LDAP field name decoration:

    $ pbook -d john
          givenName: John
                 sn: Doe
               mail: john.doe@example.com
    telephoneNumber: +44123456789
                     123
              title: Placeholder name
                  l: London
                uid: jdoe

Search result using custom search filter:

    $ pbook -S 'title=place*'
    First name: John
     Last name: Doe
        E-mail: john.doe@example.com
     Telephone: +44123456789
                123
         Title: Placeholder name
          City: London
     User name: jdoe

Search result using the `name` search template:

    $ pbook -s name doe
    First name: John
     Last name: Doe
        E-mail: john.doe@example.com
     Telephone: +44123456789
                123
         Title: Placeholder name
          City: London
     User name: jdoe

Search result using the `multicolumn` template:

    $ pbook -t multicolumn john
     Last name | First name |                         E-mail |            Telephone
    -----------+------------+--------------------------------+----------------------
           Doe |       John |           john.doe@example.com |    +44123456789, 123


Requirements
------------

* Python 2.7
* Python LDAP module (http://www.python-ldap.org)


Installation
------------

In order to install pbook, just download the code, make sure all dependencies
are installed (see [Requirements](https://github.com/jtyr/pbook#requirements)
above) and configure it:

    $ git clone https://github.com/jtyr/pbook.git
    $ cd pbook
    $ chmod +x ./pbook
    $ # edit the pbook.conf file
    $ ./pbook -c ./pbook.conf john

Or it's possible to use the Python setup script:

    $ git clone https://github.com/jtyr/pbook.git
    $ cd pbook
    $ python ./setup.py install
    $ # edit the /etc/pbook.conf file
    $ pbook john


Configuration
-------------

Look at the `pbook.conf` for a full configuration example. The configuration
can be defined globally (`/etc/pbook.conf`), per user (`~/.pbook`) or specified
by an option on the command line (`pbook -c /path/to/pbook.conf john`). The
configuration file is composed of the following 6 sections:


**connection**

In this section we configure the LDAP server connection. Server name, port and
connection protocol is determined from the `uri` parameter. Password can be
either defined in clear text or, if the value is set to `-1`, the user will be
prompted. The recommended approach is to configure `ldapsearch` correctly
first, and then re-use the parameters in this section. Example of the
`ldapsearch` command:

    $ ldapsearch -H ldaps://ldap.example.com -D uid=jdoe,ou=Users,dc=example,dc=com -b ou=Users,dc=example,dc=com -W uid=jdoe

From this command the configuration would be:

    [connection]
    uri=ldaps://ldap.example.com:636
    base_dn=ou=Users,dc=example,dc=com
    bind_dn=uid=jdoe,ou=Users,dc=example,dc=com
    password=-1


**search_template**

In this section we configure the LDAP search filter. The default search filter
is defined by `_default` (e.g. `_default=nane`) or by the command line option
`-s` (e.g. `pbook -s name john`). Example of search template definition:

    [search_template]
    _default=name
    name=(|(givenName=*%s*)(sn=*%s*))

It's also possible to specify a custom search filter on the command line with
the option `-S` (e.g. `pbook -S 'uid=%s' jdoe` or `pbook -S 'uid=jdoe'`).


**search_pattern**

On top of the default search filter, there is also pattern search filter
recognition. This allows the configuration of a specific search filter based on
a specified search string. For example, if all telephone numbers in the company
have the same format except for the last 3 digits, we can define a pattern
which will search the telephone number if the search string is a 3-digit
number:

    [search_pattern]
    (\d{3})=(telephoneNumber=+44123456\1)

Then we can search for a phone number `+44123456789` by executing `pbook 789`.


**label**

This section provides translation of the LDAP fields into a human readable
format, which is then used in the `pbook` output. For example `givenName=First
name` translates the `givenName` field to `First name` label.  It's mandatory
to have a label for every field used in the template (read more bellow).
Example of label definition:

    [label]
    givenName=First name
    sn=Last name
    telephoneNumber=Telephone


**template**

The default template is specified by the `_default` parameter (e.g.
`_default=basic`) or by the command line option `-t` (e.g. `pbook -t basic
john`). Templates can be defined in two forms. The first of which is a simple
list of LDAP fields which will be translated into a line-separated list of
labels and values. For example the following template:

    [template]
    _default=basic
    basic=(givenName,sn)

generates the following output:

    First name: John
     Last name: Doe

The second form is using the `printf` string format. For example the following
template:

    multicolumn=%(givenName)10.10s | %(sm)10.10s

generates the following output:

          John |        Doe

It is possible to specify a header for the output by a parameter named the same
the template itself appended with `_header`. The header can refer to labels by
the label name prefixed with two underscores. The header for the above example
could look like this:

    multicolumn_header=%(__givenName)10.10s | %(__sn)10.10s\n-----------+-----------

and the output would then look like this:

    First name |  Last name
    -----------+-----------
          John |        Doe


**output**

This section is optional and may contain definition of replacements for LDAP
values. In other words, it allows the manipulation of values coming from the
LDAP search by using a regular expression. For example, if we want to display
only last three digits of the `telephoneNumber`, we would define the following
output replacement:

    [output]
    telephoneNumber=.*(\d{3})$;\1


License
-------

This software is licensed by the MIT License which can be found in the file
[LICENSE](http://github.com/jtyr/pbook/blob/master/LICENSE).
