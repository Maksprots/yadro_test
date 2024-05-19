from dataclasses import dataclass


@dataclass
class Constants:
    root_path_expression = "*[@isRoot='true']"
    path_out_config = 'out/config.xml'
    path_out_meta = 'out/meta.json'
    path_read_input = 'input/impulse_test_input.xml'
    congrads = 'Succsessful'
