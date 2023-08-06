from locus import Locus

class Transcript(Locus):
    def __init__(
            self,
            transcript_id,
            db):
        assert isinstance(transcript_id, (unicode, str)), \
            "Expected transcript ID to be string, got %s : %s" % (
            transcript_id, type(transcript_id)
        )

        self.id = transcript_id
        self.db = db
        query = """
            SELECT
                transcript_name,
                seqname, start, end, strand,
                gene_name, gene_id
            FROM ensembl
            WHERE transcript_id = ?
        """
        cursor = db.execute(query, [transcript_id])
        result = cursor.fetchone()
        if result is None:
            raise ValueError("Transcript ID not found: %s" % transcript_id)

        transcript_name, contig, start, end, strand, gene_name, gene_id = result


        if not transcript_name:
            raise ValueError(
                "Missing name for transcript with ID = %s" % transcript_name
            )

        self.name = transcript_name

        if gene_name is None:
            raise ValueError(
                "Missing gene name for transcript with ID = %s" % transcript_id
            )
        self.gene_name = gene_name

        if gene_id is None:
            raise ValueError(
                "Missing gene ID for transcript with ID = %s" % transcript_id
            )
        self.gene_id = gene_id

        Locus.__init__(self, contig, start, end, strand)


    def __str__(self):
        return "Transcript(id=%s, name=%s, gene_name=%s)" % (
                    self.id, self.name, self.gene_name)

    def __repr__(self):
        return str(self)

    """
    TODO: Implement exon objects and this cached property
    @property
    def exons(self):
        if not hasattr(self, "_exons"):
            exons = ...
            self._exons = exons
        return self._exons
    """