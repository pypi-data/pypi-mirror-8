#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013--, biocore development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------
"""
Unit tests for the SortMeRNA version 2.0 Application controller
===============================================================
"""


from unittest import TestCase, main
import re
from os import close
from os.path import abspath, exists, join, dirname
from tempfile import mkstemp, mkdtemp
from shutil import rmtree

from skbio.util import remove_files
from skbio.parse.sequences import parse_fasta

from bfillings.sortmerna_v2 import (build_database_sortmerna,
                                 sortmerna_ref_cluster,
                                 sortmerna_map)

# ----------------------------------------------------------------------------
# Copyright (c) 2014--, biocore development team
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------


# Test class and cases
class SortmernaV2Tests(TestCase):
    """ Tests for SortMeRNA version 2.0 functionality """

    def setUp(self):
        self.output_dir = mkdtemp()
        self.reference_seq_fp = reference_seqs_fp
        self.read_seqs_fp = read_seqs_fp

        # create temporary file with reference sequences defined
        # in reference_seqs_fp
        f, self.file_reference_seq_fp = mkstemp(prefix='temp_references_',
                                                suffix='.fasta')
        close(f)

        # write _reference_ sequences to tmp file
        with open(self.file_reference_seq_fp, 'w') as tmp:
            tmp.write(self.reference_seq_fp)
        tmp.close()

        # create temporary file with read sequences defined in read_seqs_fp
        f, self.file_read_seqs_fp = mkstemp(prefix='temp_reads_',
                                            suffix='.fasta')
        close(f)

        # write _read_ sequences to tmp file
        with open(self.file_read_seqs_fp, 'w') as tmp:
            tmp.write(self.read_seqs_fp)
        tmp.close()

        # list of files to remove
        self.files_to_remove = [self.file_reference_seq_fp,
                                self.file_read_seqs_fp]

    def tearDown(self):
        remove_files(self.files_to_remove)
        rmtree(self.output_dir)

    def test_indexdb_default_param(self):
    	""" Test indexing a database using SortMeRNA
        """
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        expected_db_files = set(sortmerna_db + ext
                                for ext in ['.bursttrie_0.dat', '.kmer_0.dat',
                                            '.pos_0.dat', '.stats'])

        # Make sure all db_files exist
        for fp in expected_db_files:
            self.assertTrue(exists(fp))

        # Add files to be remove
        self.files_to_remove.extend(db_files_to_remove)

    def test_empty_fasta_path(self):
        """ Indexdb should fail with an empty fasta path
        """
        self.assertRaises(ValueError,
                          build_database_sortmerna,
                          fasta_path=None,
                          max_pos=250,
                          output_dir=self.output_dir)

    def test_empty_inputs(self):
        """ (1) Indexdb should set output_dir to the same directory
                as where the input FASTA file is located;
            (2) SortMeRNA should fail if an empty result path is
                passed;
            (3) SortMeRNA should fail if an empty seq path is passed
        """
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=None)

        self.files_to_remove.extend(db_files_to_remove)

        fasta_dir = dirname(abspath(self.file_reference_seq_fp))
        out_dir = dirname(sortmerna_db)

        self.assertEqual(fasta_dir, out_dir)

        self.assertRaises(ValueError,
                          sortmerna_ref_cluster,
                          seq_path=self.file_read_seqs_fp,
                          sortmerna_db=sortmerna_db,
                          refseqs_fp=self.file_reference_seq_fp,
                          result_path=None)

        self.assertRaises(ValueError,
                          sortmerna_ref_cluster,
                          seq_path=None,
                          sortmerna_db=sortmerna_db,
                          refseqs_fp=self.file_reference_seq_fp,
                          result_path=join(self.output_dir,
                                           "sortmerna_otus.txt"))

    def test_tabular_output(self):
        """ SortMeRNA should output a BLAST tabular output
        """
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA
        clusters, failures, smr_files_to_remove = sortmerna_ref_cluster(
            seq_path=self.file_read_seqs_fp,
            sortmerna_db=sortmerna_db,
            refseqs_fp=self.file_reference_seq_fp,
            result_path=join(self.output_dir, "sortmerna_otus.txt"),
            tabular=True)

        self.assertTrue(exists(join(self.output_dir,
                                    "sortmerna_otus.blast")))

    def test_empty_result_path(self):
        """ SortMeRNA should fail with an empty indexed database
        """
        self.assertRaises(ValueError,
                          sortmerna_ref_cluster,
                          seq_path=self.file_read_seqs_fp,
                          sortmerna_db=None,
                          refseqs_fp=self.file_reference_seq_fp,
                          result_path=join(self.output_dir,
                                           "sortmerna_otus.txt")
                          )

    def test_sortmerna_default_param(self):
        """ SortMeRNA version 2.0 reference OTU picking works with default settings
        """
        # rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA
        cluster_map, failures, smr_files_to_remove = sortmerna_ref_cluster(
            seq_path=self.file_read_seqs_fp,
            sortmerna_db=sortmerna_db,
            refseqs_fp=self.file_reference_seq_fp,
            result_path=join(self.output_dir, "sortmerna_otus.txt"))

        # Check all sortmerna output files exist
        output_files = [join(self.output_dir, ext)
                        for ext in ['sortmerna_otus_otus.txt',
                                    'sortmerna_otus.log',
                                    'sortmerna_otus_denovo.fasta',
                                    'sortmerna_otus.fasta']]

        # Check output files exist
        for fp in output_files:
            self.assertTrue(exists(fp))

        # Files created sortmerna to be deleted (StdErr and StdOut were already
        # removed in sortmerna_ref_cluster)
        self.files_to_remove.extend(output_files)

        # Random reads that should not appear in any output file
        random_reads = ['simulated_random_reads.fa.000000000',
                        'simulated_random_reads.fa.000000001',
                        'simulated_random_reads.fa.000000002',
                        'simulated_random_reads.fa.000000003',
                        'simulated_random_reads.fa.000000004',
                        'simulated_random_reads.fa.000000005',
                        'simulated_random_reads.fa.000000006',
                        'simulated_random_reads.fa.000000007',
                        'simulated_random_reads.fa.000000008',
                        'simulated_random_reads.fa.000000009']

        # Reads passing E-value threshold and with similarity/coverage >=97%
        otu_reads = ['HMPMockV1.2.Staggered2.673827_47',
                     'HMPMockV1.2.Staggered2.673827_115',
                     'HMPMockV1.2.Staggered2.673827_122',
                     'HMPMockV1.2.Staggered2.673827_161',
                     'HMPMockV1.2.Staggered2.673827_180',
                     'HMPMockV1.2.Staggered2.673827_203',
                     'HMPMockV1.2.Staggered2.673827_207',
                     'HMPMockV1.2.Staggered2.673827_215',
                     'HMPMockV1.2.Staggered2.673827_218',
                     'HMPMockV1.2.Staggered2.673827_220']

        # Reads passing E-value threshold and with similarity/coverage <97%
        denovo_reads = ['HMPMockV1.2.Staggered2.673827_0',
                        'HMPMockV1.2.Staggered2.673827_1',
                        'HMPMockV1.2.Staggered2.673827_2',
                        'HMPMockV1.2.Staggered2.673827_3',
                        'HMPMockV1.2.Staggered2.673827_4',
                        'HMPMockV1.2.Staggered2.673827_5',
                        'HMPMockV1.2.Staggered2.673827_6',
                        'HMPMockV1.2.Staggered2.673827_7',
                        'HMPMockV1.2.Staggered2.673827_8',
                        'HMPMockV1.2.Staggered2.673827_9']

        # Check correct number of OTU clusters in file
        otu_clusters = ['295053']

        f_aligned = open(output_files[3], "U")
        f_otumap = open(output_files[0], "U")
        f_denovo = open(output_files[2], "U")

        # Verify the aligned FASTA file
        for label, seq in parse_fasta(f_aligned):
            id = label.split()[0]
            # Read is not random
            self.assertNotIn(id, random_reads)
            # Read is either in otu_reads or denovo_reads
            self.assertIn(id, otu_reads+denovo_reads)
        f_aligned.close()

        # Verify the de novo reads FASTA file
        for label, seq in parse_fasta(f_denovo):
            id = label.split()[0]
            # Read is not random
            self.assertNotIn(id, random_reads)
            # Read is not an OTU read
            self.assertNotIn(id, otu_reads)
            # Read is a de novo read
            self.assertIn(id, denovo_reads)
        f_denovo.close()

        # Check the OTU map
        for line in f_otumap:
            otu_entry = line.split()
            # Cluster ID is correct
            self.assertIn(otu_entry[0], otu_clusters)
            # Each read in the cluster must exclusively be an OTU read
            for read in otu_entry[1:]:
                self.assertNotIn(read, random_reads)
                self.assertNotIn(read, denovo_reads)
                self.assertIn(read, otu_reads)
        f_otumap.close()

        # Check returned list of lists of clusters
        expected_cluster = ['HMPMockV1.2.Staggered2.673827_47',
                            'HMPMockV1.2.Staggered2.673827_115',
                            'HMPMockV1.2.Staggered2.673827_122',
                            'HMPMockV1.2.Staggered2.673827_161',
                            'HMPMockV1.2.Staggered2.673827_180',
                            'HMPMockV1.2.Staggered2.673827_203',
                            'HMPMockV1.2.Staggered2.673827_207',
                            'HMPMockV1.2.Staggered2.673827_215',
                            'HMPMockV1.2.Staggered2.673827_218',
                            'HMPMockV1.2.Staggered2.673827_220']

        # Should only have 1 cluster
        self.assertEqual(1, len(cluster_map))
        for actual_cluster in cluster_map.itervalues():
            actual_cluster.sort()
            expected_cluster.sort()
            self.assertEqual(actual_cluster, expected_cluster)

        # Check log file number of clusters and failures corresponds to
        # the results in the output files
        f_log = open(output_files[1], "U")
        num_clusters = 0
        num_failures = 0
        for line in f_log:
            if line.startswith(" Total OTUs"):
                num_clusters = (re.split(' = ', line)[1]).strip()
            elif line.startswith("    Total reads for de novo clustering"):
                num_failures = (re.split(' = ', line)[1]).strip()
        f_log.close()

        self.assertEqual(int(num_clusters), len(otu_clusters))
        self.assertEqual(int(num_failures), len(denovo_reads))

    def test_sortmerna_map_default(self):
        """ SortMeRNA version 2.0 for mapping sequences onto a reference
            using default parameters
        """

        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA mapper
        app_result = sortmerna_map(seq_path=self.file_read_seqs_fp,
                                   output_dir=self.output_dir,
                                   refseqs_fp=self.file_reference_seq_fp,
                                   sortmerna_db=sortmerna_db)

        # Check all sortmerna output files exist
        output_files = [join(self.output_dir, ext)
                        for ext in ['sortmerna_map.blast',
                                    'sortmerna_map.log']]

        # Check output files exist
        for fp in output_files:
            self.assertTrue(exists(fp))

        blast_alignments_fp = app_result['BlastAlignments'].name

        # Check there are 30 alignments (1 per read)
        with open(blast_alignments_fp, 'U') as blast_actual:
            entries = (line.strip().split('\t') for line in blast_actual)
            actual_alignments = {r[0]: r[1:] for r in entries}

        self.assertEqual(30, len(actual_alignments))

        # Check this alignment exists
        self.assertTrue("HMPMockV1.2.Staggered2.673827_47"
                        in actual_alignments)
        self.assertEqual("97.3", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][1])
        self.assertEqual("100", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][12])

        # Check alignment for random read is NULL
        self.assertTrue("simulated_random_reads.fa.000000000"
                        in actual_alignments)
        self.assertEqual("*", actual_alignments[
            "simulated_random_reads.fa.000000000"][0])

    def test_sortmerna_map_sam_alignments(self):
        """ SortMeRNA version 2.0 for mapping sequences onto a reference
            outputting Blast and SAM alignments
        """

        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA mapper
        app_result = sortmerna_map(seq_path=self.file_read_seqs_fp,
                                   output_dir=self.output_dir,
                                   refseqs_fp=self.file_reference_seq_fp,
                                   sortmerna_db=sortmerna_db,
                                   output_sam=True)

        # Check all sortmerna output files exist
        output_files = [join(self.output_dir, ext)
                        for ext in ['sortmerna_map.blast',
                                    'sortmerna_map.sam',
                                    'sortmerna_map.log']]

        # Check output files exist
        for fp in output_files:
            self.assertTrue(exists(fp))

        sam_alignments_fp = app_result['SAMAlignments'].name

        # Check there are 30 alignments in the SAM output (1 per read)
        with open(sam_alignments_fp, 'U') as sam_actual:
            entries = (line.strip().split('\t') for line in sam_actual)
            actual_alignments = {r[0]: r[1:] for r in entries}

        # 30 alignments expected + 2 lines for @HD and @PG fields
        self.assertEqual(32, len(actual_alignments))

        # Check this alignment exists
        self.assertTrue("HMPMockV1.2.Staggered2.673827_47"
                        in actual_alignments)
        self.assertEqual("295053", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][1])
        self.assertEqual("AS:i:418", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][10])

        # Check alignment for random read is NULL
        self.assertTrue("simulated_random_reads.fa.000000000"
                        in actual_alignments)
        self.assertEqual("*", actual_alignments[
            "simulated_random_reads.fa.000000000"][1])

    def test_sortmerna_map_sam_alignments_with_tags(self):
        """ SortMeRNA version 2.0 for mapping sequences onto a reference
            outputting SAM alignments with @SQ tags
        """

        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA mapper
        app_result = sortmerna_map(seq_path=self.file_read_seqs_fp,
                                   output_dir=self.output_dir,
                                   refseqs_fp=self.file_reference_seq_fp,
                                   sortmerna_db=sortmerna_db,
                                   output_sam=True,
                                   sam_SQ_tags=True,
                                   blast_format=None)

        # Check all sortmerna output files exist
        output_files = [join(self.output_dir, ext)
                        for ext in ['sortmerna_map.sam',
                                    'sortmerna_map.log']]

        # Check output files exist
        for fp in output_files:
            self.assertTrue(exists(fp))

        sam_alignments_fp = app_result['SAMAlignments'].name

        # Check there are 30 alignments in the SAM output (1 per read)
        with open(sam_alignments_fp, 'U') as sam_actual:
            actual_entries = [line.strip().split('\t') for line in sam_actual]

        # 30 alignments expected + 2 lines for @HD and @PG fields + 5 lines
        # for the @SQ tags
        self.assertEqual(37, len(actual_entries))

        # Check all expected @SQ tags have been included
        SQ_array = [['@SQ', 'SN:42684', 'LN:1501'],
                    ['@SQ', 'SN:342684', 'LN:1486'],
                    ['@SQ', 'SN:426848', 'LN:1486'],
                    ['@SQ', 'SN:295053', 'LN:1389'],
                    ['@SQ', 'SN:879972', 'LN:1371']]
        for entry in SQ_array:
            self.assertTrue(entry in actual_entries)

    def test_sortmerna_map_blast_no_null_alignments(self):
        """ SortMeRNA version 2.0 for mapping sequences onto a reference
            using Blast with --print_all_reads option set to False
            (no NULL alignments output)
        """

        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA mapper
        app_result = sortmerna_map(seq_path=self.file_read_seqs_fp,
                                   output_dir=self.output_dir,
                                   refseqs_fp=self.file_reference_seq_fp,
                                   sortmerna_db=sortmerna_db,
                                   print_all_reads=False)

        # Check all sortmerna output files exist
        output_files = [join(self.output_dir, ext)
                        for ext in ['sortmerna_map.blast',
                                    'sortmerna_map.log']]

        # Check output files exist
        for fp in output_files:
            self.assertTrue(exists(fp))

        blast_alignments_fp = app_result['BlastAlignments'].name

        # Check there are 20 alignments (1 per read)
        with open(blast_alignments_fp, 'U') as blast_actual:
            entries = (line.strip().split('\t') for line in blast_actual)
            actual_alignments = {r[0]: r[1:] for r in entries}

        self.assertEqual(20, len(actual_alignments))

        # Check this alignment exists
        self.assertTrue("HMPMockV1.2.Staggered2.673827_47"
                        in actual_alignments)
        self.assertEqual("97.3", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][1])
        self.assertEqual("100", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][12])

        # Check alignment for random read does not exist
        self.assertFalse("simulated_random_reads.fa.000000000"
                         in actual_alignments)

    def test_sortmerna_map_num_alignments(self):
        """ SortMeRNA version 2.0 for mapping sequences onto a reference
            outputting first INT num_alignments passing the E-value threshold
            (rather than first INT best alignments)
        """

        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        # Run SortMeRNA mapper
        app_result = sortmerna_map(seq_path=self.file_read_seqs_fp,
                                   output_dir=self.output_dir,
                                   refseqs_fp=self.file_reference_seq_fp,
                                   sortmerna_db=sortmerna_db,
                                   num_alignments=1)

        # Check all sortmerna output files exist
        output_files = [join(self.output_dir, ext)
                        for ext in ['sortmerna_map.blast',
                                    'sortmerna_map.log']]

        # Check output files exist
        for fp in output_files:
            self.assertTrue(exists(fp))

        blast_alignments_fp = app_result['BlastAlignments'].name

        # Check there are 30 alignments (1 per read)
        with open(blast_alignments_fp, 'U') as blast_actual:
            entries = (line.strip().split('\t') for line in blast_actual)
            actual_alignments = {r[0]: r[1:] for r in entries}

        self.assertEqual(30, len(actual_alignments))

        # Check this alignment exists
        self.assertTrue("HMPMockV1.2.Staggered2.673827_47"
                        in actual_alignments)
        self.assertEqual("97.3", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][1])
        self.assertEqual("100", actual_alignments[
            "HMPMockV1.2.Staggered2.673827_47"][12])

        # Check alignment for random read is NULL
        self.assertTrue("simulated_random_reads.fa.000000000"
                        in actual_alignments)
        self.assertEqual("*", actual_alignments[
            "simulated_random_reads.fa.000000000"][0])

    def test_blast_or_sam(self):
        """ SortMeRNA should fail with output_sam and blast_format both
            set to False
        """
        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        self.assertRaises(ValueError,
                          sortmerna_map,
                          seq_path=self.file_read_seqs_fp,
                          output_dir=self.output_dir,
                          refseqs_fp=self.file_reference_seq_fp,
                          sortmerna_db=sortmerna_db,
                          output_sam=False,
                          blast_format=None)

    def test_best_or_num_alignments(self):
        """ SortMeRNA should fail with "best" and "num_alignments" both
            set to True
        """
        # Rebuild the index
        sortmerna_db, db_files_to_remove = build_database_sortmerna(
            abspath(self.file_reference_seq_fp),
            max_pos=250,
            output_dir=self.output_dir)

        # Files created by indexdb_rna to be deleted
        self.files_to_remove.extend(db_files_to_remove)

        self.assertRaises(ValueError,
                          sortmerna_map,
                          seq_path=self.file_read_seqs_fp,
                          output_dir=self.output_dir,
                          refseqs_fp=self.file_reference_seq_fp,
                          sortmerna_db=sortmerna_db,
                          best=1,
                          num_alignments=1)


# Reference sequence database
reference_seqs_fp = """>426848
AGAGTTTGATCCTGGCTCAGGATGAACGCTAGCGGCAGGCTTAATACATGCAAGTCGAGGGGCAGCACTGGTAGCAATAC
CTGGTGGCGACCGGCGGACGGGTGCGTAACACGTATGCAACCTACCCTGTACAGGGGGATAGCCCGAGGAAATTCGGATT
AATACCCCATACGATAAGAATCGGCATCGATTTTTATTGAAAGCTCCGGCGGTACAGGATGGGCATGCGCCCCATTAGCT
AGTTGGTGAGGTAACGGCTCACCAAGGCTACGATGGGTAGGGGGCCTGAGAGGGTGATCCCCCACACTGGAACTGAGACA
CGGTCCAGACTCCTACGGGAGGCAGCAGTAAGGAATATTGGTCAATGGGCGCAAGCCTGAACCAGCCATGCCGCGTGCAG
GAAGACTGCCATTATGGTTGTAAACTGCTTTTATATGGGAAGAAACCTCCGGACGTGTCCGGAGCTGACGGTACCATGTG
AATAAGGATCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGATCCAAGCGTTATCCGGATTTATTGGGTTTAAA
GGGTGCGTAGGCGGCGTGTTAAGTCAGAGGTGAAATTCGGCAGCTCAACTGTCAAATTGCCTTTGATACTGGCACACTTG
AATGCGATTGAGGTAGGCGGAATGTGACATGTAGCGGTGAAATGCTTAGACATGTGACAGAACACCGATTGCGAAGGCAG
CTTACCAAGTCGTTATTGACGCTGAGGCACGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCGTA
AACGATGATAACTCGACGTTAGCGATACACTGTTAGCGTCCAAGCGAAAGCGTTAAGTTATCCACCTGGGAAGTACGATC
GCAAGGTTGAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGATGATACGCGAGGA
ACCTTACCAGGGCTTAAATGGGGAACGACCTTCTGGGAAACCAGAATTTCTTTTAGACGGTCCTCAAGGTGCTGCATGGT
TGTCGTCAGCTCGTGCCGTGAGGTGTTGGGTTAAGTCCCGCAACGAGCGCAACCCCTACTGTTAGTTGCCAGCGGATAAT
GCCGGGGACTCTAGCGGAACTGCCTGTGCAAACAGAGAGGAAGGTGGGGATGACGTCAAATCATCACGGCCCTTACGTCC
TGGGCTACACACGTGCTACAATGGCCGGTACAGAGGGCAGCCACTTCGTGAGAAGGAGCGAATCCTTAAAGCCGGTCTCA
GTTCGGATTGTAGTCTGCAACTCGACTACATGAAGCTGGAATCGCTAGTAATCGCGTATCAGCCATGACGCGGTGAATAC
GTTCCCGGGCCTTGTACACACCGCCCGTCAAGCCATGGGAATTGGGAGTACCTAAAGTCGGTAACCGCAAGGAGCCGCCT
AAGGTAATACCAGTGACTGGGGCTAAGTCGTAACAAGGTAGCCGTA
>42684
AGAGTTTGATCCTGGCTCAGATTGAACGCTGGCGGCATGCTTTACACATGCAAGTCGGACGGCAGCACAGAGGAGCTTGC
TTCTTGGGTGGCGAGTGGCGAACGGGTGAGTGACGCATCGGAACGTACCGAGTAATGGGGGATAACTGTCCGAAAGGACA
GCTAATACCGCATACGCCCTGAGGGGGAAAGCGGGGGATCTTAGGACCTCGCGTTATTCGAGCGGCCGATGTCTGATTAG
CTGGTTGGCGGGGTAAAGGCCCACCAAGGCGACGATCAGTAGCGGGTCTGAGAGGATGATCCGCCACACTGGGACTGAGA
CACGGCCCAGACTCCTACGGGAGGCAGCAGTGGGGAATTTTGGACAATGGGCGCAAGCCTGATCCAGCCATGCCGCGTGT
CTGAAGAAGGCCTTCGGGTTGTAAAGGACTTTTGTCAGGGAAGAAAAGGAACGTGTTAATACCATGTTCTGATGACGGTA
CCTGAAGAATAAGCACCGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGGTGCGAGCGTTAATCGGAATTACTGG
GCGTAAAGCGGGCGCAGACGGTTACTTAAGCGGGATGTGAAATCCCCGGGCTCAACCCGGGAACTGCGTTCCGAACTGGG
TGGCTAGAGTGTGTCAGAGGGGGGTAGAATTCCACGTGTAGCAGTGAAATGCGTAGAGATGTGGAGGAATACCGATGGCG
AAGGCAGCCCCCTGGGATAACACTGACGTTCATGCCCGAAAGCGTGGGTAGCAAACAGGGTTAGATACCCTGGTAGTCCA
CGCCCTAAACGATGTCGATTAGCTGTTGGGGCACTTGATGCCTTAGTAGCGTAGCTAACGCGTGAAATCGACCGCCTGGG
GAGTACGGTCGCAAGATTAAAACTCAAAGGAATTGACGGGGACCCGCACAAGCGGTGGATGATGTGGATTAATTCGATGC
AACGCGAAGAACCTTACCTGGTCTTGACATGTACGGAATCTTCCAGAGACGGAAGGGTGCCTTCGGGAGCCGTAACACAG
GTGCTGCATGGCTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTTGTCATTAGTTG
CCATCACTTGGTTGGGCACTCTAATGAGACTGCCGGTGACAAACCGGAGGAAGGTGGGGATGACGTCAAGTCCTCATGGC
CCTTATGACCAGGGCTTCACACGTCATACAATGGTCGGTACAGAGGGTAGCCAAGCCGCGAGGCGGAGCCAATCCCAGAA
AACCGATCGTAGTCCGGATTGCACTCTGCAACTCGAGTGCATGAAGTCGGAATCGCTAGTAATCGCAGGTCAGCATACTG
CGGTGAATACGTTCCCGGGTCTTGTACACACCGCCCGTCACACCATGGGAGTGGGGGATACCAGAAGCAGGTAGGCTAAC
CGCAAGGAGGCCGCTTGCCACGGTATGCTTCATGACTGGGGTGAAGTCGTAACAAGGTAAC
>342684
AGAGTTTGATCCTGGCTCAGGATGAACGCTAGCGGCAGGCTTAACACATGCAAGTCGAGGGGCATCGCGGGTAGCAATAC
CTGGCGGCGACCGGCGGAAGGGTGCGTAACGCGTGAGCGACATACCCGTGACAGGGGGATAACAGATGGAAACGTCTCCT
AATACCCCATAAGATCATATATCGCATGGTATGTGATTGAAAGGTGAGAACCGGTCACGGATTGGCTCGCGTCCCATCAG
GTAGACGGCGGGGCAGCGGCCCGCCGTGCCGACGACGGGTAGGGGCTCTGAGAGGAGTGACCCCCACAATGGAACTGAGA
CACGGTCCATACTCCTACGGGAGGCAGCAGTGAGGAATATTGGTCAATGGGCGGAAGCCTGAACCAGCCATGCCGCGTGC
GGGAGGACGGCCCTATGGGTTGTAAACCGCTTTTGAGTGAGAGCAATAAGGTTCACGTGTGGACCGATGAGAGTATCATT
CGAATAAGCATCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGATGCGAGCGTTATCCGGATTCATTGGGTTTA
AAGGGTGCGTAGGCGGACATGTAAGTCCGAGGTGAAAGACCGGGGCCCAACCCCGGGGTTGCCTCGGATACTGTGTGTCT
GGAGTGGACGTGCCGCCGGGGGAATGAGTGGTGTAGCGGTGAAATGCATAGATGTCACTCAGAACACCGATTGCGAAGGC
ACCTGGCGAATGTCTTACTGACGCTGAGGCACGAAAGCGTGGGGATCGAACAGGATTAGATACCCTGGTAGTCCACGCAG
TAAACGATGATGGCTGTCCGTTCGCTCCGATAGGAGTGAGTAGACAAGCGAAAGCGCTAAGCCATCCACCTGGGGAGTAC
GGCCGCAAGGCTGAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGAGGAACATGTGGTTTAATTCGATGATACGCG
AGGAACCTTACCCGGGCTCGAACGGCAGGTGAACGATGCAGAGATGCAAAGGCCCTTCGGGGCGTCTGTCGAGGTGCTGC
ATGGTTGTCGTCAGCTCGTGCCGTGAGGTGTCGGCTCAAGTGCCATAACGAGCGCAACCCTTGCCTGCAGTTGCCATCGG
GTAAAGCCGGGGACTCTGCAGGGACTGCCACCGCAAGGTGAGAGGAGGGGGGGGATGACGTCAAATCAGCACGGCCCTTA
CGTCCGGGGCGACACACGTGTTACAATGGCGGCCACAGCGGGAAGCCACCCAGTGATGGGGCGCGGATCCCAAAAAAGCC
GCCTCAGTTCGGATCGGAGTCTGCAACCCGACTCCGTGAAGCTGGATTCGCTAGTAATCGCGCATCAGCCATGGCGCGGT
GAATACGTTCCCGGGCCTTGTACACACCGCCCGTCAAGCCATGGGAGTCGTGGGCGCCTGAAGGCCGTGACCGCGAGGAG
CGGCCTAGGGCGAACGCGGTGACTGGGGCTAAGTCGTAACAAGGTA
>295053
AGAGTTTGATCCTGGCTCAGGACGAACGCTGGCGGCGTGCCTAACACATGCAAGTCGAACGGAGATGCTCCTTCGGGAGT
ATCTTAGTGGCGAACGGGTGAGTAACGCGTGAGCAACCTGACCTTCACAGGGGGATAACCGCTGGAAACAGCAGCTAATA
CCGCATAACGTCGCAAGACCAAAGAGGGGGACCTTCGGGCCTCTTGCCATCGGATGTGCCCAGATGGGATTAGCTTGTTG
GTGGGGTAACGGCTCACCAAGGCGACGATCCCTAGCTGGTCTGAGAGGATGACCAGCCACACTGGAACTGAGACACGGTC
CAGACTCCTACGGGAGGCAGCAGTGGGGAATATTGCACAATGGGCGCAAGCCTGATGCAGCCATGCCGCGTGTATGAAGA
AGGCCTTCGGGTTGTAAAGTACTTTCAGCGGGGAGGAAGGGAGTAAAGTTAATACCTTTGCTCATTGACGTTACCCGCAG
AAGAAGCACCGGCTAACTCCGTGCCAGCAGCCGCGGTAATACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAA
GCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTG
AGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTGAAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGG
CCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCGTA
AACGATGTCGACTTGGAGGTTGTGCCCTTGAGGCGTGGCTTCCGGAGCTAACGCGTTAAGTCGACCGCCTGGGGAGTACG
GCCGCAAGGTTAAAACTCAAATGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGATGCAACGCGA
AGAACCTTACCTGGTCTTGACATCCACAGAACTTTCCAGAGATGGATTGGTGCCTTCGGGAACTGTGAGACAGGTGCTGC
ATGGCTGTCGTCAGCTCGTGTTGTGAAATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCTTGTCCTTTGTTGCCAGCGG
TCCGGCCGGGAACTCAAAGGAGACTGCCAGTGATAAACTGGAGGAAGGTGGGGATGACGTCAAGTCATCATGGCCCTTAC
GACCAGGGCTACACACGTGCTACAATGGCGCATACAAAGAGAAGCGACCTCGCGAGAGCAAGCGGACCTCATAAAGTGCG
TCGTAGTCCGGATTGGAGTCTGCAACTCGACTCCATGAAGTCGGAATCGCTAGTAATCGTGGATCAGAATGCCACGGTGA
ATACGTTCCCGGGCCTTGCACACACCGCC
>879972
GACGAACGCTGGCGGCGTGCCTAATACATGCAAGTCGAACGAGATTGACCGGTGCTTGCACTGGTCAATCTAGTGGCGAA
CGGGTGAGTAACACGTGGGTAACCTGCCCATCAGAGGGGGATAACATTCGGAAACGGATGCTAAAACCGCATAGGTCTTC
GAACCGCATGGTTTGAAGAGGAAAAGAGGCGCAAGCTTCTGCTGATGGATGGACCCGCGGTGTATTAGCTAGTTGGTGGG
GTAACGGCTCACCAAGGCGACGATACATAGCCGACCTGAGAGGGTGATCGGCCACACTGGGACTGAGACACGGCCCAGAC
TCCTACGGGAGGCAGCAGTAGGGAATCTTCGGCAATGGACGGAAGTCTGACCGAGCAACGCCGCGTGAGTGAAGAAGGTT
TTCGGATCGTAAAGCTCTGTTGTAAGAGAAGAACGAGTGTGAGAGTGGAAAGTTCACACTGTGACGGTATCTTACCAGAA
AGGGACGGCTAACTACGTGCCAGCAGCCGCGGTAATACGTAGGTCCCGAGCGTTGTCCGGATTTATTGGGCGTAAAGCGA
GCGCAGGCGGTTAGATAAGTCTGAAGTTAAAGGCTGTGGCTTAACCATAGTACGCTTTGGAAACTGTTTAACTTGAGTGC
AAGAGGGGAGAGTGGAATTCCATGTGTAGCGGTGAAATGCGTAGATATATGGAGGAACACCGGTGGCGAAAGCGGCTCTC
TGGCTTGTAACTGACGCTGAGGCTCGAAAGCGTGGGGAGCAAACAGGATTAGATACCCTGGTAGTCCACGCCGTAAACGA
TGAGTGCTAGGTGTTAGACCCTTTCCGGGGTTTAGTGCCGCAGCTAACGCATTAAGCACTCCGCCTGGGGAGTACGACCG
CAGGGTTGAAACTCAAAGGAATTGACGGGGGCCCGCACAAGCGGTGGAGCATGTGGTTTAATTCGAAGCAACGCGAAGAA
CCTTACCAGGTCTTGACATCCCTCTGACCGCTCTAGAGATAGAGCTTTCCTTCGGGACAGAGGTGACAGGTGGTGCATGG
TTGTCGTCAGCTCGTGTCGTGAGATGTTGGGTTAAGTCCCGCAACGAGCGCAACCCCTATTGTTAGTTGCCATCATTCAG
TTGGGCACTCTAGCGAGACTGCCGGTAATAAACCGGAGGAAGGTGGGGATGACGTCAAATCATCATGCCCCTTATGACCT
GGGCTACACACGTGCTACAATGGCTGGTACAACGAGTCGCAAGCCGGTGACGGCAAGCTAATCTCTTAAAGCCAGTCTCA
GTTCGGATTGTAGGCTGCAACTCGCCTACATGAAGTCGGAATCGCTAGTAATCGCGGATCAGCACGCCGCGGTGAATACG
TTCCCGGGCCT
"""

# Reads to search against the database
# - 10 rRNA reads:   amplicon reads were taken from Qiime study 1685
# - 10 random reads: simulated using mason with the following command:
#     mason illumina -N 10 -snN -o simulated_random_reads.fa -n
#     150 random.fasta
# - 10 rRNA reads with id < 97: amplicon reads were taken from
#   Qiime study 1685
read_seqs_fp = """>HMPMockV1.2.Staggered2.673827_47 M141:79:749142:1:1101:16169:1589
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCAAGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATTTGATACTGGCAAGCTTGAGTCTCGTAGAGGAGGGTAGAATTCCAGGTGTAGCGGGG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCTCCATGGACGAAGACTGACGCT
>HMPMockV1.2.Staggered2.673827_115 M141:79:749142:1:1101:14141:1729
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CCGGCTCAACCTTGGAACTGCATCTGATACGGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCTCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
GGGAGCAAACA
>HMPMockV1.2.Staggered2.673827_122 M141:79:749142:1:1101:16032:1739
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
GTGATCAAACA
>HMPMockV1.2.Staggered2.673827_161 M141:79:749142:1:1101:17917:1787
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCTCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
GGGAGCAAACA
>HMPMockV1.2.Staggered2.673827_180 M141:79:749142:1:1101:16014:1819
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGTGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
>HMPMockV1.2.Staggered2.673827_203 M141:79:749142:1:1101:17274:1859
TACGGAGGTTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CCGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCTCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
GGGATCAAACA
>HMPMockV1.2.Staggered2.673827_207 M141:79:749142:1:1101:17460:1866
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
GGGAGCAAACA
>HMPMockV1.2.Staggered2.673827_215 M141:79:749142:1:1101:18390:1876
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACG
>HMPMockV1.2.Staggered2.673827_218 M141:79:749142:1:1101:18249:1879
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTTCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCCCCTGGACGAAGACTGACGCTCAGGTGCGAAAGCGTG
GGGAGCACACA
>HMPMockV1.2.Staggered2.673827_220 M141:79:749142:1:1101:15057:1880
TACGGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCACGCAGGCGGTTTGTTAAGTCAGATGTGAAATCCC
CGGGCTCAACCTGGGAACTGCATCTGATACTGGCAAGCTTGAGTCTCGTAGAGGGGGGTAGAATTCCAGGTGTAGCGGTG
AAATGCGTAGAGATCTGGAGGAATACCGGTGGCGAAGGCGGCCTCCTGGACGAAGACTGACGCTC
>simulated_random_reads.fa.000000000
AGCCGGGTGTCTACGGTCAGGTGTGTTCTGACTACGTAGTTTGACAGCACGTGTCCTTTCCCCTTCCCAAGGTAACGAAT
TGTCGTTATCAACGTTTCGATCCGTAATTTCACGGAACGACATAAAGGCATCAATACTATCGCCAACAGA
>simulated_random_reads.fa.000000001
GTGGACGTCGTGGCGGCGTACTAACTTCCTACAGGCATATCCGGAATAACATTCTGCCGCTTGTCGACATAAGCTGTTCC
CTACATAGACGACGACGGTTGAAGGGTGTATGTATTCTTTGGGTACGGCTCCTCTGGGCGCATGGTAGCA
>simulated_random_reads.fa.000000002
CATTCTTTATAGGCCTACAACACTAATCATCGTTAAGCATAAGGGGAGGAGTGTGCGTGGCATCAAGTCCTGGTTCTTCG
CCTAGTACCACACCGTCTCACACGCAGCCGCCGACGACCAGTGAGGGCGCGTGGGACACCCATTCGGTCC
>simulated_random_reads.fa.000000003
TCGCCTTGGTACAAACAGTCGCGGCACGCTGTATGGAGGACCATAGAGGCACAGGCTGAGGACAGGGGCATGGAAGGTTC
AATCGCCCCCCACAGCTTTAGGTAGGAAGTACTGTTCTAGTGCCAATTTGATTTTAACGGCAGTTACTCG
>simulated_random_reads.fa.000000004
CATATTCTAATATCCTACTTCTGATACCCGATTATACACGACACCACCCCAGGACTGTCGTCACATCCTTATCTGGATAA
ACATCCGGTTCCGTTTGGCCGTGCTCCGCAAGTGATGCGTCTGTGGAATGTACGTGGAGCGTTGACAGTT
>simulated_random_reads.fa.000000005
CCGGATTAGGCATGTTTATAGTACAACGGATTCGCAAAAAGGTCAGGGTAACAATTTTGAAATGCTTTCATACTGCGGTC
TAAATGGACCACCCTTTAGGTGCAGCCAACTATAGTTGGTCGATTCTCTGAACACGTACCGAAGGCAATT
>simulated_random_reads.fa.000000006
AACCCATCGGAATAATCTACTGCTTCGTATGGAACGGTCCTACATTTAAATAAACGTGTCCAGTGCCACCCGATACCTCT
CGTCAATCAGGGGCTCTCCCTGAATCAGCAGTAAACAAACCCAGTACACTGTCGAACACTACTGAGACCG
>simulated_random_reads.fa.000000007
CCGAAGGCAAGTCTGTCGTAGAATGGTTTTTGTCGTTGTAACAACCCCGCTCTAGACCCTGAAAACCATAAAGTCAAGCC
CAACTAATATTAGAGGCATTCTGGCTACTCCCGCTCACCGCAATCTTCACATACTGTGATACCCTCAGCC
>simulated_random_reads.fa.000000008
ATATCCGTTAAACCCCGGATTTGACAATTCATCATCAACGCTACTAACGGCTTTCTCAATTTGGGGCTGTGGCCTATCCG
CATACGGCTACCTGCGCAAGAAGAGAGTACTGTTAGATGTCACGCTGCACTTGCGAAGACCGGTGGGCGT
>simulated_random_reads.fa.000000009
AGCGATGAGTACACAAGATGAGTGAAGGGATTAAACTTCAAACCTTGAAGTGTTACCCGATTTCCTACCATTGGGGATTC
GTTAATGCTTCGAATGGATCTATATCCGGTGTTTAGCTGACTGTTAAAATACTCTCGTTGTACGAAAGTA
>HMPMockV1.2.Staggered2.673827_0 M141:79:749142:1:1101:17530:1438
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGCAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACCTTCTGGTCTGTAACTGACGCTGATGTGCGAAAGCGTG
>HMPMockV1.2.Staggered2.673827_1 M141:79:749142:1:1101:17007:1451
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGTCTGTAACTTACGCTG
>HMPMockV1.2.Staggered2.673827_2 M141:79:749142:1:1101:16695:1471
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGTCTGTAACTGACGCTGATGTGCGAAAGCGTG
GGGA
>HMPMockV1.2.Staggered2.673827_3 M141:79:749142:1:1101:17203:1479
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGTAGAGATATGGAGGAACACCAGTGGCGAAGGCGACGTTCTGGTCTGTAACTGACGCTGATGTGCGAAAGCGTG
G
>HMPMockV1.2.Staggered2.673827_4 M141:79:749142:1:1101:14557:1490
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGGCTGTAACTGACGCTGATGTGCGCAAGCGTG
GTGATCAAACA
>HMPMockV1.2.Staggered2.673827_5 M141:79:749142:1:1101:16104:1491
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGTCTGTAACTGACGC
>HMPMockV1.2.Staggered2.673827_6 M141:79:749142:1:1101:16372:1491
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACAACAGTGGCGAAGGCGACTTTCTGGTCTGTAACTGACGCTGATGTGCGTAAG
>HMPMockV1.2.Staggered2.673827_7 M141:79:749142:1:1101:17334:1499
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGTCTGTAACTGACGCTGATGT
>HMPMockV1.2.Staggered2.673827_8 M141:79:749142:1:1101:17273:1504
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
AAATGCACAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGTCTGTAACTGACGCTGA
>HMPMockV1.2.Staggered2.673827_9 M141:79:749142:1:1101:16835:1505
TACGTAGGTGGCAAGCGTTATCCGGAATTATTGGGCGTAAAGCGCGCGTAGGCGGTTTTTTAAGTCTGATGTGAAAGCCC
ACGGCTCAACCGTGGAGGGTCATTGGAAACTGGAAAACTTGAGTGCAGAAGAGGAAAGTGGAATTCCATGTGTAGCGGTG
ACATGCGCAGAGATATGGAGGAACACCAGTGGCGAAGGCGACTTTCTGGTCTGTAACTGACGCTGATGTGCGAAAGCGTG
GGGAT
"""

if __name__ == '__main__':
    main()
