'''
Mateusz Miekicki s20691
Oskar Przydatek s19388
Determining if someone has diabetes based on data from previous classes. 
'''
from tensorflow import keras
import pandas as pd
from sklearn.model_selection import train_test_split

def read_data(col_names, feature_cols, target, csv_file):
    '''
    The function loads a data set from a file and divides it into
    test data and learning data
    Parameters:
    col_names: csv file header
    feature_cols: features
    target: target to learn
    csv_file: path to csv file
    Returns: List containing train-test split of inputs.
    '''
    pima = pd.read_csv(csv_file, header=None, names=col_names)
    X = pima[feature_cols]
    y = pima[target]
    return train_test_split(X, y, test_size=0.3)


col_names = ['pregnant', 'glucose', 'bp', 'skin',
             'insulin', 'bmi', 'pedigree', 'age', 'label']
feature_cols = ['pregnant', 'glucose', 'bp',
                'skin', 'insulin', 'bmi', 'pedigree', 'age']
X_train, X_test, y_train, y_test = read_data(
    col_names, feature_cols, "label", "pima-indians-diabetes.csv")
'''
Define Sequential model with 1 layer
'''
model = keras.Sequential([
    keras.layers.Dense(8, activation='relu'),
])

'''
Configures the model for training
'''
model.compile(optimizer='adam',
              loss='mse',
              metrics=['accuracy'])

'''
Trains the model for a fixed number of epochs
'''
history = model.fit(X_train, y_train, epochs=500)

test_loss, test_acc = model.evaluate(X_test,  y_test)

print('\nTest loss:', test_loss)
print('\nTest accuracy:', test_acc)