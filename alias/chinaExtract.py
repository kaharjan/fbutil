#!/usr/bin/env python2.7
"""
Script to extract names and aliases from Freebase RDF dump.
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

def read_mids(f):
    log.info('Reading mids,names..')
    mids = frozenset([m.strip() for m in gzip.open(f, 'rb').readlines()])
    log.info('...len of mids (%d).' % len(mids))
    return mids


def mid(s):
    s = s.strip('<>')
    if s.startswith('http://rdf.freebase.com/ns/m.'):
        return s[27:]

def main(dumpf, midsf, chinaPathStr,china2PathStr):
    midDict={}
    midDict2={}
    mid_set = read_mids(midsf)
    chinaPath = open(chinaPathStr, 'w')
    chinaPathMid = open(china2PathStr,'w')
    log.info('Scanning dump for China..')
    for i, line in enumerate(gzip.open(dumpf, 'rb')):
        if i % 1000000 == 0:
            log.info('..%d..' % i)
        fields = line.strip().split('\t')
        if len(fields) != 4:
            log.warn('Unexpected format: %s' % line)
        s, p, o, t = fields
        sMid=mid(s)
        if sMid in mid_set:
            p1 = p.strip('<>')
            if not p1.endswith('type.object.name'):
                if not p1.endswith('common.topic.alias'):
		    if not p1.endswith('type.object.key'):
			if not p1.endswith('topic.description'):
		            if not p1.endswith('.topic_equivalent_webpage'):
				if not p1.endswith('rdf-schema#label'):
				    if "key/key.wikipedia" not in p1:
		                        if(midDict.has_key(sMid)):
    				            #midDict[sMid].append(sMid+"\t"+p1+"\t"+o+"\t"+t)
					    midDict[sMid].append(line)
					    o1=o.strip('<>')
					    if o1.startswith("http://rdf.freebase.com/ns/m."):
					       if(o1[27:] not in midDict2):
                                                   midDict2[o1[27:]]=0
                                               else:
						   midDict2[o1[27:]]+=1
                                        
						 
			                else:
			                    triplist=[]
			                    midDict[sMid]=triplist
    log.info("len of found 1path %d "%len(midDict))
    log.info("len of found 2path(e2) %d "%len(midDict2))
    for key,val in midDict.items():
	for tr in val:
            chinaPath.write(tr)
    for key,val in midDict2.items():
            chinaPathMid.write(key+"\n")

    log.info('all line is %i\n ..done.'%i)

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Extract relation associate with China from FB')
    p.add_argument('dump', help='Path to Freebase RDF dump file')
    p.add_argument('mids', help='List of MIDs and names (type.object.name contains China) to extract')
    p.add_argument('chinaPath1', help='Output file for chinaPath1')
    p.add_argument('chinaPath2', help='Output file for chinaPaht2')   
    args = p.parse_args()
    log.info('reading arg')
    main(args.dump, args.mids, args.chinaPath1,args.chinaPath2)
   



