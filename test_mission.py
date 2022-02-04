import unittest
import os
import mission_parser
import mission_utils


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
            os.remove(test_output_path)

    def test_add_water_sampling_commands(self):
        test_input = './test_files/missions/test_add_water_sampling_input.mp'
        test_output = './test_files/missions/test_add_water_sampling_output.mp'

        modified_mission, modified_mission_path = mission_utils.add_water_sampling_commands(
            filepath=test_input)

        with open(modified_mission_path, 'r', encoding='utf-8') as f:
            actual = f.readlines()
        with open(test_output, 'r', encoding='utf-8') as f:
            target = f.readlines()

        for (actual_line, target_line) in zip(actual, target):
            self.assertEqual(actual_line, target_line)
        os.remove(modified_mission_path)


if __name__ == '__main__':
    unittest.main()
