from exceptions.generator import NotSupportedError
from config_generator import generator as g
from const.consts import Constants as cs

if __name__ == '__main__':
    gen = g.Generator(cs.path_read_input)
    gen.parse_file()
    try:
        gen.generate_xml(path=cs.path_out_config)
        gen.generate_json(path=cs.path_out_meta)
    except Exception as e:
        raise NotSupportedError
    print(cs.congrads)
    print(cs.path_out_meta)
    print(cs.path_out_config)