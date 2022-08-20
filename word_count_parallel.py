# See http://a-coda.tumblr.com/
 
import os
import re
from collections import Counter
from time import time
from multiprocessing import Pool
 
def find_files ( root, extension ):
    for dirpath, dirname, filenames in os.walk( root ):
        for name in filenames:
            if name.endswith( extension ):
                yield os.path.join( dirpath, name )
 
def find_lines ( filename ):
    with open( filename ) as stream:
        yield from stream.readlines()
 
def find_words ( filename ):
    for line in find_lines( filename ):
        yield re.findall( r'\w+', line )
 
def count_words ( filename ):
    return accumulate( find_words( filename ) )
 
def accumulate ( values ):
    counts = Counter()
    for value in values:
        counts.update( value )
    return counts
 
def main ():
    start = time()
    files = [ filename for filename in find_files( ".", ".java" ) ]
    file_counts = Pool().map( count_words, files )
    counts = accumulate( file_counts )
    common = counts.most_common( 20 )
    end = time()
    for word, count in common:
        print( word, count )
    print( "files: %d" % ( len( files ) ) )
    print( "time: %f" % ( end - start ) )
 
if __name__ == '__main__':
    main()
