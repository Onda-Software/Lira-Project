from multiprocessing import Pool
from multiprocessing import Process

def f(x):
    print(x)
    return x

if __name__ == "__main__":
    #with Pool(5) as p:
     #   print(p.map(f, [1, 2, 3]))
      #  print(p.map_async(f, [2]).get())

    process = Process(target=f, args=('ola',))
    print(process.start())
    process.join()
    
