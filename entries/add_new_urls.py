from form.myconstants import LIST_URLS_FILE
import sys


def add_new_sweepstakes(new_urls):
    url_file = open(LIST_URLS_FILE, "a")  # append mode
    for item in new_urls:
        url_file.write("%s\n" % item)
    url_file.close()


if __name__ == '__main__':
    add_new_sweepstakes(sys.argv[1:])
