import unittest
import io
import sys
from pystdf.IO import Parser, appendFieldParser
from pystdf.Types import RecordHeader, EofException, EndOfRecordException
from pystdf import V4

class TestIO(unittest.TestCase):
    def setUp(self):
        sys.stderr.write('Setting up test...\n')
        self.test_stream = io.BytesIO()
        self.parser = Parser(recTypes=V4.records, inp=self.test_stream, endian='<')
        self.parser.eof = 0  # Reset EOF flag
        sys.stderr.write('Setup complete.\n')

    def write_to_stream(self, data):
        """Helper method to write bytes to the test stream and reset position"""
        self.test_stream.write(data)
        self.test_stream.seek(0)

    def test_read_field_types(self):
        sys.stderr.write('Starting field types test...\n')
        # Set up header
        header = RecordHeader()

        # Test U1 (unsigned 1-byte integer)
        test_data = bytes([42])
        self.write_to_stream(test_data)
        header.len = 1
        value = self.parser.readField(header, "U1")
        sys.stderr.write(f'U1 value: {value}\n')
        self.assertEqual(value, 42)

    def test_read_header(self):
        header_data = bytes([
            0x0A, 0x00,  # Length (10)
            0x15,        # Type (21)
            0x20         # Sub-type (32)
        ])
        self.write_to_stream(header_data)
        header = self.parser.readHeader()
        self.assertEqual(header.len, 10)
        self.assertEqual(header.typ, 21)
        self.assertEqual(header.sub, 32)

    def test_read_field_types(self):
        print('Starting field types test...')
        # Set up header
        header = RecordHeader()

        # Test U1 (unsigned 1-byte integer)
        test_data = bytes([42])
        self.write_to_stream(test_data)
        header.len = 1
        value = self.parser.readField(header, "U1")
        self.assertEqual(value, 42)

        # Test U2 (unsigned 2-byte integer)
        self.test_stream.seek(0)
        self.test_stream.truncate()
        test_data = bytes([0x2A, 0x00])
        self.write_to_stream(test_data)
        header.len = 2
        value = self.parser.readField(header, "U2")
        self.assertEqual(value, 42)

        # Test I1 (signed 1-byte integer)
        self.test_stream.seek(0)
        self.test_stream.truncate()
        test_data = bytes([0xFF])  # -1 in two's complement
        self.write_to_stream(test_data)
        header.len = 1
        value = self.parser.readField(header, "I1")
        self.assertEqual(value, -1)

    def test_read_string(self):
        print('Starting string test...')
        # Set up header
        header = RecordHeader()
        header.len = 6  # 1 byte length + 5 bytes string

        # Test Cn (variable-length string)
        test_str = b"Hello"
        test_data = bytes([len(test_str)]) + test_str  # String length + string data
        self.write_to_stream(test_data)
        value = self.parser.readCn(header)
        self.assertEqual(value, "Hello")

        # Test empty string
        self.test_stream.seek(0)
        self.test_stream.truncate()
        test_data = bytes([0])  # Length 0
        self.write_to_stream(test_data)
        header.len = 1
        value = self.parser.readCn(header)
        self.assertEqual(value, "")

    def test_read_array(self):
        print('Starting array test...')
        # Test array of U1
        test_data = bytes([10, 20, 30])
        self.write_to_stream(test_data)
        header = RecordHeader()
        header.len = 3
        values = self.parser.readArray(header, 3, "U1")
        self.assertEqual(values, [10, 20, 30])

    def test_append_field_parser(self):
        print('Starting append field parser test...')
        def base_parser(*args):
            return [1, 2]
        
        def field_action(*args):
            return 3

        new_parser = appendFieldParser(base_parser, field_action)
        result = new_parser()
        self.assertEqual(result, [1, 2, 3])

    def test_end_of_record(self):
        print('Starting end of record test...')
        # Test handling of premature end of record
        test_data = bytes([0x02])  # Only 1 byte when 2 are expected
        self.write_to_stream(test_data)
        header = RecordHeader()
        header.len = 2
        with self.assertRaises(EndOfRecordException):
            self.parser.readField(header, "U2")

    def test_eof(self):
        print('Starting EOF test...')
        # Test handling of EOF
        self.write_to_stream(bytes([]))  # Empty stream
        header = RecordHeader()
        header.len = 1
        with self.assertRaises(EofException):
            self.parser.readField(header, "U1")

if __name__ == '__main__':
    unittest.main()
