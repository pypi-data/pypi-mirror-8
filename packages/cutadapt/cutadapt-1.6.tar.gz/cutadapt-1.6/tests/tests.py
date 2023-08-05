# TODO
# test with the --output option
# test reading from standard input
from __future__ import print_function, division, absolute_import

import sys, os
from nose.tools import raises
from contextlib import contextmanager
from cutadapt.scripts import cutadapt

@contextmanager
def redirect_stderr():
	"Send stderr to stdout. Nose doesn't capture stderr, yet."
	old_stderr = sys.stderr
	sys.stderr = sys.stdout
	yield
	sys.stderr = old_stderr


def dpath(path):
	"""
	get path to a data file (relative to the directory this test lives in)
	"""
	return os.path.join(os.path.dirname(__file__), path)


def datapath(path):
	return dpath(os.path.join('data', path))


def files_equal(path1, path2):
	return os.system("diff -u {0} {1}".format(path1, path2)) == 0


def run(params, expected, inpath, inpath2=None):
	if type(params) is str:
		params = params.split()
	#params = ['--quiet'] + params
	params += ['-o', dpath('tmp.fastaq') ] # TODO not parallelizable
	params += [ datapath(inpath) ]
	if inpath2:
		params += [ datapath(inpath2) ]

	assert cutadapt.main(params) is None
	# TODO redirect standard output
	assert files_equal(dpath(os.path.join('cut', expected)), dpath('tmp.fastaq'))
	os.remove(dpath('tmp.fastaq'))
	# TODO diff log files
	#echo "Running $CA $1 data/$3 ${second}"
	#if ! $CA $1 "data/$3" -o tmp.fastaq ${second} > tmp.log; then
		#cat tmp.log
		#exit 1
	#fi
	#sed -i '/Total time/d;/Time per read/d;/cutadapt version/d;/^Command line /d' tmp.log
	#diff -u cut/$2 tmp.fastaq
	#diff -u tmp.log log/$2.log


def test_example():
	run(["-b", "ADAPTER"], 'example.fa', 'example.fa')

def test_small():
	run(["-b", "TTAGACATATCTCCGTCG"], 'small.fastq', 'small.fastq')

def test_empty():
	'''empty input'''
	run(["-a", "TTAGACATATCTCCGTCG"], 'empty.fastq', 'empty.fastq')

def test_newlines():
	'''DOS/Windows newlines'''
	run("-e 0.12 -b TTAGACATATCTCCGTCG", "dos.fastq", "dos.fastq")

def test_lowercase():
	'''lower case adapter'''
	run("-b ttagacatatctccgtcg", "lowercase.fastq", "small.fastq")


def test_rest():
	'''-r/--rest-file'''
	run(['-b', 'ADAPTER', '-r', dpath('rest.tmp')], "rest.fa", "rest.fa")
	assert files_equal(datapath('rest.txt'), dpath('rest.tmp'))
	os.remove(dpath('rest.tmp'))


def test_restfront():
	run(['-g', 'ADAPTER', '-r', dpath('rest.tmp')], "restfront.fa", "rest.fa")
	assert files_equal(datapath('restfront.txt'), dpath('rest.tmp'))
	os.remove(dpath('rest.tmp'))


def test_discard():
	'''--discard'''
	run("-b TTAGACATATCTCCGTCG --discard", "discard.fastq", "small.fastq")


def test_discard_untrimmed():
	'''--discard-untrimmed'''
	run('-b CAAGAT --discard-untrimmed', 'discard-untrimmed.fastq', 'small.fastq')


def test_plus():
	'''test if sequence name after the "+" is retained'''
	run("-e 0.12 -b TTAGACATATCTCCGTCG", "plus.fastq", "plus.fastq")


def test_extensiontxtgz():
	'''automatic recognition of "_sequence.txt.gz" extension'''
	run("-b TTAGACATATCTCCGTCG", "s_1_sequence.txt", "s_1_sequence.txt.gz")


def test_format():
	'''the -f/--format parameter'''
	run("-f fastq -b TTAGACATATCTCCGTCG", "small.fastq", "small.myownextension")


def test_minimum_length():
	'''-m/--minimum-length'''
	run("-c -m 5 -a 330201030313112312", "minlen.fa", "lengths.fa")


def test_too_short():
	'''--too-short-output'''
	run("-c -m 5 -a 330201030313112312 --too-short-output tooshort.tmp.fa", "minlen.fa", "lengths.fa")
	assert files_equal(datapath('tooshort.fa'), "tooshort.tmp.fa")
	os.remove('tooshort.tmp.fa')


def test_too_short_no_primer():
	'''--too-short-output and --trim-primer'''
	run("-c -m 5 -a 330201030313112312 --trim-primer --too-short-output tooshort.tmp.fa", "minlen.noprimer.fa", "lengths.fa")
	assert files_equal(datapath('tooshort.noprimer.fa'), "tooshort.tmp.fa")
	os.remove('tooshort.tmp.fa')


def test_maximum_length():
	'''-M/--maximum-length'''
	run("-c -M 5 -a 330201030313112312", "maxlen.fa", "lengths.fa")


def test_too_long():
	'''--too-long-output'''
	run("-c -M 5 --too-long-output toolong.tmp.fa -a 330201030313112312", "maxlen.fa", "lengths.fa")
	assert files_equal(datapath('toolong.fa'), "toolong.tmp.fa")
	os.remove('toolong.tmp.fa')


def test_length_tag():
	'''454 data; -n and --length-tag'''
	run("-n 3 -e 0.1 --length-tag length= " \
		"-b TGAGACACGCAACAGGGGAAAGGCAAGGCACACAGGGGATAGG "\
		"-b TCCATCTCATCCCTGCGTGTCCCATCTGTTCCCTCCCTGTCTCA", '454.fa', '454.fa')

def test_overlap_a():
	'''-O/--overlap with -a (-c omitted on purpose)'''
	run("-O 10 -a 330201030313112312", "overlapa.fa", "overlapa.fa")

def test_overlap_b():
	'''-O/--overlap with -b'''
	run("-O 10 -b TTAGACATATCTCCGTCG", "overlapb.fa", "overlapb.fa")

def test_qualtrim():
	'''-q with low qualities'''
	run("-q 10 -a XXXXXX", "lowqual.fastq", "lowqual.fastq")

def test_qualtrim_csfastaqual():
	'''-q with csfasta/qual files'''
	run("-c -q 10", "solidqual.fastq", "solid.csfasta", 'solid.qual')

def test_qualbase():
	'''-q with low qualities, using ascii(quality+64) encoding'''
	run("-q 10 --quality-base 64 -a XXXXXX", "illumina64.fastq", "illumina64.fastq")

def test_quality_trim_only():
	'''only trim qualities, do not remove adapters'''
	run("-q 10 --quality-base 64", "illumina64.fastq", "illumina64.fastq")

def test_twoadapters():
	'''two adapters'''
	run("-b CTCGAGAATTCTGGATCCTC -b GAGGATCCAGAATTCTCGAGTT", "twoadapters.fasta", "twoadapters.fasta")

def test_bwa():
	'''MAQ-/BWA-compatible output'''
	run("-c -e 0.12 -a 330201030313112312 -x 552: --maq", "solidmaq.fastq", "solid.csfasta", 'solid.qual')

def test_bfast():
	'''BFAST-compatible output'''
	run("-c -e 0.12 -a 330201030313112312 -x abc: --strip-f3", "solidbfast.fastq", "solid.csfasta", 'solid.qual')

def test_polya():
	'''poly-A tails'''
	run("-m 24 -O 10 -a AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "polya.fasta", "polya.fasta")

def test_trim_095():
	'''some reads properly trimmed since cutadapt 0.9.5'''
	run("-c -e 0.122 -a 330201030313112312", "solid.fasta", "solid.fasta")

def test_mask_adapter():
	'''mask adapter with N (reads maintain the same length)'''
	run("-b CAAG -n 3 --mask-adapter", "anywhere_repeat.fastq", "anywhere_repeat.fastq")

def test_gz_multiblock():
	'''compressed gz file with multiple blocks (created by concatenating two .gz files)'''
	run("-b TTAGACATATCTCCGTCG", "small.fastq", "multiblock.fastq.gz")

def test_suffix():
	'''-y/--suffix parameter, combined with _F3'''
	run("-c -e 0.12 -a 330201030313112312 -y _my_suffix --strip-f3", "suffix.fastq", "solid.csfasta", 'solid.qual')

def test_read_wildcard():
	'''test wildcards in reads'''
	run("--match-read-wildcards -b ACGTACGT", "wildcard.fa", "wildcard.fa")

def test_adapter_wildcard():
	'''wildcards in adapter'''
	wildcardtmp = dpath("wildcardtmp.txt")
	for adapter_type, expected in (("-a", "wildcard_adapter.fa"),
		("-b", "wildcard_adapter_anywhere.fa")):
		run("--wildcard-file {0} {1} ACGTNNNACGT".format(wildcardtmp, adapter_type),
			expected, "wildcard_adapter.fa")
		lines = open(wildcardtmp, 'rt').readlines()
		lines = [ line.strip() for line in lines ]
		assert lines == ['AAA 1', 'GGG 2', 'CCC 3b', 'TTT 4b']
		os.remove(wildcardtmp)

def test_wildcard_N():
	'''test 'N' wildcard matching with no allowed errors'''
	run("-e 0 -a GGGGGGG --match-read-wildcards", "wildcardN.fa", "wildcardN.fa")

def test_adapter_front():
	'''test adapter in front'''
	run("--front ADAPTER", "examplefront.fa", "example.fa")

def test_literal_N():
	'''test matching literal 'N's'''
	run("-N -e 0.2 -a NNNNNNNNNNNNNN", "trimN3.fasta", "trimN3.fasta")

def test_literal_N2():
	run("-N -O 1 -g NNNNNNNNNNNNNN", "trimN5.fasta", "trimN5.fasta")

def test_anchored_front():
	run("-g ^FRONTADAPT", "anchored.fasta", "anchored.fasta")

def test_solid():
	run("-c -e 0.122 -a 330201030313112312", "solid.fastq", "solid.fastq")

def test_solid_basespace_adapter():
	'''colorspace adapter given in basespace'''
	run("-c -e 0.122 -a CGCCTTGGCCGTACAGCAG", "solid.fastq", "solid.fastq")

def test_solid5p():
	'''test 5' colorspace adapter'''
	# this is not a real adapter, just a random string
	# in colorspace: C0302201212322332333
	run("-c -e 0.1 --trim-primer -g CCGGAGGTCAGCTCGCTATA", "solid5p.fasta", "solid5p.fasta")

def test_solid5p_prefix_notrim():
	'''test anchored 5' colorspace adapter, no primer trimming'''
	run("-c -e 0.1 -g ^CCGGAGGTCAGCTCGCTATA", "solid5p-anchored.notrim.fasta", "solid5p.fasta")

def test_solid5p_prefix():
	'''test anchored 5' colorspace adapter'''
	run("-c -e 0.1 --trim-primer -g ^CCGGAGGTCAGCTCGCTATA", "solid5p-anchored.fasta", "solid5p.fasta")

def test_solid5p_fastq():
	'''test 5' colorspace adapter'''
	# this is not a real adapter, just a random string
	# in colorspace: C0302201212322332333
	run("-c -e 0.1 --trim-primer -g CCGGAGGTCAGCTCGCTATA", "solid5p.fastq", "solid5p.fastq")

def test_solid5p_prefix_notrim_fastq():
	'''test anchored 5' colorspace adapter, no primer trimming'''
	run("-c -e 0.1 -g ^CCGGAGGTCAGCTCGCTATA", "solid5p-anchored.notrim.fastq", "solid5p.fastq")

def test_solid5p_prefix_fastq():
	'''test anchored 5' colorspace adapter'''
	run("-c -e 0.1 --trim-primer -g ^CCGGAGGTCAGCTCGCTATA", "solid5p-anchored.fastq", "solid5p.fastq")

def test_sra_fastq():
	'''test SRA-formatted colorspace FASTQ'''
	run("-c -e 0.1 --format sra-fastq -a CGCCTTGGCCGTACAGCAG", "sra.fastq", "sra.fastq")

def test_issue_46():
	'''issue 46 - IndexError with --wildcard-file'''
	wildcardtmp = dpath("wildcardtmp.txt")
	run("--anywhere=AACGTN --wildcard-file={0}".format(wildcardtmp), "issue46.fasta", "issue46.fasta")
	os.remove(wildcardtmp)

def test_strip_suffix():
	run("--strip-suffix _sequence -a XXXXXXX", "stripped.fasta", "simple.fasta")


# note: the actual adapter sequence in the illumina.fastq.gz data set is
# GCCTAACTTCTTAGACTGCCTTAAGGACGT (fourth base is different)
def test_info_file():
	infotmp = dpath("infotmp.txt")
	run(["--info-file", infotmp, '-a', 'adapt=GCCGAACTTCTTAGACTGCCTTAAGGACGT'], "illumina.fastq", "illumina.fastq.gz")
	assert files_equal(dpath(os.path.join('cut', 'illumina.info.txt')), infotmp)
	os.remove(infotmp)


def test_named_adapter():
	run("-a MY_ADAPTER=GCCGAACTTCTTAGACTGCCTTAAGGACGT", "illumina.fastq", "illumina.fastq.gz")


def test_adapter_with_U():
	run("-a GCCGAACUUCUUAGACUGCCUUAAGGACGU", "illumina.fastq", "illumina.fastq.gz")


def test_no_trim():
	''' --no-trim '''
	run("--no-trim --discard-untrimmed -a CCCTAGTTAAAC", 'no-trim.fastq', 'small.fastq')

def test_bzip2():
	'''test bzip2 support'''
	run('-b TTAGACATATCTCCGTCG', 'small.fastq', 'small.fastq.bz2')


def test_paired_separate():
	'''test separate trimming of paired-end reads'''
	run('-a TTAGACATAT', 'paired.1.fastq', 'paired.1.fastq')
	run('-a CAGTGGAGTA', 'paired.2.fastq', 'paired.2.fastq')


@raises(SystemExit)
def test_no_args():
	with redirect_stderr():
		cutadapt.main()


@raises(SystemExit)
def test_paired_end_missing_file():
	with redirect_stderr():
		cutadapt.main(['-a', 'XX', '--paired-output', 'out.fastq', datapath('paired.1.fastq')])


@raises(SystemExit)
def test_first_too_short():
	# paired-truncated.1.fastq is paired.1.fastq without the last read
	with redirect_stderr():
		cutadapt.main('-a XX --paired-output out.fastq'.split() + [datapath('paired-truncated.1.fastq'), datapath('paired.2.fastq')])


@raises(SystemExit)
def test_second_too_short():
	# paired-truncated.2.fastq is paired.2.fastq without the last read
	with redirect_stderr():
		cutadapt.main('-a XX --paired-output out.fastq'.split() + [datapath('paired.1.fastq'), datapath('paired-truncated.2.fastq')])


@raises(SystemExit)
def test_unmatched_read_names():
	# paired-swapped.1.fastq: paired.1.fastq with reads 2 and 3 swapped
	with redirect_stderr():
		cutadapt.main('-a XX --paired-output out.fastq'.split() + [datapath('paired-swapped.1.fastq'), datapath('paired.2.fastq')])


def test_paired_end():
	'''--paired-output'''
	pairedtmp = dpath("paired-tmp.fastq")
	# the -m 14 filters out one read, which should then also be filtered out in the second output file
	run(['-a', 'TTAGACATAT', '-m', '14', '--paired-output', pairedtmp], 'paired.m14.1.fastq', 'paired.1.fastq', 'paired.2.fastq')
	assert files_equal(dpath(os.path.join('cut', 'paired.m14.2.fastq')), pairedtmp)
	os.remove(pairedtmp)


def test_anchored_no_indels():
	'''anchored 5' adapter, mismatches only (no indels)'''
	run('-g ^TTAGACATAT --no-indels -e 0.1', 'anchored_no_indels.fasta', 'anchored_no_indels.fasta')


def test_anchored_no_indels_wildcard_read():
	'''anchored 5' adapter, mismatches only (no indels), but wildcards in the read count as matches'''
	run('-g ^TTAGACATAT --match-read-wildcards --no-indels -e 0.1', 'anchored_no_indels_wildcard.fasta', 'anchored_no_indels.fasta')


def test_anchored_no_indels_wildcard_adapt():
	'''anchored 5' adapter, mismatches only (no indels), but wildcards in the adapter count as matches'''
	run('-g ^TTAGACANAT --no-indels -e 0.1', 'anchored_no_indels.fasta', 'anchored_no_indels.fasta')


def test_unconditional_cut_front():
	run('-u 5', 'unconditional-front.fastq', 'small.fastq')


def test_unconditional_cut_back():
	run('-u -5', 'unconditional-back.fastq', 'small.fastq')


def test_no_zero_cap():
	run("--no-zero-cap -c -e 0.122 -a CGCCTTGGCCGTACAGCAG", "solid-no-zerocap.fastq", "solid.fastq")


def test_untrimmed_output():
	tmp = dpath('untrimmed.tmp.fastq')
	run(['-a', 'TTAGACATATCTCCGTCG', '--untrimmed-output', tmp], 'small.trimmed.fastq', 'small.fastq')
	assert files_equal(dpath(os.path.join('cut', 'small.untrimmed.fastq')), tmp)
	os.remove(tmp)


def test_untrimmed_paired_output():
	paired1 = datapath('paired.1.fastq')
	paired2 = datapath('paired.2.fastq')
	tmp1 = dpath("tmp-paired.1.fastq")
	tmp2 = dpath("tmp-paired.2.fastq")
	untrimmed1 = dpath("tmp-untrimmed.1.fastq")
	untrimmed2 = dpath("tmp-untrimmed.2.fastq")

	params = ['--quiet', '-a', 'TTAGACATAT', '-o', tmp1, '-p', tmp2, '--untrimmed-output', untrimmed1, '--untrimmed-paired-output', untrimmed2, paired1, paired2]
	assert cutadapt.main(params) is None

	assert files_equal(dpath(os.path.join('cut', 'paired-untrimmed.1.fastq')), untrimmed1)
	assert files_equal(dpath(os.path.join('cut', 'paired-untrimmed.2.fastq')), untrimmed2)
	assert files_equal(dpath(os.path.join('cut', 'paired-trimmed.1.fastq')), tmp1)
	assert files_equal(dpath(os.path.join('cut', 'paired-trimmed.2.fastq')), tmp2)
	os.remove(tmp1)
	os.remove(tmp2)
	os.remove(untrimmed1)
	os.remove(untrimmed2)


def test_adapter_file():
	run('-a file:' + datapath('adapter.fasta'), 'illumina.fastq', 'illumina.fastq.gz')


def test_explicit_format_with_paired():
	pairedtmp = dpath("paired-tmp.fastq")
	run(['--format=fastq', '-a', 'TTAGACATAT', '-m', '14', '-p', pairedtmp], 'paired.m14.1.fastq', 'paired.1.txt', 'paired.2.txt')
	assert files_equal(dpath(os.path.join('cut', 'paired.m14.2.fastq')), pairedtmp)
	os.remove(pairedtmp)


def test_no_trimming():
	# make sure that this doesn't divide by zero
	cutadapt.main(['-a', 'XXXXX', '-o', '/dev/null', '-p', '/dev/null', datapath('paired.1.fastq'), datapath('paired.2.fastq')])
