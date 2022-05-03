from modules import *

__parser = argparse.ArgumentParser()
__parser.add_argument(
    'config',
    type=str,
    help='Configuration file, either subscription url or file path is ok.',
)
__parser.add_argument(
    'template', type=str, help='Template file, same requirement as configuration.'
)
__parser.add_argument(
    '-o', '--output', type=str, help='Output file path.', default='config.yml'
)
args = __parser.parse_args()


def main():
    r = Retune(args.config, args.template, args.output)
    r.dump_withOriginName()
