from enum import Enum


class FilterType(Enum):
    date_range_filter = 'dateRangeFilter'
    metadata_filter = 'metadataFilter'
    prefix_filter = 'prefixFilter'
    query_filter = 'queryFilter'


class Filter(object):
    """Use a Filter to restrict answers using metadata"""

    def __init__(self, filter_type, field_name, values=()):
        self.filter_type = filter_type
        self.field_name = field_name
        self.values = values

    def __eq__(self, other):
        """Return True iff self is equivalent to other

        :param other: A Filter
        :return: True or False
        """
        if self is other:
            return True

        if not isinstance(other, Filter):
            return False
        if self.filter_type != other.filter_type:
            return False
        if self.field_name != other.field_name:
            return False
        if self.values != other.values:
            return False

        return True
