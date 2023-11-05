# Generic for loop solution:

def count_kmer_loop(sequence, kmer):
    kmer_count = 0
    for position in range(len(sequence)- (len(kmer)-1)):
        if sequence[position:position + len(kmer)] == kmer:
            kmer_count +=1
    return kmer_count



# List comprehension solution :

def count_kmer_listcomp(sequence, kmer):
    kmer_list = [sequence[pos:pos + len(kmer)]
                 for pos in range(len(sequence) - (len(kmer)- 1))] 
    
    return kmer_list.count(kmer)