from dittto.autoencoder import generate_autoencoder
import pandas as pd
from tensorflow import keras

def generate_synthetic_data(model_name: str, original_df, minority_class_column: str = 'class', 
                            minority_class_label: str = '0', decoder_activation: str = 'sigmoid', epochs: int = 100):

    if original_df.empty:
        raise ValueError("Empty dataframe.")
    
    if epochs < 1:
        raise ValueError("Invalid number of epochs.")
    
    original_df[minority_class_column] = original_df[minority_class_column].astype(str)  
    minority_df = original_df[original_df[minority_class_column] == minority_class_label]

    if minority_df.empty:
        raise ValueError("Minority class label not found in the dataset.")
    
    majority_df = original_df[original_df[minority_class_column] != minority_class_label]

    minority_df = minority_df.drop(columns=[minority_class_column])
    input_shape = minority_df.shape[1]

    if model_name == 'single_encoder':
        encoder_dense_layers = [20]
        bottle_neck = 16
        decoder_dense_layers = [18, 20]

    elif  model_name == 'balanced': 
        encoder_dense_layers = [22, 20]
        bottle_neck = 16
        decoder_dense_layers = [20, 22]

    elif model_name == 'heavy_decoder':
        encoder_dense_layers = [22,20]
        bottle_neck = 16
        decoder_dense_layers = [18, 20, 22, 24]

    else:
        raise ValueError("Invalid model name.") 
    
    try:
        autoencoder, encoder, decoder = generate_autoencoder(input_shape, encoder_dense_layers=encoder_dense_layers,
                                                            bottle_neck=bottle_neck, 
                                                            decoder_dense_layers=decoder_dense_layers,
                                                            decoder_activation=decoder_activation)
    except ValueError:
        raise ValueError("Invalid model parameters.")
    
    opt = keras.optimizers.Adam(learning_rate=0.001)
    autoencoder.compile(optimizer=opt, loss='mse')

    batch_size = 16
    validation_split = 0.25

    autoencoder.fit(minority_df, minority_df, epochs=epochs, batch_size=batch_size, validation_split=validation_split, verbose=0)
    synthetic_minority_df = autoencoder.predict(minority_df, verbose=0)
    reshaped_data = synthetic_minority_df.reshape(len(minority_df), -1)
    df_generated = pd.DataFrame(reshaped_data, columns = minority_df.columns)

    if minority_class_label.isnumeric():
        df_generated[minority_class_column] = int(minority_class_label)
    else:
        df_generated[minority_class_column] = minority_class_label

    synthetic_df = pd.concat([minority_df, df_generated, majority_df], ignore_index=True)
    synthetic_df = synthetic_df.sample(frac=1).reset_index(drop=True)

    return synthetic_df