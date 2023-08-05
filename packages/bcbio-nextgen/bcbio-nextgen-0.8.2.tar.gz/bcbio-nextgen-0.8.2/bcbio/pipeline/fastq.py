"""Pipeline utilities to retrieve FASTQ formatted files for processing.
"""
import os

from bcbio import bam, broad, utils
from bcbio.bam import fastq
from bcbio.bam import cram
from bcbio.pipeline import alignment
from bcbio.utils import file_exists, safe_makedir
from bcbio.provenance import do

def get_fastq_files(item):
    """Retrieve fastq files for the given lane, ready to process.
    """
    assert "files" in item, "Did not find `files` in input; nothing to process"
    ready_files = []
    for fname in item["files"]:
        if fname.endswith(".bam"):
            if _pipeline_needs_fastq(item["config"], item):
                ready_files = _convert_bam_to_fastq(fname, item["dirs"]["work"],
                                                    item, item["dirs"], item["config"])
            else:
                ready_files = [fname]
        elif fname.startswith(utils.SUPPORTED_REMOTES):
            ready_files.append(fname)
        else:
            ready_files.append(fname)
    ready_files = [x for x in ready_files if x is not None]
    ready_files = [_gzip_fastq(x) for x in ready_files]
    for in_file in ready_files:
        assert os.path.exists(in_file), "%s does not exist." % in_file
    return ((ready_files[0] if len(ready_files) > 0 else None),
            (ready_files[1] if len(ready_files) > 1 else None))

def _gzip_fastq(in_file):
    """
    gzip a fastq file if it is not already gzipped
    """
    if fastq.is_fastq(in_file) and not utils.is_gzipped(in_file):
        gzipped_file = in_file + ".gz"
        if file_exists(gzipped_file):
            return gzipped_file
        message = "gzipping {in_file}.".format(in_file=in_file)
        do.run("gzip -c {in_file} > {gzipped_file}".format(**locals()), message)
        return gzipped_file
    return in_file

def _pipeline_needs_fastq(config, item):
    """Determine if the pipeline can proceed with a BAM file, or needs fastq conversion.
    """
    aligner = config["algorithm"].get("aligner")
    support_bam = aligner in alignment.metadata.get("support_bam", [])
    return aligner and not support_bam

def _convert_bam_to_fastq(in_file, work_dir, item, dirs, config):
    """Convert BAM input file into FASTQ files.
    """
    out_dir = safe_makedir(os.path.join(work_dir, "fastq_convert"))

    qual_bin_method = config["algorithm"].get("quality_bin")
    if (qual_bin_method == "prealignment" or
         (isinstance(qual_bin_method, list) and "prealignment" in qual_bin_method)):
        out_bindir = safe_makedir(os.path.join(out_dir, "qualbin"))
        in_file = cram.illumina_qual_bin(in_file, item["sam_ref"], out_bindir, config)

    out_files = [os.path.join(out_dir, "{0}_{1}.fastq".format(
                 os.path.splitext(os.path.basename(in_file))[0], x))
                 for x in ["1", "2"]]
    if bam.is_paired(in_file):
        out1, out2 = out_files
    else:
        out1 = out_files[0]
        out2 = None
    if not file_exists(out1):
        broad_runner = broad.runner_from_config(config)
        broad_runner.run_fn("picard_bam_to_fastq", in_file, out1, out2)
    if out2 and os.path.getsize(out2) == 0:
        out2 = None
    return [out1, out2]
