from tensorflow.keras.models import load_model

model = load_model(
    "models/cnn_sdp_model.h5",
    compile=False
)

EXPECTED_LENGTH = 5000