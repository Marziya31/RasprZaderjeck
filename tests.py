import pytest
import typer 

def test_upload_info():
    typer.upload_info(filename='test1.txt') 
    assert typer.typed_strings == 8
    typer.upload_info(filename='nosuchfile.txt') 
    assert typer.typed_strings == 0
    


def test_choose_string():
    assert typer.choose_string(filename='test1.txt') == ''
    assert typer.choose_string(filename='test1.txt', string_number=2) == 'a'
    assert typer.choose_string(filename='test1.txt', string_number=3) == 'b'
    assert typer.choose_string(filename='test1.txt', string_number=4) == 'c'
    assert typer.choose_string(filename='test1.txt', string_number=5) is None
    