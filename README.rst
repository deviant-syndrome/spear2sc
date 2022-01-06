spear2sc
========

This package provides utilities to read SPEAR_ particle files,
perform basic analysis on them and also convert them to a CSV file, that can be then directly read by SuperCollider_.
It reads the basic Spear format which is just a list of sinusoidal signals each classified with frequency, amplitude and temporal position.
When the Allows you to play particle-resynthezied samples in SuperCollider.
This package provides the above functionality in form of both a set of API methods, as well, a command line executable:

You can refer to this HTML-rendered Jupyter notebook to see the examples of API usage.

Installation
============
Requires Python 3. If this is not installed, download and install: https://www.python.org.

No official PIP package yet. You can easily install it from source::

    $ git clone hell
    $ cd there
    $ pip install -e ./

This will install a library and an executable. ``spear2sc`` command will be available from your terminal.
If you're are not interested in using imports, provided by this package, you can bypass installing and use it directly from the command line::

    $ git clone hell
    $ cd there
    $ python -m spear2sc choir1.txt -d=1.7 -a=0.001 --plot

Command Line Usage
==================

``spear2sc [-h] [--max-partials [MAX_PARTIALS]] [--part-dur-thresh [PART_DUR_THRESH]] [--part-lev-thresh [PART_LEV_THRESH]] [--plot] input
[output]``

positional arguments:
  ``input``:                Input file name in Spear format

  ``output``:                Output file, if not specified, only source file analysis will be performed

optional arguments:
  ``-h, --help``:           show this help message and exit

  ``--max-partials [MAX_PARTIALS], -m [MAX_PARTIALS]``: Maximum number of partials to write

  ``--part-dur-thresh [PART_DUR_THRESH], -d [PART_DUR_THRESH]``: Partial duration threshold, secs

  ``--part-lev-thresh [PART_LEV_THRESH], -a [PART_LEV_THRESH]``: Partial median level threshold, [0..1]

  ``--plot, -p``:            Plot partial level envelopes and duration distributions to console


Output CSV Format
=================
As SuperCollider supports with format natively, CSV file  format conventions:

- Lines are read by three for each partial
- First line is the time offsets
- Second line is the frequency points
- Third line is the amp level points

Example SuperCollider code to read and play this file would be the following::

    (
        var data = CSVFileReader.readInterpret("choir1.csv");
        var count = Array.fill(data.size.div(3), { arg i; [i * 3, i * 3 + 1, i * 3 + 2] });

        var pbinds = Array.newClear(data.size.div(3));

        count.do({ arg accessor, partNum;
	        var particleBind;
	        var partialTimePoints = data[accessor[0]];
	        var partialFreqPoints = data[accessor[1]];
	        var partialAmpPoints = data[accessor[2]];

	        var timeSize = partialTimePoints.size;
	        var valSize = partialFreqPoints.size;

	        var synthName = \partial_ ++ partNum;

	        SynthDef(synthName, { | gate = 1 |
		        var masterEnv = EnvGen.ar(Env.adsr(0.2, 4, 0.4, 0.5, 0.5), gate, doneAction: 2);

		        var ampEnvArray = Env(partialAmpPoints, partialTimePoints);
		        var freqEnvArray = Env(partialFreqPoints, partialTimePoints);


		        var ampEnvSig = EnvGen.ar(ampEnvArray, timeScale: 10);
		        var freqEnvSig = EnvGen.ar(freqEnvArray, timeScale: 10);
		        Out.ar(0, SinOsc.ar(freqEnvSig * 0.5, 0, ampEnvSig * masterEnv) ! 2)
	        }).add;

	        particleBind = Pbind(
	        	\instrument, synthName,
	        	\dur, Pn(5, 1)
	        );

	        pbinds[partNum] = particleBind;

        });

        Pspawner({|sp|
	        sp.seq(
	        	Ppar(pbinds, 1)
	        )
        }).play();
    )

.. _SPEAR: https://www.klingbeil.com/spear/
.. _SuperCollider: https://supercollider.github.io/

Future Improvements
===================
* Particle time offsets support in format
* Loop points detection
* Loop points support in format

python-cmdline-bootstrap
========================

This package was based on a structure template for Python command line applications, ready to be
released and distributed via setuptools/PyPI/pip for Python 2 and 3.

Please have a look at the corresponding article:
http://gehrcke.de/2014/02/distributing-a-python-command-line-application/

Acknowledgements
================
Code was reading a SPEAR file was based on the work of Stephen Bradshaw, which could be found in this repository:
https://github.com/stephenjbradshaw