import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).with_name('engineering.py')
spec = importlib.util.spec_from_file_location('engineering', MODULE_PATH)
engineering = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engineering)


def test_val_accepts_positive_bounded_dimensions():
    assert engineering.val({'size': '150'}, 'size', 120) == 150
    assert engineering.val({'size': '999999'}, 'size', 120) == 120
    assert engineering.val({'size': '-1'}, 'size', 120) == 120


def test_keyword_parser_restricts_shape_vocabulary():
    parsed = engineering.keyword_parse('please make a gear 80')
    assert parsed == {
        'shape': 'gear',
        'size': 80,
        'message': 'Generating gear in keyword mode.',
    }
    assert engineering.keyword_parse('make something unknown') is None


def test_all_shape_generators_return_cad_code_and_label():
    for shape, generator in engineering.SHAPES.items():
        code, label = generator({'shape': shape, 'size': 120})
        assert isinstance(code, str) and code.strip()
        assert isinstance(label, str) and label.strip()
        assert 'result =' in code


def test_keyword_parser_handles_missing_dimension_with_default():
    parsed = engineering.keyword_parse('generate a plate')
    assert parsed['shape'] == 'plate'
    assert parsed['size'] == 120
