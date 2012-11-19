import os
import os.path
import sys

def main():
    for dirpath, dirnames, filenames in os.walk(os.path.join(sys.argv[-1], 'candidates')):
        for filename in filenames:
            root, ext = os.path.splitext(filename)

            if ext != ".md":
                continue

            image_path = os.path.join(sys.argv[-1], 'images/candidates', "{}.jpg".format(root))

            if not os.path.exists(image_path):
                print image_path

if __name__ == '__main__':
    main()
