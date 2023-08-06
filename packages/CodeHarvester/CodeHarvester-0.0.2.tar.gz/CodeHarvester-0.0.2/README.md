CodeHarvester
=============

CodeHarvester is a lightweight tool for merging different files respecting the requirements which are stated
in those files. It would be useful in Web development for concatenating multiple files together. Currently it
supports only JS like requirement definitions, but it is easily extensible.

Installation
------------

To install CodeHarvester simply do:

    pip install codeharvester
    
This will install CodeHarvester package and the runner script (`harvester.py`) into `/bin` directory.

Usage
-----

CodeHarvester can concatenate any type of files but currently understands only JS like notating.
To specify a requirement just write in the file:

    //= require anoter_file.js
    
`another_file.js` will be included in the same place it was defined. If the same requirement will appear anywhere else
it will be skipped because it is already included.

For command line options run:

    harvester.py --help

Example
-------

fileA.js:
  
    //= require fileB.js
    
    // this will be skipped because fileC.js will be already loaded as a requirement of fileB.js 
    //= require fileC.js
    
    ... fileA.js stuff ...
    
fileB.js
    
    //= require fileC.js
    
    ... fileB.js stuff ...
    
fileC.js
    
    ... fileC.js stuff ...
     
output_file.js
    
    ... fileC.js stuff ...
    ... fileB.js stuff ...
    ... fileA.js stuff ...
    