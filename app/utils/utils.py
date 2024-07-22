from Bio import SeqIO, Entrez
import requests
import os

dbfrom = "nucleotide"
db = "gene"


def find_cds(seqrecord):
    """Fonction used to find the coding area on a gene.

    Returns the start and end location of the coding area on a gene.
    """
    result = []
    couplePosition = tuple()

    for f in seqrecord.features:
        if f.type == "CDS":
            couplePosition = (f.location._start.position, f.location._end.position)
            result.append(couplePosition)

    return result


def mrna_to_gene(num_accession):
    """Search for the id of gene given the number of accession of a mrna.

    Returns the id of the gene from the gene data base.
    """

    handle = Entrez.elink(dbfrom=dbfrom, db=db, id=num_accession)
    record = Entrez.read(handle)
    handle.close()

    try:
        linked = [link["Id"] for link in record[0]["LinkSetDb"][0]["Link"]]
        return linked[0]
    except ValueError:
        print("No id found...")


def get_genom_id_accession(id_gene):
    """Search for the id accession fo the chromosom given a gene id.

    Returns the id accession of chromosomes.
    """

    handle = Entrez.esummary(db=db, id=id_gene)
    record = Entrez.read(handle)
    handle.close()

    dictElem = dict(record)["DocumentSummarySet"]
    premierElem = dict(dictElem)["DocumentSummary"]
    info = []

    for e in premierElem:
        for stuff in dict(e).items():
            if stuff[0] == "GenomicInfo":
                info = stuff[1]

    return info[0]["ChrAccVer"]


def get_seq_start_stop(id_gene):
    """Search for the start and end sequence from a gene.

    Given an id of a gene, search for the start and end position of it sequence on the gene.
    """
    seq_start = 0
    seq_stop = 0

    handle = Entrez.esummary(db=db, id=id_gene)
    record = Entrez.read(handle)
    handle.close()

    dictElem = dict(record)["DocumentSummarySet"]
    premierElem = dict(dictElem)["DocumentSummary"]
    info = []

    for e in premierElem:
        for stuff in dict(e).items():
            if stuff[0] == "GenomicInfo":
                info = stuff[1]

    seq_start = info[0]["ChrStart"]
    seq_stop = info[0]["ChrStop"]

    return seq_start, seq_stop


def upstream_gene_seq(id_gene, seq_length):
    """Find the upstream sequence of a gene.
    Return the promotor sequence of a gene.
    """

    seq_start, seq_stop = get_seq_start_stop(id_gene)
    genom_accession = get_genom_id_accession(id_gene)

    if seq_start < seq_stop:
        handle = Entrez.efetch(
            db=dbfrom,
            id=genom_accession,
            rettype="fasta",
            strand=1,
            retmode="text",
            seq_start=str(int(seq_start) - seq_length),
            seq_stop=seq_start,
        )
        genomic_record = SeqIO.read(handle, "fasta")
    else:
        handle = Entrez.efetch(
            db=dbfrom,
            id=genom_accession,
            rettype="fasta",
            strand=-1,
            retmode="text",
            seq_start=str(int(seq_start) + 2),
            seq_stop=str(int(seq_start) + seq_length),
        )
        genomic_record = SeqIO.read(handle, "fasta")

    handle.close()

    return genomic_record


def download_motif(motif_id, out_put_dir):
    """Download a motif from the JASPAR API and save it in the JASPAR format."""
    url = f"https://jaspar2020.genereg.net/api/v1/matrix/{motif_id}/"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    pfm = data["pfm"]
    jaspar_format = f">{motif_id}\t{data['name']}\n"
    jaspar_format += "A  [ " + " ".join(f"{int(x):>5}" for x in pfm["A"]) + " ]\n"
    jaspar_format += "C  [ " + " ".join(f"{int(x):>5}" for x in pfm["C"]) + " ]\n"
    jaspar_format += "G  [ " + " ".join(f"{int(x):>5}" for x in pfm["G"]) + " ]\n"
    jaspar_format += "T  [ " + " ".join(f"{int(x):>5}" for x in pfm["T"]) + " ]\n"

    filename = os.path.join(out_put_dir, motif_id + ".jaspar")
    with open(filename, "w") as f:
        f.write(jaspar_format)
    print("Download done.")


def download_promotors(ids_mrna_list, seq_length, out_put_dir):
    """Download promotors sequences for a list of MRNA as fasta files."""
    print("Downloading files, please wait:")
    for id_mrna in ids_mrna_list:
        print("Fetching data for gene: " + id_mrna)
        id_gene = mrna_to_gene(id_mrna)
        seq = upstream_gene_seq(id_gene, seq_length)
        filename = os.path.join(out_put_dir, id_mrna + "_" + str(seq_length) + ".fa")
        SeqIO.write(seq, filename, "fasta")
        print("Download done.")


def Seq_obj_from_files(files_list):
    """Take a list of promotor sequences from fasta files.

    Return a list of SeqRecord objects.
    """

    seq_obj_list = list()

    for file in files_list:
        seq_object = SeqIO.read(file, "fasta")
        seq_obj_list.append(seq_object)

    return seq_obj_list
