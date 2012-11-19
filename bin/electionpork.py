from pelican.utils import slugify
import os.path
import os
import sys
import subprocess
import StringIO

def main():
    output_dir = '/Users/victor/poop'
    input_dir = sys.argv[-1]

    for dirname, _, filenames in os.walk(input_dir):
        for filename in filenames:
            root, ext = os.path.splitext(filename)

            if ext != '.docx':
                continue

            slug = slugify(os.path.basename(root).decode('utf-8'))

            try:
                f = open(os.path.join(dirname, filename))
                ret = subprocess.check_output('antiwordxp.rb', stdin=f)
            except subprocess.CalledProcessError, e:
                print
                print "{}".format(filename)
                print "{}".format(e)
                print "----"
            finally:
                f.close()

            ret = ret.decode('utf-8')

            if not "00Name and registration number" in ret:
                print filename
                continue

            if not "-342900Please, do not write anything in this area." in ret:
                print filename
                continue

if __name__ == '__main__':
    main()
