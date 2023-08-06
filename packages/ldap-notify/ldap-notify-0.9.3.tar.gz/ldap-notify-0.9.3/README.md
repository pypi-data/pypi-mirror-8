ldap-notify
===========

[![Build Status](https://travis-ci.org/sttts/ldap-notify.svg)](https://travis-ci.org/sttts/ldap-notify)

NAME
----

ldap-notify - LDAP Password/Login Expiration Notification Tool

SYNOPSIS
--------

Usage: ldap-notify [OPTION]... -c *config_file.conf*

DESCRIPTION
-----------

`ldap-notify` searches users in an LDAP directory whose login or password expires in a certain number of days. These users are notified with a customizable email. The time intervals for the notifications and the email templates can be freely defined. By using a custom LDAP attribute the last notification is stored in the directory such that users are only notified once per rule. Moreover, this mechanism allows running the tool (e.g. via cron) on multiple machine with a certain time delta in order to implement high availabiliy. 

OPTIONS
-------

`-h`, `--help`
  show this help
 
`-c`, `--conf` *config-file*
  mandatory parameter: the config file name

`-k`
  ignore SSL/TLS certificates

`--dry`
  do not send emails or modify anything in ldap

`--test` *test-address*
  send all mails to the given address

`--restrict` *DN*;*CN*;...
  restrict notifications to these semicolon separated user DNs or CNs
  
`--time` *timestamp*
  simulate current UTC time (format: `20141031162633Z`)
  
`-v`, `--verbose`
  enable verbose logging

`-d`, `--debug`
  enable debug logging

`--print-conf`
  print the used configuration to console and exit

Configuration
-------------

The behaviour of ldap-notify is defined via a *config-file*. The parameters above will override the options in the configuration file.

The configuration file given by the mandatory `-c` or `--conf` parameter uses the common INI file format. This means that it consists of sections with key/values pairs in the following format:

```
[section_name]
attribute=value
second_attribute = multi
    line
    value
    
# comment
```

The multi-line value is useful for long lists like in the `restrict_to_users` value.

The default configuration is the following (call `ldap-notify` with the `--print-conf` parameter to print it):

```
[common]
server = ldap://localhost
bind_dn =
bind_password =
bind_password_base64 =
base_dn =
subtree_search = false 
starttls = false
ignore_cert = false
expiry_attribute = passwordExpirationTime
notify_attribute = pwmNotify
dry = false
restrict_to_users =
user_objectclass = person
object = password
objects =

[smtp]
server =
ssl = false
starttls = false
user =
password =
password_base64 =

[admin]
from_address = root@<HOSTNAME>
to_address = admin@<HOSTNAME>
from_text = $Object Expiry Notification
subject = $Object Expiry Notification Report
text_template = <LDAP_NOTIFY_DIR>/templates/admin.tmpl.txt

[test]
enabled = false
to_address = root@<HOSTNAME>
```

The configuration options have the following meaning:

### Common Section

| Option  | Format   | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `server`  | RFC 4516 | the server LDAP URI | `ldap://host:389` or `ldaps://host` |
| `bind_dn` | DN or empty | the DN to bind to; can be empty | `cn=admin,ou=users,dc=localhost` |
| `bind_password` | string | the password to be used during binding | secret |
| `bind_password_base64` | base64 encoded string | an encoded bind password | `YWRtaW5fc2VjcmV0` |
| `base_dn` | DN list | the base DNs to start a search at | `ou=users,dc=localhost;ou=admins,dc=localhost` or empty |
| `subtree_search | boolean | do a SUBTREE or ONELEVEL search | true or false |
| `starttls` | boolean | use starttls on a ldap:// connection | true or false |
| `ignore_cert` | boolean | don't check server SSL/TLS certificate | true or false |
| `expiry_attribute` | LDAP attribute | the attribute holding the expiration timestamp | passwordExpirationTime |
| `notify_attribute` | LDAP attribute | the attribute used to store sent notifications | pwmNotify |
| `dry` | boolean | don't send mails or modify LDAP |
| `restrict_to_users` | DN or CN list | restrict sent mail and LDAP modifications | `cn=admin,ou=users,dc=localhost;root;hschmidt;` |
| `user_objectclass` | LDAP objectClass | an object class name to restrict the user search | pwmUser or person |
| `object` | string | the object this config talks about | password or login |
| `objects` | string | the plural string of object | passwords or logins |

The `DN list` of `base_dn` is separated by semi-colons, spaces or newlines. An empty `base_dn` implies `substree_search = true` and means to start the search at the dictionary root.

The `DN or CN list` of `restrict_to_users is separated by semi-colons, spaces or newlines. A non-trivial example with a multi-line value is the following:

```
restrict_to_user = cn=alice,ou=users,dc=localhost
	cn=bob,ou=users,dc=localhost
	root;admin;operations
```

The `object` and `objects` values are only used in templates in order to allow unified templates for e.g. password and login configuration.

### SMTP Section

| Option  | Format   | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `server` | HOSTNAME[:PORT] | the mail server address | smtp.gmail.com |
| `ssl` | boolean | true if the server speaks SSL | true or false |
| `starttls` | boolean | use starttls after connecting with encryption | true or false |
| `user` | string | the SMTP user name to authenticate with | hschmidt |
| `password` | string | the SMTP password to authenticate with | secret |
| `password_base64` | base64 encoded string | the SMTP password encoded with base64 | YWRtaW5fc2VjcmV0 |

### Admin Section

| Option  | Format   | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `from_address` | email address | the sender address for the admin report | `admin@company.com` |
| `to_address` | email address | send the admin report here | `admin_group@company.com` |
| `from_text` | sender name | the sender name for the admin report | Password Expiry Notification Service |
| `subject` | string | the admin report subject | Password Expiry Notification Report |
| `text_template` | absolute filename | the admin report email body template | `/etc/ldap-notify/admin.tmpl.txt` |

### Test Section

| Option  | Format   | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `enabled` | boolean | if true, all emails are sent to the test email address | true or false |
| `to_address` | email address | the test email address | `root@localhost` |

The `object` string in the `common` section can be used in the templates such that they work for password and login notification emails.

### Rule Sections

An arbitrary number of rules can be defined in the configuration file. The rules are named according to their number of days before an expiration date when the rule applies. E.g. a 30 day rule is called "30".

The default values of a 30 day rule:

```
[30]
from_address = *ADMIN FROM ADRESS*
from_text = *ADMIN FROM TEXT*
subject = $Object will expire soon
text_template = <LDAP_NOTIFY_DIR>/templates/notify.tmpl.txt
html_template =
```

A quite minimal rules configuration with only one template (the default `notify.tmpl.txt`), but customized subject lines looks like this:

```
[30]
subject = $weeks_left weeks left

[7]
subject = $days_left days left

[1]
subject = Tomorrow
```

The rule options have the following meaning:

| Option  | Format   | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `from_address` | email address or empty | the notification mail from address | `admin@company.com` |
| `from_text` | string | the notification mail from text | Password Notification |
| `subject` | string | the subject of a notification | expires in $days_left days
| `text_template` | absolute filename | the notification mail text template | `/etc/ldap-notify/notify-30.tmpl.txt` |
| `html_template` | absolute filename | the notification mail html template | `/etc/ldap-notify/notify-30.tmpl.html` |

The subject of the notification emails will be interpolated with the same variables as in the email template itself (cf. below).

By default, HTML mail templates are disabled. Next to the default text template there is also an example notify.tmpl.html. By assigning a template to the html_template option, HTML mail templates will be enabled.

Test Operation
--------------

During test of the script it is highly suggested to use the `--test`, the `--dry` and `--restrict` options or the respective options in the configuration file.

These three options are orthogonal and can be combined depending on the test case at hand:

- `--test` *test-address*: all emails that are sent by `ldap-notify` are sent to the test address, not the actual addresses of the matching users. Moreover, no LDAP modifications are done.
- `--dry`: no emails are sent at all, not even to a test user. Moreover, no LDAP modifications are done.
- `--restrict` *DNs*;*CNs*;...: all users are processed as in normal operation, but emails are only sent to the admin (for the admin report) and the given users as *DN*s or *CN*s. Moreover, no LDAP modifications are done to users not in this list.

For debugging and testing it is useful to use verbose and debug output:

- `-v`: show log output on level ERROR, WARN, INFO. Normally, INFO log output is supressed.
- `-d`: show log output on level ERROR, WARN, INFO and DEBUG. Normally, INFO and DEBUG log output is supressed.

The debug parameter `-d` can be passed multiple times in order to increase the debug level even further.

Templates
---------

Email templates, email subjects and email from strings for rules are interpolated with a number of variables. 

### User Rule Emails

In the case of user notification emails the following variables are interpolated:

| Variable  | Format | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `$expiry_date` | string | the localized (according to the LANG setting) date of the expiration timestamp | `12.10.2014` for LANG=de_DE |
| `$days_left` | integer | number of days from today to the expiration timestamp, rounded down | 4 |
| `$weeks_left` | integer | number of weeks from today to the expiration timestamp, rounded down | 2 |
| `$months_left` | integer | number of months from today to the expiration timestamp, roundded down | 1 |
| `$rule_days` | integer | the days of the applying rule | 14 |
| `$cn` | string | the common name of the user being notified | hschmidt |
| `$dn` | DN | the DN of the user being notified | `cn=hschmidt,ou=users,dc=localhost` |
| `$fullname` | string | the full name of the user being notified | Hans Schmidt |
| `$object` | string | the object in singular, defined by `object` in the configuration | password |
| `$objects` | string | the object in plural, defined by `objects` in the configuration | passwords |
| `$Object` | string | the singular object with capital letter | Password |
| `$Objects` | string | the plural object with capital letter | Passwords |
| `$grace` | integer | the number of grace commits | 3 |

The `object` and `objects` variables are defined by the very same options in the configuration. If `objects` is empty, a single `s` character is appended to the `object` value.

### Admin Report Emails ###

In the case of admin report emails the following variables are interpolated::

| Variable  | Format | Description | Examples |
|:------- |:-------- |:----------- |:---------|
| `$notified_users` | multiline string | users which were notified via email | `cn=alice,ou=users,dc=localhost, alice@company.com, 14 Days Rule, Expiry Date: 2014-10-13 14:20:25` |
| `$failed_users` | multiline string | users where notification failed | as in `$notified_users` |
| `$users_without_email` | multiline string | users to be notified, but without email | `cn=alice,ou=users,dc=localhost, 14 Days Rule, Expiry Date: 2014-10-13 14:20:25` |
| `$no_grace_logins` | multiline string | users without grace logins | `cn=alice,ou=users,dc=localhost, alice@company.com, Expiry Date: 2014-10-13` |
| `$notified_users_length` | integer | number of rows in `$notified_users` | 52 |
| `$failed_users_length` | integer | number of rows in `$failed_users` | 0 |
| `$users_without_email_length` | integer | number of rows in `$users_without_email` | 7 |
| `$no_grace_logins_length` | integer | number of rows in `$no_grace_logins` | 5 |
| `$object` | string | the object in singular | password |
| `$objects` | string | the object in plural | passwords |
| `$Object` | string | the singular object with capital letter | Password |
| `$Objects` | string | the plural object with capital letter | Passwords |

The `object` and `objects` variables are defined by the very same options in the configuration. If `objects` is empty, a single `s` character is appended to the `object` value.

The `..._length` variables count the number of lines in the respective `..._users` variables. These can be used to shows counters (e.g. of failed notifications) at the very top of the admin report.

Search Algorithm
----------------

The search algorithm in `ldap-notify looks for users of each rule which satisfy the following conditions:

- have an expiration timestamp within the number of days in the rule,
- do not match with other rules,
- are not disabled,
- have not received the same notification before.

In addition in case of any of the following conditions only the admin is notified via the admin report, no user notification is sent out:

- have an email address,
- have grace login available.

### Notify Attribute

The algorithm stores the last sent notification and a timestamp in the `notify_attribute` (defined in the `common` config section). The value has the following format:

```
20140116111356Z:30
```

It tells the algorithm that this user was notified at the given timestamp with a 30 days rule.

### Notification Logic

Assume that three rules are defined: 30, 7, 1 and `passwordExpirationTime` is used as the expiry attribute. Then three independent LDAP searches are performed, each of them with a filter of the following shape:

```
(& (objectClass=person)
   (!(loginDisabled=true))
   (& (passwordExpirationTime>=20141112173529Z)
      (!(passwordExpirationTime>=20141116173529Z))
      (!(loginGraceRemaining=0))
   )
)
```

The timestamps used are:

- 1 days: `passwordExpirationTime >= *NOW*` and `passwordExpirationTime < *24 HOURS FROM NOW*`
- 7 days: `passwordExpirationTime >= *24 HOURS FROM NOW*` and `passwordExpirationTime < *7 DAYS FROM NOW*`
- 30 days: `passwordExpirationTime >= *7*` and `passwordExpirationTime < *30 DAYS FROM NOW*`.

To detect that the same notification was sent before, but to cope with old notify attribute values at the same time, the notify attribute is read, e.g. `20130116111356Z:30`. This notify attribute timestamp is considered _old_ if

- `expirationTime - last_notify >= 30 days`
- *or* the current applied rule (e.g. 7) is smaller than the last notified rule: `7 < 30`.

If neither condition matches, the notifiy attribute is current and the user is skipped.
If at least one condition matches, the user is notified and a new notify attribute is written.

### Fault Tolerance

Users are notified only once for each rule. This allows to launch `ldap-notify` on multiple servers, *with a time delta to avoid overlap and race conditions*. If the first server fails, the second launch on the second server will notice this and send the notifications on behalf of the first instance.

Moreover, `ldap-notify` will handle SMTP errors gracefully: if the SMTP connection fails, the notification attribute is not updated.

If the notification attribute cannot be parsed (i.e. its format is invalid), the notification attribute is deleted before processing the user.

Development
-----------

`ldap-notify` is written in Python. The `ldap-notify` has no dependencies other than python-ldap. After cloning the Github repository with the source code, some more dependencies are needed for development which can be installed with pip:

```
virtualevn ../env
. ../env/bin/activate
pip install -r requirements.txt
```

After installation the dependencies, the unit tests can be run to verify that everything works as expected:

```
nosetests --rednose -v ldap_notify/tests
```

Everything should be green.

To launch the `ldap-notify` itself, do the following:

```
python -mldap_notify.main -c login.conf
```

Make sure that `login.conf` in the current directory is valid.

To update the man page from README.md, install `md2man`and run:

```
grep -v 'Build Status' README.md | md2man-roff > man5/ldap-notify.5
man -M . ldap-notify
```

AUTHOR
------

Dr. Stefan Schimanski <stefan.schimanski@gmail.com>

SEE ALSO
--------

- https://github.com/sttts/ldap-notify
- https://build.opensuse.org/package/show/home:sttts/ldap-notify
