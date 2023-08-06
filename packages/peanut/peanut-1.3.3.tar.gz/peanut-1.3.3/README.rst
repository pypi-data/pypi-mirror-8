=======================================
PEANUT - The ParallEl AligNment UTility
=======================================

PEANUT is a read mapper for DNA or RNA sequence reads. Read mapping is the
process of aligning biological DNA or RNA sequencing reads to a known
reference genome.

By exploiting the massive parallelism of modern graphics processors and a novel
index datastructure (the q-group index), PEANUT achieves supreme speed compared
to current state of the art read mappers like BWA MEM, Bowtie2 and RazerS3
while maintaining their accuracy. PEANUT thereby allows to report both only the
best hit or all hits of a read.

When using PEANUT, please cite our article:

    Köster J, Rahmann S (2014).
    Massively parallel read mapping on GPUs with the q-group index and PEANUT.
    PeerJ 2:e606 http://dx.doi.org/10.7717/peerj.606


Requirements
------------

* A POSIX compatible OS (e.g. Linux, MacOS X, FreeBSD)
* an NVIDIA GPU with up-to-date proprietary drivers
  (this may change in the future as the AMD drivers become more mature)
* Python >= 3.2
* Numpy >= 1.7
* Cython >= 0.19
* Pyopencl >= 2013.1


Installation
------------

Using easy_install, all dependencies will be installed automatically if missing::

   $ easy_install3 peanut

When installing manually from setup.py, just execute::

   $ python3 setup.py install


Usage
-----

PEANUT will be available as a command line tool.
To index a reference genome `genome.fasta`, issue the following::

   $ peanut index genome.fasta genome.index.hdf5

To map paired end reads `reads.1.fastq` and `reads.2.fastq` onto the indexed
reference, use the following invocation::

   $ peanut map --threads 8 --insert-size 200 --insert-size-error 50 genome.index.hdf5 reads.1.fastq reads.2.fastq | samtools view -Sb - > mapped.bam

Here, an insert size or 200 with a tolerance of 50 is expected. Defining the
expected insert size is required for PEANUT to be able to detect properly
paired reads. Setting the wrong insert size here can lead to reduced
performance since PEANUT will try to rescue reads not properly paired by
performing additional alignments. As can be seen, PEANUT outputs hits in the
SAM format. Hence, output has to be piped into samtools to obtain a BAM file.
PEANUT buffers reads and hits in GPU and CPU memory. The default buffer
settings of PEANUT are optimized for a GPU with at least 2.5 GB memory and a
CPU with 16 GB memory (but 8 GB should do, too). You can lower both buffer
sizes to adapt for weaker systems, e.g.::

   $ peanut map --read-buffer 100000 --hits-buffer 500000 ...

This, however, can reduce performance since the amount of possible parallelism
on the GPU is affected. For further help, invoke::

   $ peanut --help

or visit http://peanut.readthedocs.org.


News
----

=========== ===================================================================
5 Sep 2014  Release 1.3.2 of PEANUT. Fixed a bug causing an invalid OpenCL work
            group size with uneven number of reads (special thanks to Sean Li
            for reporting this).
----------- -------------------------------------------------------------------
18 Aug 2014 Release 1.3 of PEANUT. Added rescue mode for paired-end sequencing.
----------- -------------------------------------------------------------------
7 Jul 2014  Release 1.2 of PEANUT. Improved mapping quality estimate that
            reflects the original posterior probability like defined in the MAQ
            paper of Heng Li.
----------- -------------------------------------------------------------------
26 May 2014 Release 1.1 of PEANUT. Reduced memory usage (at most 1/2 if you are
            lucky).
----------- -------------------------------------------------------------------
16 May 2014 Release 1.0.3 of PEANUT. Changed the argument order for the map
            subcommand to agree with other mappers.
----------- -------------------------------------------------------------------
7 May 2014  Release 1.0.2 of PEANUT. More fixes for alignment selection in case
            of paired end reads. Fixed missing import and --query-buffer not
            being considered.
----------- -------------------------------------------------------------------
30 Apr 2014 Release 1.0.1 of PEANUT. Improved flag usage in SAM output.
            Rescaled mapping quality in accordance with the paper. Fixed rare
            cases of where the wrong mate alignment was chosen as the best
            alignment.
=========== ===================================================================
