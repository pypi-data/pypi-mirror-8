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
