import tensorflow as tf
from tensorflow.keras.layers import Conv1D, LSTM, Dense, Dropout, Bidirectional, TimeDistributed, GRU
from tensorflow.keras.layers import MaxPooling1D, Flatten
from tensorflow.keras.regularizers import L1, L2

#CNN-LSTM model
def cnn_lstm(ws=20, multi=3):

    model = tf.keras.Sequential()

    # Creating the Neural Network model
    # CNN layers
    model.add(TimeDistributed(Conv1D(256, kernel_size=5, padding='same', activation='selu', input_shape=(None, ws, 1))))
    model.add(TimeDistributed(MaxPooling1D(2)))
    model.add(TimeDistributed(Flatten()))
#    model.add(Dense(5, kernel_regularizer=L1(0.01)))

    # LSTM layers
    model.add(Bidirectional(LSTM(multi*ws, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(multi*ws, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(multi*ws, return_sequences=True)))
    model.add(Dropout(0.3))
    model.add(Bidirectional(LSTM(multi*ws, return_sequences=False)))
    model.add(Dropout(0.3))

    #Final layers
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='Adamax', loss='mae', metrics=['mse', 'mae', 'mape'])

    return model
