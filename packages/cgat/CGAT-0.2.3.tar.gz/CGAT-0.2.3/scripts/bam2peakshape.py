'''bam2peakshape.py - compute peak shape features from a bam-file
==============================================================

:Author: Andreas Heger
:Release: $Id$
:Date: |today|
:Tags: Genomics NGS Intervals BAM BED Summary

Purpose
-------

This script takes a :term:`bed` formatted file with regions of
interest, for example binding intervals from a ChIP-Seq
experiment. Using a collection of aligned reads is a :term:`bam`
formatted file or :term:`bigwig` formatted file, the script outputs a
collection of features describing the peak shape.

This script is designed with a slight emphasis on ChIP-Seq datasets.
The main reason that this script is better suited for ChIP-Seq is
that(1) it is able to center the counting window at the summit of
every individual peak; (2) it is also able to use the control ChIP-Seq
library to enable side-by-side comparison of treatment vs control;(3)
it can randomly shift the set of input regions to generate a
artificial set of regions, in the absence of real ChIP-Seq control
library, the random regions can provide a peaks profile that can be
used as the control.

For example, given the peaks regions defined by analyzing some
ChIP-Seq dataset (e.g. by using MACS), and without the need to use any
additional genomic annotations (e.g. ENSEMBL, refseq), we can
visualise the binding profiles of transcriptionfactors ChIP-Seq data
relative to the center of each peak regions.

The script outputs a tab-separated table on stdout containing features
for each interval. A peak is defined as the location of the highest
density in an interval. The width of the peak (peak_width) is defined
as the region around the peak in which the density does not drop below
a threshold of peak_heigt * 90%.

Usage
-----

Detailed usage example
++++++++++++++++++++++

The following command will generate the peak shape plot for the peak
regions defined in :file:`onepeak.bed`, using the reads stored in
:file:`small.bam`.  The command will also create a profile for the
control library.  The control library in this example is re-using the
same reads file :file:`small.bam`, however, in your actual experiment,
it should be a different library (the input library for this ChIP-Seq
experiment).::

    python ./scripts/bam2peakshape.py \
        ./tests/bam2peakshape.py/small.bam \
        ./tests/bam2peakshape.py/onepeak.bed \
        --control-bam-file=./tests/bam2peakshape.py/small.bam \
        --use-interval \
        --normalize-transcript


Output files
++++++++++++

Among the features output are:

+-------------------+---------------------------------------------------------+
|*Column*           |*Content*                                                |
+-------------------+---------------------------------------------------------+
|peak_height        |number of reads at peak                                  |
+-------------------+---------------------------------------------------------+
|peak_median        |median coverage compared to peak height                  |
+-------------------+---------------------------------------------------------+
|interval_width     |width of interval                                        |
+-------------------+---------------------------------------------------------+
|peak_width         |width of peak                                            |
+-------------------+---------------------------------------------------------+
|bins               |bins for a histogram of densities within the interval.   |
+-------------------+---------------------------------------------------------+
|npeaks             |number of density peaks in interval.                     |
+-------------------+---------------------------------------------------------+
|peak_center        |point of highest density in interval                     |
+-------------------+---------------------------------------------------------+
|peak_relative_pos  |point of highest density in interval coordinates         |
+-------------------+---------------------------------------------------------+
|counts             |counts for a histogram of densities within the interval  |
+-------------------+---------------------------------------------------------+
|furthest_half_heigh|Distance of peak center to furthest half-height position |
+-------------------+---------------------------------------------------------+
|closest_half_height|Distance of peak center to closest half-height position  |
+-------------------+---------------------------------------------------------+


Additionally, the script outputs a set of matrixes with densities over
intervals that can be used for plotting. The default filenames are
``(matrix|control)_<sortorder>.tsv.gz``, The names can be controlled
with the ``--output-filename-pattern`` option.


Type::

   python bam2peakshape.py --help

for command line help.


Options
-------

Option: Shift
+++++++++++++

shift the each read by a certain distance, because in a ChIP-Seq
experment, the read is always at the edge of an sonicated fragment,
the actual binding site is usually L/2 distance away from the read,
where L is the length of sonicated fragment (determined either
experimentally or computationally).

This option is used only if the input reads are in :term:`bam` formatted file.
If input reads are :term:`bigwig` formatted file, this option is ignored.

Option: Random shift
++++++++++++++++++++

randomly shift the set of input regions to generate a artificial set
of regions. In the absence of real ChIP-Seq control library, the
random regions can provide a peaks profile that can be used as the
control.

Option: Centring method
+++++++++++++++++++++++

"reads" will output in the way that the summit of the peaks are
aligned. "middle" will output in the way that the middle of the input
bed intervals are aligned.

Option: Only interval
+++++++++++++++++++++

Only count reads that are in the interval as defined by the input bed file.

Option: normalization=sum
+++++++++++++++++++++++++

normalize counts such that the sum of all counts in all features are
exactly 1000000.

The detail normalization algorithm as follows: norm = sum(all counts
in all features)/1000000.0 normalized count = normalized count / norm

.. todo::

   paired-endedness is not fully implemented.

Command line options
--------------------

'''

import sys
import re
import CGAT.Experiment as E
import CGAT.IOTools as IOTools
import pysam
import CGAT.Bed as Bed
import numpy
import bx.bbi.bigwig_file

try:
    import pyximport
    pyximport.install(build_in_temp=False)
    import _bam2peakshape
except ImportError:
    import CGAT._bam2peakshape as _bam2peakshape


def buildOptionParser(argv):

    if not argv:
        argv = sys.argv

    # setup command line parser
    parser = E.OptionParser(version="%prog version: $Id",
                            usage=globals()["__doc__"])

    parser.add_option("-f", "--format", dest="format", type="choice",
                      choices=("bam", "bigwig"),
                      help = "format of genomic input files for densities "
                      "[%default]")

    parser.add_option(
        "-o", "--use-interval", dest="use_interval", action="store_true",
        help="only count tags that are in interval given "
        "in bed file. Otherwise, use a fixed width window (see --window-size) "
        "around peak [%default]")

    parser.add_option(
        "-w", "--window-size", dest="window_size", type="int",
        help="window size around peak in interval to use"
        "[%default]")

    parser.add_option("-b", "--bin-size", dest="bin_size", type="int",
                      help="bin-size for histogram of read depth. "
                      "[%default]")

    parser.add_option("-s", "--sort-order", dest="sort_orders",
                      type="choice",
                      action="append",
                      choices=("peak-height", "peak-width", "unsorted",
                               "interval-width", "interval-score"),
                      help = "output sort order for matrices. "
                      "[%default]")

    parser.add_option(
        "-c", "--control-bam-file", dest="control_file", type="string",
        help="control file. If given, two peakshapes are computed, "
        "one for the primary data and one for the control data. "
        "The control file is centered around the same "
        "base as the primary file and output in the same "
        "sort order as the primary profile to all side-by-side. "
        "comparisons. "
        "[%default]")

    parser.add_option(
        "-r", "--random-shift", dest="random_shift", action="store_true",
        help="shift intervals in random direction up/downstream of interval "
        "[%default]")

    parser.add_option(
        "-e", "--centring-method", dest="centring_method", type="choice",
        choices=("reads", "middle"),
        help = "centring method. Available are: "
        "reads=use density to determine peak, "
        "middle=use middle of interval "
        "[%default]")

    parser.add_option(
        "-n", "--normalize-matrix", dest="normalization", type="choice",
        choices=("none", "sum"),
        help = "matrix normalisation to perform. "
        "[%default]")

    parser.add_option(
        "--use-strand", dest="strand_specific", action="store_true",
        help="use strand information in intervals. Intervals on the "
        "negative strand are flipped "
        "[%default]")

    parser.add_option(
        "-i", "--shift-size", dest="shift", type="int",
        help="shift for reads. When processing bam files, "
        "reads will be shifted upstream/downstream by this amount. "
        "[%default]")

    parser.set_defaults(
        bin_size=10,
        shift=0,
        window_size=1000,
        sort_orders=[],
        centring_method="reads",
        control_file=None,
        random_shift=False,
        strand_specific=False,
        format="bam",
        report_step=100,
    )

    return parser


def outputResults(result, bins, options):
    '''ouput results from density profiles.'''

    # center bins
    out_bins = bins[:-1] + options.bin_size

    def writeMatrix(result, sort):

        outfile_matrix = E.openOutputFile(
            "matrix_%s.gz" % re.sub("-", "_", sort))
        outfile_matrix.write("name\t%s\n" % "\t".join(map(str, out_bins)))

        if result[0][2] is not None:
            outfile_control = E.openOutputFile(
                "control_%s.gz" % re.sub("-", "_", sort))
            outfile_control.write("name\t%s\n" % "\t".join(map(str, out_bins)))

        if result[0][3] is not None:
            outfile_shift = E.openOutputFile(
                "shift_%s.gz" % re.sub("-", "_", sort))
            outfile_shift.write("name\t%s\n" % "\t".join(map(str, out_bins)))

        n = 0
        for features, bed, control, shifted in result:
            n += 1
            if "name" in bed:
                name = bed.name
            else:
                name = str(n)
            bins, counts = features[-2], features[-1]
            outfile_matrix.write(
                "%s\t%s\n" % (name, "\t".join(map(str, counts))))
            if control:
                outfile_control.write(
                    "%s\t%s\n" % (name, "\t".join(map(str, control.counts))))
            if shifted:
                outfile_shift.write(
                    "%s\t%s\n" % (name, "\t".join(map(str, shifted.counts))))

        outfile_matrix.close()

    n = 0
    for features, bed, control, shifted in result:
        n += 1
        if "name" in bed:
            name = bed.name
        else:
            name = str(n)
        options.stdout.write("%s\t%i\t%i\t%s\t" %
                             (bed.contig, bed.start, bed.end, name))

        options.stdout.write("\t".join(map(str, features[:-2])))
        bins, counts = features[-2], features[-1]
        options.stdout.write("\t%s" % ",".join(map(str, bins)))
        options.stdout.write("\t%s" % ",".join(map(str, counts)))
        options.stdout.write("\n")

    norm_result = []
    if options.normalization == "sum":
        E.info("Starting sum normalization")
        # get total counts across all intervals
        norm = 0.0
        for features, bed, control, shifted in result:
            counts = features[-1]
            norm += sum(counts)
        norm /= 1000000
        E.info("norm = %i" % norm)

        # normalise
        for features, bed, control, shifted in result:
            counts = features[-1]
            norm_counts = []
            for c in counts:
                norm_counts.append(c / (norm))
            new_features = features._replace(counts=norm_counts)
            norm_result.append((new_features, bed, control, shifted))
    else:
        E.info("No normalization performed")
        norm_result = result

    # output sorted matrices
    if not options.sort_orders:
        writeMatrix(norm_result, "unsorted")

    for sort in options.sort_orders:

        if sort == "peak-height":
            norm_result.sort(key=lambda x: x[0].peak_height)

        elif sort == "peak-width":
            norm_result.sort(key=lambda x: x[0].peak_width)

        elif sort == "interval-width":
            norm_result.sort(key=lambda x: x[1].end - x[1].start)

        elif sort == "interval-score":
            try:
                norm_result.sort(key=lambda x: float(x[1].score))
            except IndexError:
                E.warn("score field not present - no output")
                continue
            except TypeError:
                E.warn("score field not a valid number - no output")
                continue

        writeMatrix(norm_result, sort)


def buildResults(bedfile, fg_file, control_file, counter, options):
    '''compute densities and peakshape parameters.'''

    options.stdout.write("\t".join(("contig",
                                    "start",
                                    "end",
                                    "name",
                                    "\t".join(_bam2peakshape.PeakShapeResult._fields))) + "\n")

    if options.window_size:
        # bins are centered at peak-center and then stretching outwards.
        bins = numpy.arange(-options.window_size + options.bin_size // 2,
                            +options.window_size,
                            options.bin_size)

    #contigs = set(pysam_in.references)

    strand_specific = options.strand_specific

    result = []
    c = E.Counter()
    c.input = 0

    for bed in Bed.iterator(IOTools.openFile(bedfile)):
        c.input += 1

        # if bed.contig not in contigs:
        #    c.skipped += 1
        #    continue

        if c.input % options.report_step == 0:
            E.info("iteration: %i" % c.input)

        features = counter.countInInterval(
            fg_file,
            bed.contig, bed.start, bed.end,
            window_size=options.window_size,
            bins=bins,
            use_interval=options.use_interval,
            centring_method=options.centring_method)

        if features is None:
            c.skipped += 1
            continue

        if control_file:
            control = counter.countAroundPos(control_file,
                                             bed.contig,
                                             features.peak_center,
                                             bins=features.bins)

        else:
            control = None

        if options.random_shift:
            direction = numpy.random.randint(0, 2)
            if direction:
                pos = features.peak_center + 2 * bins[0]
            else:
                pos = features.peak_center + 2 * bins[-1]
            shifted = counter.countAroundPos(fg_file,
                                             bed.contig,
                                             pos,
                                             bins=features.bins)
        else:
            shifted = None

        if strand_specific and bed.strand == "-":
            features._replace(hist=hist[::-1])
            if control:
                control._replace(hist=hist[::-1])
            if shifted:
                shift._replace(hist=hist[::-1])

        result.append((features, bed, control, shifted))
        c.added += 1

    E.info("interval processing: %s" % c)

    return result, bins


def main(argv=None):
    """script main.

    parses command line options in sys.argv, unless *argv* is given.
    """

    parser = buildOptionParser(argv)

    # add common options (-h/--help, ...) and parse command line
    (options, args) = E.Start(parser, argv=argv, add_output_options=True)

    if len(args) != 2:
        raise ValueError("please specify a bam and bed file")

    infile, bedfile = args
    control_file = None
    if options.control_file:
        E.info("using control file %s" % options.control_file)

    if options.format == "bigwig":
        fg_file = bx.bbi.bigwig_file.BigWigFile(open(infile))
        if options.control_file:
            control_file = bx.bbi.bigwig_file.BigWigFile(
                open(options.control_file))
        counter = _bam2peakshape.CounterBigwig()

    elif options.format == "bam":
        fg_file = pysam.Samfile(infile, "rb")
        if options.control_file:
            control_file = pysam.Samfile(options.control_file, "rb")
        counter = _bam2peakshape.CounterBam(shift=options.shift)

    result, bins = buildResults(bedfile,
                                fg_file,
                                control_file,
                                counter,
                                options)

    if len(result) == 0:
        E.warn("no data - no output")
        E.Stop()
        return

    outputResults(result, bins, options)

    # write footer and output benchmark information.
    E.Stop()

if __name__ == "__main__":
    sys.exit(main(sys.argv))
