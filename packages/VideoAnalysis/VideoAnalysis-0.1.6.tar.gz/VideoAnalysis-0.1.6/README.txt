Widgets for analyzing videos of worms. 

To install, use:

    setup.py install

To see other install options:

    setup.py --help

In addition to the listed requirements, you will need to install
wormtracker, roitools, and OpenCV, which cannot be installed from
PyPI. 

To install OpenCV, see
http://docs.opencv.org/doc/tutorials/introduction/table_of_content_introduction/table_of_content_introduction.html. 

wormtracker and roitools are by Stephen Helms and can be obtained from
him (shelms@amolf.nl). wormtracker in turn requires scipy, h5py, and
scikit-image, which are available from PyPI. For convenience, these
are also listed as requirements of VideoAnalysis.

Other tricks to look out for: First, you will need an up-to-date
version of the ipython notebook, such as 2.4. Many ipython
installations have a very early version of the notebook, such as
0.x. This won't work. You can fix this with 

    pip install --upgrade --user ipython

You may find, though, when you actually run 'ipython notebook', that
it fails with the exception 'ImportError: IPython.html requires pyzmq
>= 2.1.11'. To fix this, use

    pip install pyzmq

(Why this is not listed in PyPI as a requirement for ipython[notebook]
I don't understand...)
