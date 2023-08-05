========
Tutorial
========

Installation
============

Vdirsyncer requires Python 2.7+ or 3.3+.

Unless you want to contribute to vdirsyncer, you should use the packages from
your distribution:

- `AUR package for ArchLinux <https://aur.archlinux.org/packages/vdirsyncer>`_.
- `pkgsrc <http://pkgsrc.se/time/py-vdirsyncer>`_.

If your distribution doesn't provide a package for vdirsyncer, you still can
use Python's package manager PIP. You'll have to check that a compatible
version of Python is installed (see above), and then run::

    pip install --user vdirsyncer

This will install vdirsyncer and its dependencies into your home directory,
presumably into ``~/local/lib/pythonX.X/``, and an executable under
``~/.local/bin/``. You then can uninstall vdirsyncer with ``pip uninstall
vdirsyncer``, but this will leave vdirsyncer's dependencies on your system,
whose files you'll have to remove manually from the mentioned directories. You
could check out pipsi_, but that one is a quite new tool. You should always
prefer the packages of your distribution over this method.

.. _pipsi:: https://github.com/mitsuhiko/pipsi

Configuration
=============

.. note::
    The `example.cfg from the repository
    <https://github.com/untitaker/vdirsyncer/blob/master/example.cfg>`_
    contains a very terse version of this.

By default, *vdirsyncer* looks for its configuration file at
``~/.vdirsyncer/config``. You can use the ``VDIRSYNCER_CONFIG`` environment
variable to change this path.

The config file should start with a :ref:`general section <general_config>`,
where the only required parameter is ``status_path``. The following is a
minimal example::

    [general]
    status_path = ~/.vdirsyncer/status/

After the general section, an arbitrary amount of *pair and storage sections*
might come.

In vdirsyncer, synchronization is always done between two storages. Such
storages are defined in :ref:`storage sections <storage_config>`, and which
pairs of storages should actually be synchronized is defined in :ref:`pair
section <pair_config>`.

This format is copied from OfflineIMAP, where storages are called
repositories and pairs are called accounts.

The following example synchronizes a single CardDAV-addressbook to
``~/.contacts/``::

    [pair my_contacts]
    a = my_contacts_local
    b = my_contacts_remote

    [storage my_contacts_local]
    type = filesystem
    path = ~/.contacts/
    fileext = .vcf

    [storage my_contacts_remote]
    type = carddav
    url = https://owncloud.example.com/remote.php/carddav/addressbooks/bob/default/
    username = bob
    password = asdf

After running ``vdirsyncer sync``, ``~/.contacts/`` will contain a bunch of
``.vcf`` files which all contain a contact in ``VCARD`` format each. You can
modify their content, add new ones and delete some, and your changes will be
synchronized to the CalDAV server after you run ``vdirsyncer sync`` again. For
further reference, it uses the storages
:py:class:`vdirsyncer.storage.FilesystemStorage` and
:py:class:`vdirsyncer.storage.CarddavStorage`.

But what if we want to synchronize multiple addressbooks from the same server?
Of course we could create new pairs and storages for each addressbook, but that
is very tedious to do. Instead we will use a shortcut:

- Remove the last segment from the URL, so that it ends with ``.../bob/``
  instead of ``.../bob/default/``.

- Add the following line to the *pair* section::

      [pair my_contacts]
      ...
      collections = default,work

This will synchronize
``https://owncloud.example.com/remote.php/carddav/addressbooks/bob/default/``
with ``~/.contacts/default/`` and
``https://owncloud.example.com/remote.php/carddav/addressbooks/bob/work/`` with
``~/.contacts/work/``. Under the hood, vdirsyncer also just copies the pairs
and storages for each collection and appends the collection name to the path or
URL.

It almost seems like it could work. But what if the same item is changed on
both sides? What should vdirsyncer do? By default, it will show an ugly error
message, which is surely a way to avoid the problem. Another way to solve that
ambiguity is to add another line to the *pair* section::

    [pair my_contacts]
    ...
    conflict_resolution = b wins

Earlier we wrote that ``b = my_contacts_remote``, so when vdirsyncer encounters
the situation where an item changed on both sides, it will simply overwrite the
local item with the one from the server. Of course ``a wins`` is also a valid
value.

Calendar sync works almost the same. Just swap ``type = carddav`` for ``type =
caldav`` and ``fileext = .vcf`` for ``fileext = .ics``.
