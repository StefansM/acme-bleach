import pathlib
import runpy

import pytest

import acme.bleach.codec  # noqa


unencoded = """\
print("Hello ")
print("world.")
"""

encoded = (
    b"	   					   		 		  	 		 	  	   		   	 		\n"
    b"		 	 					 			 		 		 				  		 	 	  	  		\n"
    b"	  	  			  	    		 							 			 			 	 		 \n"
    b"				 	 		   					   		 		  	 		 	  	   	\n"
    b"	   	 				 	 					 			 		   	   	  	    \n"
    b"	   		 		  	  			  		 				 	   			 			 	\n"
    b"		 	 		 				 	 	\n"
)

# This gets encoded to a file with a "# coding=bleach" header and executed.
var_setting_example = """\
return_value = 1
"""


def test_round_trip() -> None:
    encoded = unencoded.encode("bleach")
    decoded = encoded.decode("bleach")
    assert decoded == unencoded


def test_encode() -> None:
    actual = unencoded.encode("bleach")
    assert encoded == actual


def test_decode() -> None:
    actual = encoded.decode("bleach")
    assert unencoded == actual


@pytest.fixture
def encoded_file(tmp_path: pathlib.Path) -> pathlib.Path:
    file_path = tmp_path / "bleached.py"
    with file_path.open("wb") as encoded_out:
        encoded_out.write(b"# coding=bleach\n")
        encoded_out.write(var_setting_example.encode("bleach"))

    return file_path


def test_execute(encoded_file: pathlib.Path) -> None:
    mod_globals = runpy.run_path(str(encoded_file.absolute()))
    assert mod_globals["return_value"] == 1
