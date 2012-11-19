from pelican.utils import slugify
import codecs
import os
import os.path
import sys

TEMPLATE = u"""Title: {name}
Registration: {registration_number}

"""

def main():
    if not len(sys.argv) == 2:
        print "Provide position name, please."
        return

    position = sys.argv[-1]
    base_path = os.path.join('content/candidates', position)

    if not os.path.exists(base_path):
        print "Creating directory for {}".format(position)
        os.makedirs(base_path)

    print "Creating files for {} candidates".format(position)
    print "Enter candidates, press enter and Ctrl+D:"
    candidates = sys.stdin.readlines()

    print ""

    for candidate in candidates:
        candidate = candidate.decode('utf-8')

        parts = candidate.split()

        if not len(parts) > 1:
            continue

        registration_number = parts.pop()
        name = " ".join(parts)

        slug = slugify(name)

        filename = os.path.join(base_path, "{}.md".format(slug))
        content = TEMPLATE.format(name=name, registration_number=registration_number)

        print "{}...".format(slug)

        f = codecs.open(filename, 'w', encoding='utf-8')
        f.write(content)
        f.close()

if __name__ == '__main__':
    main()
