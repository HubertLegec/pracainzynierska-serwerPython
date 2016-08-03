import argparse


def parse_parameters():
    parser = argparse.ArgumentParser(description='Visual search engine', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c', '--config', type=str, metavar='PATH', required=True, help='Path to configuration file')
    parser.add_argument('-v', '--vocabulary', type=str, metavar='PATH', required=True,
                        help='Path to file with vocabulary')
    parser.add_argument('-d', '--debug', action='store_true', help='run in debug mode')
    parser.add_argument('-p', '--port', type=int, help='port number to run server on')
    parser.add_argument('-h', '--host', type=str, help='address to run server on')
    return parser.parse_args()


if __name__ == '__main__':
    params = parse_parameters()
    # TODO

