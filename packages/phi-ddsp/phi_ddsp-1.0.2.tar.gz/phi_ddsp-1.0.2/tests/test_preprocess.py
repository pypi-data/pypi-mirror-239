from phi import preprocess 
import pkg_resources
import pytest
import numpy as np

@pytest.fixture
def test_preprocessing():
    # Get the test chirp 
    file = pkg_resources.resource_filename('phi', 'data/chirp.wav')

    # Define some parameters
    sampling_rate = 44100
    block_size = 60 
    signal_length = 240 

    # Store the preprocessed chrip
    preprocessed_features = preprocess(file, sampling_rate, block_size, signal_length)

    signal = preprocessed_features[0]
    feature_table = np.stack((preprocessed_features[1], preprocessed_features[2], preprocessed_features[3]), axis=0)

    return (signal, feature_table) 


# Compare the chirps signal shape with that of the original data table
def test_signal_shape(test_preprocessing):
    signal, _ = test_preprocessing
    expected_data = pkg_resources.resource_filename('phi', 'data/chirp_signal.npy')
    expected_value = np.load(expected_data)
    assert signal.shape == expected_value.shape 

# Compare the chirps feature shape with that of the original data table
def test_feature_shape(test_preprocessing):
    _, feature_table = test_preprocessing
    expected_data = pkg_resources.resource_filename('phi', 'data/chirp_features.npy')
    expected_value = np.load(expected_data)
    assert feature_table.shape == expected_value.shape 
