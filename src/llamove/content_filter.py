import re

class ContentFilter:
    def __init__(self):
        pass

    def _is_short_line(self, line):
        return len(line.split()) < 10

    def _is_citation(self, line):
        # This regex matches lines that look like [n]
        return re.match(r'^\[\d+\]$', line.strip()) is not None

    def _is_table_or_figure(self, line):
        return re.match(r'^(Table|Figure)', line.strip()) is not None

    def _is_mostly_numerical(self, line):
        words = line.split()
        if len(words) == 0:
            return True
    
        numerical_count = sum([word.isnumeric() for word in words])
        return numerical_count >= len(words) / 2

    def _is_metadata(self, line):
        line_lower = line.lower()
        metadata_keywords = [
            "copyright", "page", "conference", "abstract", "contents", "index"
        ]
        return any(keyword in line_lower for keyword in metadata_keywords)
    
    def _is_filtered(self, line):
        # Returns if a line should be filtered out
        filters = [
            self._is_short_line,
            self._is_citation,
            self._is_table_or_figure,
            self._is_mostly_numerical,
            self._is_metadata
        ]
        return any(filter(line) for filter in filters)

    def filter(self, text):
        lines = text.split('\n')
        filtered_lines = []
        for line in lines:
            if not self._is_filtered(line):
                filtered_lines.append(line)
        return '\n'.join(filtered_lines)