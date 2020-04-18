import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import shuffle
import pickle

if __name__ == '__main__':

    # Load training data
    df = np.load('training_data.npy')

    for i in range(len(df)):
        if df[i,-1] == 0:
            df[i, -1] = 1
        else:
            df[i, -1] = 0

    # Add low confidence samples with corrective values
    df_new = []
    for i in range(200):
        if i < 100:
            rand_pred = np.random.randint(500,1000)/1000.
            rand_min = np.random.randint(0, 100) / 1000.
            rand_mean = np.random.randint(100, 500) / 1000.
            rand_max = np.random.randint(500, 1000) / 1000.
            df_new.append([rand_min, rand_mean, rand_max, rand_pred, 1])

        else:
            rand_pred = np.random.randint(200, 500) / 1000.
            rand_min = np.random.randint(200, 700) / 1000.
            rand_mean = np.random.randint(400, 900) / 1000.
            rand_max = np.random.randint(980, 1000) / 1000.
            df_new.append([rand_min, rand_mean, rand_max, rand_pred, 1])

    for i in range(200):
        if i < 100:
            rand_pred = np.random.randint(0,500)/1000.
            rand_min = np.random.randint(0,100)/1000.
            rand_mean = np.random.randint(0,500)/1000.
            rand_max = np.random.randint(0,800)/1000.
            df_new.append([rand_min, rand_mean, rand_max, rand_pred, 0])

        else:
            rand_pred = np.random.randint(500, 800) / 1000.
            rand_min = np.random.randint(0, 100) / 1000.
            rand_mean = np.random.randint(0, 500) / 1000.
            rand_max = np.random.randint(0, 500) / 1000.
            df_new.append([rand_min, rand_mean, rand_max, rand_pred, 0])


    df_new = np.asarray(df_new)

    df = np.concatenate((df, df_new), axis=0)
    df = shuffle(df)

    x_train, x_test, y_train, y_test = train_test_split(df[:,:-1], df[:,-1], stratify=df[:,-1], test_size=0.2)
    x_train, y_train = shuffle(x_train, y_train)

    svm = RandomForestClassifier()
    svm.fit(x_train, y_train)

    score = svm.score(x_test, y_test)
    print(score)

    filename = 'confidence_final.sav'
    pickle.dump(svm, open(filename, 'wb'))




