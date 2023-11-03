.. |acdclogo| image:: https://raw.githubusercontent.com/SchmollerLab/Cell_ACDC/6bf8442b6a33d41fa9de09a2098c6c2b9efbcff1/cellacdc/resources/logo.svg
   :width: 80

|acdclogo| Cell-ACDC
=====================

A GUI-based Python framework for **segmentation**, **tracking**, **cell cycle annotations** and **quantification** of microscopy data
-------------------------------------------------------------------------------------------------------------------------------------

*Written in Python 3 by* \ `Francesco Padovani <https://github.com/ElpadoCan>`__ \ *and* \ `Benedikt Mairhoermann <https://github.com/Beno71>`__\ *.*

.. image:: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-windows_pyqt5.yml/badge.svg
   :target: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-windows_pyqt5.yml
   :alt: Build Status (Windows PyQt5)

.. image:: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-ubuntu_pyqt5.yml/badge.svg
   :target: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-ubuntu_pyqt5.yml
   :alt: Build Status (Ubuntu PyQt5)

.. image:: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-macos_pyqt5.yml/badge.svg
   :target: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-macos_pyqt5.yml
   :alt: Build Status (macOS PyQt5)

.. image:: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-windows_pyqt6.yml/badge.svg
   :target: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-windows_pyqt6.yml
   :alt: Build Status (Windows PyQt6)

.. image:: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-macos_pyqt6.yml/badge.svg
   :target: https://github.com/SchmollerLab/Cell_ACDC/actions/workflows/build-macos_pyqt6.yml
   :alt: Build Status (macOS PyQt6)

.. image:: https://img.shields.io/pypi/pyversions/cellacdc
   :target: https://www.python.org/downloads/
   :alt: Python Version

.. image:: https://img.shields.io/pypi/v/cellacdc?color=red
   :target: https://pypi.org/project/cellacdc/
   :alt: PyPi Version

.. image:: https://static.pepy.tech/badge/cellacdc/month
   :target: https://pepy.tech/project/cellacdc
   :alt: Downloads per month

.. image:: https://img.shields.io/badge/license-BSD%203--Clause-brightgreen
   :target: https://github.com/SchmollerLab/Cell_ACDC/blob/main/LICENSE
   :alt: License

.. image:: https://img.shields.io/github/repo-size/SchmollerLab/Cell_ACDC
   :target: https://github.com/SchmollerLab/Cell_ACDC
   :alt: Repository Size

.. image:: https://img.shields.io/badge/DOI-10.1101%2F2021.09.28.462199-informational
   :target: https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-022-01372-6
   :alt: DOI

.. image:: https://readthedocs.org/projects/cell-acdc/badge/?version=latest
    :target: https://cell-acdc.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

|

.. image:: https://raw.githubusercontent.com/SchmollerLab/Cell_ACDC/main/cellacdc/resources/figures/Fig1.jpg
   :alt: Overview of pipeline and GUI
   :width: 600

Overview of pipeline and GUI

Overview
========
Let's face it, when dealing with segmentation of microscopy data we
often do not have time to check that **everything is correct**, because
it is a **tedious** and **very time consuming process**. Cell-ACDC comes
to the rescue! We combined the currently **best available neural network
models** (such as `Segment Anything Model
(SAM) <https://github.com/facebookresearch/segment-anything>`__,
`YeaZ <https://www.nature.com/articles/s41467-020-19557-4>`__,
`cellpose <https://www.nature.com/articles/s41592-020-01018-x>`__,
`StarDist <https://github.com/stardist/stardist>`__,
`YeastMate <https://github.com/hoerlteam/YeastMate>`__,
`omnipose <https://omnipose.readthedocs.io/>`__,
`delta <https://gitlab.com/dunloplab/delta>`__,
`DeepSea <https://doi.org/10.1016/j.crmeth.2023.100500>`__, etc.) and we
complemented them with a **fast and intuitive GUI**.

We developed and implemented several smart functionalities such as
**real-time continuous tracking**, **automatic propagation** of error
correction, and several tools to facilitate manual correction, from
simple yet useful **brush** and **eraser** to more complex flood fill
(magic wand) and Random Walker segmentation routines.

See below **how it compares** to other popular tools available (*Table 1
of
our* \ `publication <https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-022-01372-6>`__).

.. image:: https://raw.githubusercontent.com/SchmollerLab/Cell_ACDC/main/cellacdc/resources/figures/Table1.jpg
  :width: 700

Is it only about segmentation?
------------------------------
Of course not! Cell-ACDC automatically computes **several single-cell
numerical features** such as cell area and cell volume, plus the mean,
max, median, sum and quantiles of any additional fluorescent channel's
signal. It even performs background correction, to compute the **protein
amount and concentration**.

You can load and analyse single **2D images**, **3D data** (3D z-stacks
or 2D images over time) and even **4D data** (3D z-stacks over time).

Finally, we provide Jupyter notebooks to **visualize** and interactively
**explore** the data produced.

Bidirectional microscopy shift error correction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Is every second line in your files from your bidirectional microscopy
shifted? Look
`here <https://github.com/SchmollerLab/Cell_ACDC/blob/main/cellacdc/scripts/README.md>`__
for further information on how to correct your data.

Resources
=========
- Please find a complete user guide `here <https://cell-acdc.readthedocs.io/en/latest/>`__
- `Installation guide <https://cell-acdc.readthedocs.io/en/latest/installation.html#installation-using-anaconda-recommended>`__
- `User manual <https://github.com/SchmollerLab/Cell_ACDC/blob/main/UserManual/Cell-ACDC_User_Manual.pdf>`__
- `Publication <https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-022-01372-6>`__ of Cell-ACDC
- `Forum <https://github.com/SchmollerLab/Cell_ACDC/discussions>`__ for discussions (feel free to **ask any question**)
- **Report issues, request a feature or ask questions** by opening a new issue `here <https://github.com/SchmollerLab/Cell_ACDC/issues>`__
- X `thread <https://twitter.com/frank_pado/status/1443957038841794561?s=20>`__

Contact
=======
**Do not hesitate to contact me** here on GitHub (by opening an issue)
or directly at my email padovaf@tcd.ie for any problem and/or feedback
on how to improve the user experience!

Important links
===============

* `GitHub <https://github.com/SchmollerLab/Cell_ACDC>`__
* `Publication <https://bmcbiol.biomedcentral.com/articles/10.1186/s12915-022-01372-6>`__
* `Forum <https://forum.image.sc/tag/Cell-ACDC>`__
