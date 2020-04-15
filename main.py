#! /usr/bin/python3
import pickle, math, random, time
import pywren_ibm_cloud as pywren
import numpy as np
from sys import argv
from cos_backend import COSBackend

dic = { 
	    # Add here definitions to access COS {endpoint, access_key, secret,key}
    }

def push_matrix(m, n, l, w):
    obj = COSBackend(dic)
    # Generate random matrix
    matrix1 = np.random.randint(-5, 6, size=(m, n))
    matrix2 = np.random.randint(-5, 11, size=(n, l))
    # Push A submatrix
    for i in range(0, w):
        infM = int((i * m) / w)
        supM = int((((i + 1) * m) / w) - 1)
        submatrix1 = matrix1[infM:supM+1, :]
        obj.put_object('prac1', 'A' + str(i) + '.mtx', pickle.dumps(submatrix1))
    # Push B submatrix
    for j in range (0, w):
        infL = int((j * l) / w)
        supL = int((((j + 1) * l) / w) - 1)
        submatrix2 = matrix2[:, infL:supL+1]
        obj.put_object('prac1', 'B' + str(j) + '.mtx', pickle.dumps(submatrix2))

def map_function(i, j):
    obj2 = COSBackend(dic)
    # Get submatrix
    m1 = pickle.loads(obj2.get_object('prac1', 'A' + str(i) + '.mtx'))
    m2 = pickle.loads(obj2.get_object('prac1', 'B' + str(j) + '.mtx'))
    # Calculate multiplication
    result = m1.dot(m2)
    return result

def reduce_function(results):
    # Concatenation of submatrix
    f = []
    num_results = len(results)
    r = int(math.sqrt(num_results))
    g = results[0]
    for i in range(0, r-1):
        g = np.concatenate((g, results[i*1+1]), axis=1)
    f = g
    for i in range(1, r):
        g = results[i*r]
        for j in range(0, r-1):
            g = np.concatenate((g, results[i*r+j+1]), axis=1)
        f = np.concatenate((f, g), axis=0)
    return f
    #return 0 

if __name__ == "__main__":
    m = int(argv[1])
    n = int(argv[2])
    l = int(argv[3])
    w = int(argv[4])
    if (w > m or w > n or w > l or w > 10):
        print("Worker's number is too big")
        exit()
    # Create the executor
    pw = pywren.ibm_cf_executor()
    # Matrix generation & push to COS (cloud execution)
    r = pw.call_async(push_matrix, [m, n, l, w])
    pw.wait(r)
    # Create iterdata
    iterdata = []
    for i in range(0, w):
        for j in range (0, w):
            iterdata.append([i, j])
    # Calculate in the cloud
    start_time = time.time()
    if (w == 1):
        futures = pw.call_async(map_function, [0, 0])
    else:
        futures = pw.map_reduce(map_function, iterdata, reduce_function)
    pw.wait(futures)
    elapsed_time = time.time() - start_time
    print(str(elapsed_time) + " seconds\n")
    print("RESULTANT MATRIX\n", pw.get_result())