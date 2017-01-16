#!/usr/bin/env python
import optparse, datetime, tarfile, os

def main():
    usage = "usage: %prog [options] source_dir destination_dir"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-n', '--number', dest="number", help="number of archives to keep during rotation; 0 - don't rotate archives", default=7)
    parser.add_option('-q', '--quiet', action="store_true", dest="quiet", help="don't produce any output", default=False)
    (options, args) = parser.parse_args()

    if not args:
        parser.print_usage()
        exit(1)

    if not options.quiet: print "Backup started " + datetime.datetime.now().strftime('%F at %T')
    filename = args[1] + "/" + datetime.datetime.now().strftime('%F_%H-%M-%S') + ".tar.gz"
    archive = tarfile.open(filename, "w:gz")
    archive.add(args[0])
    archive.close
    if not options.quiet: print "Backup completed " + datetime.datetime.now().strftime('%F at %T')

    if ( options.number > 0 ):
        files = os.listdir(args[1])
        files.sort(reverse=True)
        i = 1
        for file in files:
            if ( i > options.number ):
                os.remove(args[1] + "/" + file)
                if not options.quiet: print "Obsolete archive file " + file + " deleted"
            i += 1

if __name__ == "__main__":
    main()
