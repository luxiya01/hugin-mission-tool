import unittest
import os
import mission_parser


class TestMission(unittest.TestCase):
    def test_mission_repr(self):
        test_mission_folder = './test_files/missions/'
        for filename in os.listdir(test_mission_folder):
            print(f'Test parsing file {filename}...')
            filepath = os.path.join(test_mission_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                orig_file_content = f.readlines()

            parsed_mission = mission_parser.MissionParser.parse_file(filepath)
            test_output_path = f'{test_mission_folder}/{filename}.test'
            with open(test_output_path, 'w', encoding='utf-8') as f:
                f.writelines(str(parsed_mission))

            with open(test_output_path, 'r', encoding='utf-8') as f:
                parsed_file_content = f.readlines()

            for (orig_line, parsed_line) in zip(orig_file_content,
                                                parsed_file_content):
                self.assertEqual(orig_line, parsed_line)


if __name__ == '__main__':
    unittest.main()
