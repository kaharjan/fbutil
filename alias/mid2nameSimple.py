#!/usr/bin/env python2.7
"""
Script to convert mid to name in FB.
"""
import gzip
import logging

logging.basicConfig(format='%(asctime)s %(message)s')
log = logging.getLogger()
log.setLevel(logging.INFO) # DEBUG, INFO, WARN, ERROR, CRITICAL

def read_mids_names(f):
    log.info('Reading mids,names..')
    mids = frozenset([m.strip().split("\t")[0] for m in gzip.open(f, 'rb').readlines()])
    log.info('...len of mids (%d).' % len(mids))
    names_dict={}
    for m in gzip.open(f,'rb').readlines():
	mid,name=m.strip().split('\t')
	names_dict[mid]=name	
    log.info('..len of name_dict (%d).' % len(names_dict))
    return mids,names_dict



def mid(s):
    s = s.strip('<>')
    if s.startswith('http://rdf.freebase.com/ns/m.'):
        return s[27:]
    else:
	return s
    

def main(midsf, inputfile_name, outputfile_name):
    midDict={}
    midDict2={}
    mid_set,name_dict = read_mids_names(midsf)
    out_file = open(outputfile_name,'w')
    log.info('Converting mids to human readable name ...')
    for i, line in enumerate(open(inputfile_name, 'rb')):
        if i % 1000000 == 0:
            log.info('..%d..' % i)
        fields = line.strip().split('\t')
        if len(fields) != 4:
            log.warn('Unexpected format: %s' % line)
        s, p, o, t = fields
        sMid=mid(s)
	oMid=mid(o)
        if sMid in mid_set:
		if o.startswith('<http://rdf.freebase.com/ns/m.'):
			#oMid=mid(o)
                        if oMid in mid_set:
		            out_file.write(name_dict[sMid]+"\t"+p+"\t"+name_dict[oMid]+"\t"+t+"\n")
                        else:
                            out_file.write(name_dict[sMid]+"\t"+p+"\t"+o+"\t"+t+"\n")
		else:
			out_file.write(name_dict[sMid]+"\t"+p+"\t"+o+"\t"+t+"\n")
	elif oMid in mid_set:
		out_file.write(s+"\t"+p+"\t"+name_dict[oMid]+"\t"+"\n")
	else:
		out_file.write(line)

    log.info('all line is %i\n ..done.'%i)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='convert MIDs to type.object.name in FB')
    p.add_argument('mid2name', help='MIDs2names (type.object.name) file')
    p.add_argument('inputname', help='Input file name')
    p.add_argument('outputname', help='Output file name')   
    args = p.parse_args()
    log.info('reading arg')
    main(args.mid2name, args.inputname, args.outputname)
   
