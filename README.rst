hexsticker
----------

Produce hexagon stickers automatically from an image in compliance to the `Stickers Standard <https://sticker.how/>`_.


Installation
============

.. code-block:: console

  $ pip install hexsticker


After the installation step listed above, you will be able to use the `hexsticker` command:

.. code-block:: console

  $ hexsticker --help


Examples
========

Let's create a hexagon sticker for the `Selinon project <https://github.com/selinon>`_.

Here is the input image:

.. figure:: https://raw.githubusercontent.com/fridex/hexsticker/master/fig/input/selinon.png
   :alt: Selinon input logo
   :align: center

Let's create a hexagon sticker:

.. code-block:: console

  $ hexsticker selinon.png -o selinon-sticker-1.png
  INFO:hexsticker.create:Writing output to 'selinon-sticker-1.png'


The resulting image is:

.. figure:: https://raw.githubusercontent.com/fridex/hexsticker/master/fig/output/selinon-sticker-1.png
   :alt: Selinon hexagon sticker sticker 1
   :align: center
   :scale: 50%

As can be seen above, there are some parts cut off - let's add some padding to the image:

.. code-block:: console

  $ hexsticker input/selinon.png -o output/selinon-sticker-2.png --padding-size 25
  INFO:hexsticker.create:Writing output to 'selinon-sticker-2.png'


.. figure:: https://raw.githubusercontent.com/fridex/hexsticker/master/fig/output/selinon-sticker-2.png
   :alt: Selinon hexagon sticker sticker 2
   :align: center
   :scale: 50%


The padded part is white by default - that's why there are missing spikes of hexagon. Let's set color of padded area to the same color as background color of the original image:

.. code-block:: console

  $ hexsticker input/selinon.png -o output/selinon-sticker-3.png --padding-size 25 --padding-color '#66cfa7'
  INFO:hexsticker.create:Writing output to 'selinon-sticker-3.png'

.. figure:: https://raw.githubusercontent.com/fridex/hexsticker/master/fig/output/selinon-sticker-3.png
   :alt: Selinon hexagon sticker sticker 3
   :align: center
   :scale: 50%


Nice! What we could do next? Let's try to add a hexagon border:

.. code-block:: console

  $ hexsticker input/selinon.png -o output/selinon-sticker-4.png --padding-size 25 --padding-color '#66cfa7' --border-size 35
  INFO:hexsticker.create:Writing output to 'selinon-sticker-4.png'


.. figure:: https://raw.githubusercontent.com/fridex/hexsticker/master/fig/output/selinon-sticker-4.png
   :alt: Selinon hexagon sticker sticker 4
   :align: center
   :scale: 50%

Ehm, the default black one does not look that good in this case! Let's try some color that fits color scheme:

.. code-block:: console

  $ hexsticker input/selinon.png -o output/selinon-sticker-5.png --padding-size 25 --padding-color '#66cfa7' --border-size 35 --border-color '#197a9f'
  INFO:hexsticker.create:Writing output to 'selinon-sticker-5.png'


.. figure:: https://raw.githubusercontent.com/fridex/hexsticker/master/fig/output/selinon-sticker-5.png
   :alt: Selinon hexagon sticker sticker 5
   :align: center
   :scale: 50%

As you can see, this tool can automate creation of hexagon stickers so they respect the hexagon standard. Feel free to additionally adjust the resulting image of your logo or the input image.

Running from repo
=================

To run hexsticker from repository run the following commands:

.. code-block:: console

  $ git clone https://github.com/fridex/hexsticker  # or use ssh
  $ cd hexsticker
  $ export PYTHONPATH='.'
  $ ./hexsticker-cli --help
