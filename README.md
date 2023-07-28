# Neighborhood Correlation

This program implements Dannie Durand's Neighborhood Correlation, as described in 
Song, Joseph, et al., 2008 (see below). It is designed to take BLAST bit-scores as input.

For details, see the [Neighborhood Correlation website](http://www.neighborhoodcorrelation.org). 

The code you find here at Github is an adaption to Python 3.x done by Jesper Holm as part of an
update of [GenFamClust](https://github.com/arvestad/GenFamClust). Lars Arvestad have helped with some restructuring
and Github adaption. 

## Cite!

If you use this software, please cite:

* Song N, Joseph JM, Davis GB, Durand D; _Sequence Similarity Network Reveals Common Ancestry of Multidomain
Proteins_; PLoS Computational Biology 4(5): e1000063; [doi:10.1371/journal.pcbi.1000063](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000063)

For details of Neighborhood Correlation please refer to
http://www.neighborhoodcorrelation.org/ or the paper above. 



# Licensing

(C) 2011 Jacob Joseph (<jmjoseph@andrew.cmu.edu>), and Carnegie Mellon University. 
    
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or (at
your option) any later version, see `LICENCE`.


## Prerequisites

This program requires `numpy`.

Additionally, a C compiler is required during installation to compile
the inner loop of the algorithm.  Such a compiler will be available on
nearly all UNIX-based systems.


## Installation

This program may be installed to your system (Mac and Linux at least, please report successful builds on other systems!) as follows.
Other platforms may require slight variations.

```
git clone git@github.com:arvestad/neighborhood_correlation.git
cd neighborhood_correlation
python -m build
python install .
```

Note that this package is using the "next generation" of Python package build tools, so leaving old-style setup.py behind.

# Running Neighborhood Correlation


The executable NC_standalone should now be installed to your system.
An explanation of program parameters is as follows:

Usage:

```
NC_standalone -f <flatfile> [options]
```

Output of Neighborhood Correlation scores will be printed to
stdout in the same three-column format as used for input.

**Options:**

```
     -f, --flatfile <filename>   (required)
          A white-space delimited file of BIT-scores from BLAST.  Three
          columns are expected, of the format:

          --------------------------------------
          seq_id_0   seq_id_1   bit_score
          seq_id_2   seq_id_3   bit_score
          ....
          --------------------------------------

          No column heading should be provided.  Please refer to
          http://www.ncbi.nlm.nih.gov/books/bv.fcgi?rid=handbook.section.614
          for an explanation of BIT-score.

     -o, --output <filename>
          Write score output to a file.  If omitted, the score list is
          printed to stdout.

     -h, --help
          Print this help message.

     --num_residues <integer>
          Number of residues in the sequence database.  Used to
          calculate SMIN, the lowest expected bit_score.  If
          unspecified, an estimate of 537 residues per sequence will
          be used, which is an average of mouse and human SwissProt
          sequences.

     --nc_thresh <0.05>
          NC reporting threshold.  Calculated values below this
          threshold will not be reported.  Conservatively defaults to
          0.05.

     --smin_factor <0.95>
          SMIN factor.  Calculate SMIN from the expected random
          BIT-score scaled by this factor. Defaults to 0.95.
```


## Input and Output

This program accepts as input a list of pairwise sequence
similarities, as BLAST BIT-scores.  Please refer to
http://www.ncbi.nlm.nih.gov/books/bv.fcgi?rid=handbook.section.614 for
discussion of the BIT-score.

Specifically, this program will read a white-space delimited file, in
a three-column format:

```
    --------------------------------------
    seq_id_0   seq_id_1   bit_score
    seq_id_2   seq_id_3   bit_score
    ....
    --------------------------------------
```          
No column heading should be provided.

Output is provided in the same three-column format:

```
    --------------------------------------
    seq_id_0   seq_id_1   nc_score
    seq_id_2   seq_id_3   nc_score
    ....
    --------------------------------------
```

Note that the output score file will not have the same pairs of
sequences.  BLAST will only output scores for pairs which are
significant.  Because Neighborhood Correlation considers the entire
set of BLAST scores related to a particular pair of sequences, 
a sequence pair that does not have a significant
BLAST score may still have a reasonably high Neighborhood Correlation
score.  Conversely, a pair of sequences with a high BIT-score may not
yield a high Neighborhood Correlation score.

The '--nc_thresh' parameter can be used to report only scores above a
given threshold (default=0.05).  Lower thresholds may be used for
greater completeness, producing an output file of more pairs.  If
'--nc_thresh' is set to zero, all pairs with a bit-score or at least
one common neighbor will be printed.  (The Neighborhood Correlation
between nodes that share no neighbors is necessarily zero, and such
pairs are not computed.)  This threshold affects only the printed
output and will not greatly affect runtime.


# Running BLAST

## Lars' note, 2023

_This section needs an update. There are better tools than
BLAST. Consider using DIAMOND, MMSEQ, or similar, to obtain scores instead._

## Old recommendations

Though comprehensive BLAST usage is beyond the scope of this document,
a few aspects of BLAST execution are critical.  In particular,

 - Expectation value ( blastall -e) should be set to the number 10*N,
   where N is the number of sequences in your dataset.  This ensures
   that BLAST returns similarity scores for all alignments.

 - Effective search space length (blastall -Y) should be set to R^2,
   where R is the number of residues in your dataset.

Standalone blast executables are available from NCBI at
http://www.ncbi.nlm.nih.gov/BLAST/download.shtml.

NCBI BLAST is able to output much more information in addition to the
scores required for input to Neighborhood Correlation.  If you are in
need of robust BLAST parsing, we recommend you consider that provided
by the BioPython project (http://biopython.org).


## Example Dataset


The file 'human_mouse_bit_scores.dat' contains all-against-all BLAST
results for all Human and Mouse sequences in SwissProt, version
50.9. Fragments have been excluded.

This is the dataset used for the Song et al. PLoS Computational
Biology paper.

Execution may be accomplished with:

```
   NC_standalone -f human_mouse_bit_scores.dat
```



#  ChangeLog

## Version 2.2

The code was updated by Jesper Holm in 2022, to ensure that it could run on Python 3.x, and specifically 3.7. 

## Version 2.1

Version 2.1 further improves the performance of Neighborhood
Correlation, in two ways:

1. To produce Neighborhood Correlation scores for all pairs of
   sequences, previous versions iterated over all N^2 pairs, for N
   input sequences.  This version progressively iterates through the
   neighborhood of each query sequence, resulting in N * M pairwise
   calculations, where M is the number of sequences in the
   neighborhood of each query sequence, plus the number of sequences
   in the neighborhoods of those sequences.  For large datasets, this
   optimization is extremely beneficial.

2. Neighborhood Correlation first makes the input BLAST scores
   symmetric: BIT-score(x,y) = max( BIT-score(x,y), BIT-score(y,x)).
   This version improves the efficiency of this calculation through
   use of a compiled C function.


BUG FIX: Version 2.0 was released with LOG_10 transformation of the
input inadvertently disabled.  Version 2.1 restores the correct
functionality, by using the LOG_10( BIT-score) for all internal
calculations.


## Version 2.0

Version 2.0 is a complete rewrite of the Neighborhood Correlation
implementation.  It is meant to replace Version 1.0 (previously
referred to as the "reference implementation").  Version 2.0 been
optimized to accommodate large datasets through fast computation and
greatly reduced memory usage.

This implementation has added a dependency upon the Numpy numerical
package.  It also requires a C compiler be available on the system.
See "Prerequisites", below.

Performance is greatly improved over Version 1.0.  As a rough guide,
the set of Mouse and Human sequences used in our analysis included
26,197 sequences.  From this, all-against-all BLAST yielded
approximately 4.8 million pairwise relations.  For this dataset,
Neighborhood Correlation, Version 2.0 can be expected to consume
approximately 125MB of memory.  Running time for this dataset is
approximately 45 minutes on an Intel Pentium D, at 3.2GHz.  Greater
than 1GB of memory, and 16 hours of running time were required by
Version 1.0.

The input and output of both versions should be equivalent, save the
following modification: Version 1.0 reported NC scores for pairs that
satisfied the condition (NC(x,y) >= nc_thresh || BLAST score (x,y)
exists).  Now, this has been simplified to only (NC(x,y) >=
nc_thresh).

Old versions remain available at
http://www.neighborhoodcorrelation.org.


## Version 1.0

Initial release.  This code was written for the original PLoS paper
describing Neighborhood Correlation.
