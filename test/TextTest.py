text = 'test with a text'

total_seq = 0x00
sequences = []
clean_seq = []

sequences.append(text.split()[:])

for index in range(1, len(text.split())):
    
    sequences.append([text.split()[index]])
    sequences.append(text.split()[:index])
    sequences.append(text.split()[index:])
    sequences.append(text.split()[index-1:index+1])
    
for seq in sequences:
    if seq not in clean_seq:
        clean_seq.append(seq)

total_seq += len(clean_seq)
sequences = clean_seq
