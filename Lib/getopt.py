# module getopt -- Standard command line processing.

# Function getopt.getopt() has a different interface but provides the
# same functionality as the Unix getopt() function.

# It has two arguments: the first should be argv[1:] (it doesn't want
# the script name), the second the string of option letters as passed
# to Unix getopt() (i.e., a string of allowable option letters, with
# options requiring an argument followed by a colon).

# It raises the exception getopt.error with a string argument if it
# detects an error.

# It returns two items:
# (1)	a list of pairs (option, option_argument) giving the options in
#	the order in which they were specified.  (I'd use a dictionary
#	but applications may depend on option order or multiple
#	occurrences.)  Boolean options have '' as option_argument.
# (2)	the list of remaining arguments (may be empty).

# Added by Lars Wirzenius (liw@iki.fi): A third argument is optional.
# If present, getopt.getopt works similar to the GNU getopt_long
# function (but optional arguments are not supported).  The third
# argument should be a list of strings that name the long options.  If
# the name ends '=', the argument requires an argument.

# (While making this addition, I rewrote the whole thing.)

import string

error = 'getopt error'

def getopt(args, shortopts, longopts = []):
        list = []
        longopts = longopts[:]
        longopts.sort()
        while args and args[0][:1] == '-' and args[0] != '-':
                if args[0] == '-' or args[0] == '--':
                        args = args[1:]
                        break
                if args[0][:2] == '--':
                        list, args = do_longs(list, args[0][2:],
                                        longopts, args[1:])
                else:
                        list, args = do_shorts(list, args[0][1:],
                                        shortopts, args[1:])

        return list, args

def do_longs(list, opt, longopts, args):
        try:
                i = string.index(opt, '=')
                opt, optarg = opt[:i], opt[i+1:]
        except ValueError:
                optarg = ''

        has_arg, opt = long_has_args(opt, longopts)
        if has_arg:
                if not optarg:
                        if not args:
                                raise error, 'option --' + opt + \
                                        ' requires argument'
                        optarg, args = args[0], args[1:]
        else:
                if optarg:
                        raise error, 'argument --' + opt + \
                                ' must not have an argument'
        list.append('--' + opt, optarg)
        return list, args

# Return:
#   has_arg?
#   full option name
def long_has_args(opt, longopts):
        optlen = len(opt)
        for i in range(len(longopts)):
                x, y = longopts[i][:optlen], longopts[i][optlen:]
                if opt != x:
                        continue
                if y != '' and y != '=' and i+1 < len(longopts):
                        if opt == longopts[i+1][:optlen]:
                                raise error, 'option --' + opt + \
                                        ' not a unique prefix'
                if longopts[i][-1:] == '=':
                        return 1, longopts[i][:-1]
                return 0, longopts[i]
        raise error, 'option --' + opt + ' not recognized'

def do_shorts(list, optstring, shortopts, args):
        while optstring != '':
                opt, optstring = optstring[0], optstring[1:]
                if short_has_arg(opt, shortopts):
                        if optstring == '':
                                if not args:
                                        raise error, 'option -' + opt + \
                                                ' requires argument'
                                optstring, args = args[0], args[1:]
                        optarg, optstring = optstring, ''
                else:
                        optarg = ''
                list.append('-' + opt, optarg)
        return list, args

def short_has_arg(opt, shortopts):
        for i in range(len(shortopts)):
                if opt == shortopts[i] != ':':
                        return shortopts[i+1:i+2] == ':'
        raise error, 'option -' + opt + ' not recognized'

if __name__ == '__main__':
        import sys
        print getopt(sys.argv[1:], "a:b")
