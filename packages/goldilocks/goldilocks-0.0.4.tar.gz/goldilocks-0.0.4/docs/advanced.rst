==============
Advanced Usage
==============

The following assumes basic Python programming experience (and
that you have installed Goldilocks and familiarised yourself
with the basics), skip to the end if you think you know what you're doing.


Filtering Regions
-----------------

By default when returning region data the "total" group is used, in our running
example of counting missing nucleotides, this would represent the total number
of 'N' bases seen in sequence data across each sample in the same genomic region
on the same chromosome. But if you are more interested in a particular sample: ::

    g._filter("max", group="my_sample")


When using tracks (for strategies that calculate multiple distinct values for
each genomic region - such as different nucleotide bases or k-mers), you may wish
to extract regions based on scores for a certain track: ::

    g._filter("max", track="AAA")


You may be interested in regions within some distance of the mean: ::

    g._filter("mean", acutal_distance=10)

Or perhaps the "top 10%", or the "middle 25%" around the mean: ::

    g._filter("max", percentile_distance=10)
    g._filter("mean", percentile_distance=25)

When not using `max` or `min`, by default both actual and percentile differences
calculate 'around' the `mean` or `median` value instead. If you'd like to control
this behaviour you can specify a direction: Let's fetch regions that have values
falling within 25% above or below the mean respectively: ::

    g._filter("mean", percentile_distance=25, direction=1)
    g._filter("mean", percentile_distance=25, direction=-1)


You can of course use these at the same time (though actual and percentile distances
are mutually exclusive), let's fetch the top 10% of regions that contain the most
"AAA" k-mers for all chromosomes in a hypothetical sample called "my_kmer_example": ::

    g._filter("max", group="my_kmer_example", track="AAA", percentile_distance=10)


Excluding Regions
-----------------

The filter function also allows users to specify a dictionary of exclusion criteria.

To filter regions based on the 1-indexed starting position greater than or equal to 3: ::

    g._filter("min", exclusions={
                                "start_gte": 3,
                                })

To filter regions based on the 1-indexed ending position less than or equal to 9: ::

    g._filter("min", exclusions={
                                "end_lte": 9,
                                })

You can filter regions that appear on particular chromosomes completely by providing a list: ::

    g._filter("min", exclusions={
                                "chr": ["X", 6],
                                })

You may want to use such exclusion criteria at the same time. Let's say we have
a bunch of sequence data from a species whose chromosomes all feature centromeres
between bases 500-1000. Let's ignore regions from that area. Let's also exclude
anything from chromosome 'G'. If a single one of these criteria are true, a region
will be excluded: ::

    g._filter("mean", exclusions={
                                 "start_gte": 500,
                                 "end_lte": 1000,
                                 "chr": ['G'],
                                 })

What if you want to exclude based on multiple criteria that should all be true?
Let's exclude regions that start before or on base 100 on chromosome X or Y [#]_.
Note the use of `use_and=True`! [#]_ ::

    g._filter("mean", exclusions={
                                 "start_lte": 100,
                                 "chr": ['X', 'Y'],
                                 }, use_and=True)


Finally applying exclusions across all chromosomes might seem quite naive, what
if we want to ignore centromeres on a real species? Introducing chromosome
dependent exclusions; the syntax is the same as previously, just the exclusions
dictionary is a dictionary of dictionaries with keys representing each chromosome.
Note the use of `use_chrom=True`: ::

    g._filter("median", exclusions={
                                    "one": {
                                        "start_lte": 3,
                                        "end_gte": 4
                                    },
                                    2: {
                                        "start_gte": 9
                                    },
                                    "X": {
                                        "chr": True
                                    }}, use_chrom=True)

It is important to note that currently Goldilocks does not sanity check the contents of
the exclusions dictionary including the spelling of exclusion names or whether you
have correctly set use_chrom if you are providing chromosome specific filtering.
However, on this latter point, if Goldilocks detects a key in the exclusions dictionary
matches the name of a chromosome, it will print a warning (but continue regardless).


.. [#] Support for chromosome matching is still 'or' based even when using use_and=True,
       a region can't appear on more than one chromosome and so this seemed a more
       natural and useful behaviour.
.. [#] Apart from the above caveat on chromosome matching always being or-based,
       currently there is no support for more complicated queries such as exclude
       if (statement1 and statement2) or statement3. It's or, or and on all criteria!

Limiting Regions
----------------

One may also limit the number of results returned by Goldilocks: ::

    g._filter("mean", limit=10)


Example
-------

Almost all of these options can be used together! Let's finish off our examples
by finding the top 5 regions that are within an absolute distance of 1.0 from
the maximum number of 'N' bases seen across all subsequences over the 'my_sample'
sample. We'll exclude any region that appears on chromosome "one" and any regions on
chromosome 2 that start on a base position greater than or equal to 5 *and* end on
a base position less than or equal to 10. Although when filtering the default
track is indeed 'default', we've explicity set that here too.::

    g._filter("max",
              group="my_sample",
              track="default",
              actual_distance=1,
              exclusions={
                    2: {
                        "start_gte": 5,
                        "end_lte": 10
                    },
                    "one": {
                        "chr":True
                    }
                },
                use_chrom=True,
                use_and=True,
                limit=5
    )

    [NOTE] Filtering values between 1.00 and 2.00 (inclusive)
    [NOTE] 28 processed, 12 match search criteria, 7 excluded, 5 limit

    ID      VAL     CHR     POSITIONS (INC.)
    0       {'default': 2}  2                1 -          3
    2       {'default': 2}  2                3 -          5
    1       {'default': 1}  2                2 -          4
    3       {'default': 1}  2                4 -          6
    20      {'default': 1}  X               13 -         15
