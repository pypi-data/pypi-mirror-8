#!/usr/bin/env python3
"""
Generate random sequences in FASTA format
"""
import sys
from random import choice, randint

from sqt import HelpfulArgumentParser

__author__ = "Marcel Martin"


def main():
	parser = HelpfulArgumentParser(description=__doc__)
	parser.add_argument("--minimum-length", "-m", type=int, default=20)
	parser.add_argument("--maximum-length", "-M", type=int, default=50)
	parser.add_argument("n", type=int, help="Number of sequences to generate")

	args = parser.parse_args()
	ALPHABET = 'ACGT'
	for i in range(args.n):
		l = randint(args.minimum_length, args.maximum_length)
		seq = ''.join(choice('ACGT') for _ in range(l))
		print(">seq{0}\n{1}".format(i+1, seq))


if __name__ == '__main__':
	main()
