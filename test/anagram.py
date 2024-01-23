from multiprocessing import Process, Pipe

def insert_element(element_list, connection):
    
    filtered_elements = []

    for element in element_list:
        if(not element in filtered_elements and element != []):
            filtered_elements.append(element)
    
    connection.send(filtered_elements)
    connection.close()

text = "Test of anagram neural"
text_divisions = []

for index in range(0, len(text.split())):
    
    text_divisions += [
        text.split()[:],
        [text.split()[index]],
        text.split()[:index],
        text.split()[index:],
        text.split()[index-1:index+1],
    ]

parent_conn, child_conn = Pipe()
process = Process(target=insert_element, args=(text_divisions, child_conn,))
process.start()

input_sequences = parent_conn.recv()
if (process.join()): pass
