from harpoon.errors import BadOptionFormat

from option_merge import MergedOptions
import string

class NotSpecified(object):
    """Tell the difference between not specified and None"""

class MergedOptionStringFormatter(string.Formatter):
    """Resolve format options into a MergedOptions dictionary"""
    def __init__(self, all_options, option_path, chain=None, value=NotSpecified):
        if chain is None:
            if isinstance(option_path, list):
                chain = [thing for thing in option_path]
            else:
                chain = [option_path]
        self.chain = chain
        self.value = value
        self.option_path = option_path
        self.all_options = all_options
        super(MergedOptionStringFormatter, self).__init__()

    def format(self):
        """Format our option_path into all_options"""
        val = self.value
        if self.value is NotSpecified:
            val = self.get_string(self.option_path)
        if not isinstance(val, basestring):
            return val
        return super(MergedOptionStringFormatter, self).format(val)

    def get_string(self, key):
        """Get a string from all_options"""
        if key not in self.all_options:
            raise BadOptionFormat("Can't find key in options", key=key, chain=self.chain[:-1], source=self.all_options.source_for(self.chain[:-1]))

        val = self.all_options[key]
        if isinstance(val, dict) or isinstance(val, MergedOptions):
            raise BadOptionFormat("Shouldn't format in a dictionary", key=key, val=type(val), chain=self.chain)

        return val

    def _vformat(self, format_string, args, kwargs, used_args, recursion_depth):
        """I really want to know what the format_string is so I'm taking from standard library string and modifying slightly"""
        if recursion_depth < 0:
            raise ValueError('Max string recursion exceeded')

        result = []
        for literal_text, field_name, format_spec, conversion in self.parse(format_string):

            # output the literal text
            if literal_text:
                result.append(literal_text)

            # if there's a field, output it
            if field_name is not None:
                # this is some markup, find the object and do
                #  the formatting

                # given the field_name, find the object it references
                #  and the argument it came from
                # Slight modification here to pass in the format_spec
                obj, arg_used = self.get_field(field_name, args, kwargs, format_spec)
                used_args.add(arg_used)

                # do any conversion on the resulting object
                obj = self.convert_field(obj, conversion)

                # expand the format spec, if needed
                format_spec = self._vformat(format_spec, args, kwargs,
                                            used_args, recursion_depth-1)

                # format the object and append to the result
                result.append(self.format_field(obj, format_spec))

        return ''.join(result)

    def get_field(self, value, args, kwargs, format_spec=None):
        """Also take the spec into account"""
        if format_spec in ("env", ):
            return value, ()

        if self.option_path is None:
            this = self.all_options
        else:
            this = self.all_options.get(self.option_path)
        options = MergedOptions.using(self.all_options, {"this": this})

        if value in self.chain:
            raise BadOptionFormat("Recursive option", chain=self.chain + [value])

        return MergedOptionStringFormatter(options, value, chain=self.chain + [value]).format(), ()

    def format_field(self, obj, format_spec):
        """Know about any special formats"""
        if format_spec == "env":
            return "${{{0}}}".format(obj)
        else:
            return super(MergedOptionStringFormatter, self).format_field(obj, format_spec)

