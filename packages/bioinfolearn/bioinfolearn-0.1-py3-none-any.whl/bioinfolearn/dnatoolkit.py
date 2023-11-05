import collections
from collections import Counter
from . utils import colored
from . structure import*

__all__ = ['validateSeq', 'countNucFrequency', 'transcription',
           'reverse_complement', 'gc_content', 'gc_content_subsec', 'translate_seq', 'codon_usage', 
           'gen_readin_frames', 'proteins_from_rf', 'all_proteins_from_orfs', 'readTextFile', 'writeTextFile',
          'read_FASTA', 'rna', 'helix', 'GC_Content', 'GC_kmer', 'AT_Content', 'AT_kmer', 'colored']


# check the sequence to make sure it is a DNA String
def validateSeq(dna_seq):
    tmpseq = dna_seq.upper()
    for nuc in tmpseq:
        if nuc not in Nucleotides:
            return False
    return tmpseq


"""
def countNucFrequency(seq):
    tmpFreqDict = {"A":0, "C":0, "G":0, "T":0}
    for nuc in seq:
        tmpFreqDict[nuc] +=1
    return tmpFreqDict
"""

def countNucFrequency(seq):
    return dict(collections.Counter(seq))

def transcription(seq):
    """
    DNA -> RNA Rranscription
    """
    return seq.replace("T","U")

""" 
def reverse_complement(seq):
    return ''.join([DNA_ReverseComplement[nuc] for nuc in seq])[::-1]
"""

def reverse_complement(seq):
    """ 
    Swappin adenine with thyimine and gaumine with cytosine 
    Reversing newly generated string
    """
    # python approach a little bit faster solution
    mapping = str.maketrans('ATCH', 'TAGC')
    return seq.translate(mapping)[::-1]

# GC Content Wiki, gc content tool , pmc
def gc_content(seq):
    """ 
    GC Content in a DNA/RNA sequence
    """
    return round(seq.count('C') + seq.count('G')/ len(seq)*100)

def gc_content_subsec(seq, k=20):
    """ 
    GC Content in a DNA/RNA subsequence 
    length k =20  by default 
    
    """
    
    res = []
    for i in range(0, len(seq)-k+1, k):
        subseq = seq[i:i+k]
        res.append(gc_content(subseq))
    return res 

# DNA codon table

def translate_seq(seq, init: int):
    return [DNA_Codons[seq[pos: pos + 3]] for pos in range(init, len(seq) - 2, 3)]

def codon_usage(seq, aminoacid):
    """ provides the frequency of each codon encoding a given aminoacid in a DNA sequence"""
    tmpList = []
    for i in range(0, len(seq)-2, 3):
        if DNA_Codons[seq[i:i+3]] == aminoacid:
            tmpList.append(seq[i:i+3])
            
    freqDict = dict(Counter(tmpList))
    totalWight = sum(freqDict.values())
    for seq in freqDict:
        freqDict[seq] = round(freqDict[seq]/ totalWight,2)
        
    return freqDict

# Ribosome wiki , NIH
def gen_readin_frames(seq):
    """
    Generate the six reading frames of a DNA sequence,
    including reverse complement 
    """
    frames = []
    frames.append(translate_seq(seq, 0))
    frames.append(translate_seq(seq, 1))
    frames.append(translate_seq(seq, 2))
    frames.append(translate_seq(reverse_complement (seq),0))
    frames.append(translate_seq(reverse_complement(seq), 1))
    frames.append(translate_seq(reverse_complement(seq), 2))
    
    return frames



def proteins_from_rf(aa_seq):
    """Compute all possible proteins in an aminoacid seq and return a list of possible proteins"""
    current_prot = []
    proteins = []
    for aa in  aa_seq:
        if aa == "_":
            # Stop accumulating amino acids if _ - STOP was found
            
            if current_prot:
                for p in current_prot:
                    proteins.append(p)
                current_prot= []
                
        else:
            # START accumulating amino acids if M - START  was found
            if aa == "M":
                current_prot.append("")
                
            for i in range(len(current_prot)):
                current_prot[i] += aa
                
    return proteins 

# Generate all RF
# Extrat all ports
# Return a list sorted/unsorted


def all_proteins_from_orfs(seq, startReadPos=0, endReadPos=0, orderd=False):
    """Compute all possible proteins for all open reading frames"""
    """protine search DB: https://www.ncbi.nlm.nih.gov/nuccore/NM_001185097.2"""
    """API can be used to pull proteins info"""
    
    if endReadPos > startReadPos:
        rfs = gen_readin_frames(seq[startReadPos:endReadPos])
        
    else:
        rfs = gen_readin_frames(seq)
        
    res = []
    for rf in rfs:
        prots = proteins_from_rf(rf)
        for p in prots:
            res.append(p)
            
    if orderd:
        return sorted(res, key=len, reverse=True)
    return res 

            
def readTextFile(filePath):
    with open(filePath, 'r') as f:
        return "".join([l.strip() for l in f.readlines()])    

def writeTextFile(filePath, seq, mode='w'):
    with open(filePath, mode) as f:
        f.write(seq+ '\n')
        
        
def read_FASTA(filePath):
    with open(filePath, 'r') as f:
        FASTAFile = [l.strip() for l in f.readlines()]
        
        
    FASTADict = {}
    FASTALabel = ""
    
    for line in FASTAFile:
        if '>' in line:
            FASTALabel = line
            FASTADict[FASTALabel] = ""
            
        else:
            FASTADict[FASTALabel] +=line
            
    return FASTADict
            
            
            
def rna(seq):
    print(" ")
    return "RNA sequence: " + "5' " + "-".join([colored(rna_complement[nuc]) for nuc in seq]) + " 3'"

def helix(seq):
    print('''
    
Double Helix
    ''')
    return f'''
5' {colored(seq)} 3'
   {len(seq) * "I"}
3' {reverse_complement(seq)} 5'
'''
     
     
def GC_Content(seq):
    return round(((seq.count("G") + seq.count("C")) / len(seq)) * 100)



def GC_kmer(seq, k):
    res = ["GC-Content"]
    gc_li = []
    n = 0
    if len(seq) - int(len(seq)) > 0:
        for l in range(int(round(len(seq) / k)) - 1):
            gc_li.clear()
            for i in range(k):
                gc_li.append(seq[n])
                n += 1
            percent = ((gc_li.count("G") + gc_li.count("C")) / len(gc_li)) * 100
            res.append(round(percent, 1))
        return res
    else:
        for l in range(int(round(len(seq) / k))):
            gc_li.clear()
            for i in range(k):
                try:
                    gc_li.append(seq[n])
                    n += 1
                except IndexError:
                    pass

            percent = ((gc_li.count("G") + gc_li.count("C")) / len(gc_li)) * 100
            res.append(round(percent, 1))
        return res

def AT_Content(seq):
    return round(((seq.count("A") + seq.count("T")) / len(seq)) * 100)

def AT_kmer(seq, k):
    res1 = ["AT-Content"]
    gc_li = []
    n = 0
    if len(seq) - int(len(seq)) > 0:
        for l in range(int(round(len(seq) / k)) - 1):
            gc_li.clear()
            for i in range(k):
                gc_li.append(seq[n])
                n += 1
            percent = ((gc_li.count("A") + gc_li.count("T")) / len(gc_li)) * 100
            res1.append(round(percent, 1))
        return res1
    else:
        for l in range(int(round(len(seq) / k))):
            gc_li.clear()
            for i in range(k):
                try:
                    gc_li.append(seq[n])
                    n += 1
                except IndexError:
                    pass
            percent = ((gc_li.count("A") + gc_li.count("T")) / len(gc_li)) * 100
            res1.append(round(percent, 1))
        return res1   