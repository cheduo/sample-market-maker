# creating a parser
import argparse
parser = argparse.ArgumentParser(description='Process some intergers.')
Adding arguments
parser.add_argument('integers',
                    metavar='N',
                    type=int,
                    nargs='+',
                    help='an integer for the accumulator')
parser.add_argument('--sum',
                    dest='accumulate',
                    action='store_const',
                    const=sum,
                    default=max,
                    help='sum the interger(default: find the max)')
# call parse_args() will return an object with two attributes
# integers and accumulate
# integers attribute will be a list of one or more ints
# accumulate attribute  will be either the sum() function if --sum was specified at the command line
# or the max function if it was not
parser.parse_args(['--sum','7','-1','42'])
# Namespace(accumulate=<built-in function sum>, integer=[7,-1,42])
# parse_args() inspects the command line,
# convert each argument to the appropriate action.
# In most cases, this means a simple Namespace object will be built up from attributes parsed out of command line

# the add_argument method must know whether an optional argument like -f or --foo
# or a positional argument, like a list of filenames is expected
# the first argument passed to add_argument() must be
# - either a series of flags
# - a simple argument name

# action
'store
'store const
