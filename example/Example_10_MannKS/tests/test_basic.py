import pytest
import sys
import os

# Add parent directory to path to allow importing modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from modules.data_generator import generate_synthetic_data

def test_generator():
    df = generate_synthetic_data(10, None, 'Days', 0.1, 0, 0, 0, 0, 0, 'None', 0, 42)
    assert len(df) == 10
    assert 'value' in df.columns
