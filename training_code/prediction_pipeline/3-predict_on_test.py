################################## alfonsomedela.com #################################################

import matplotlib
matplotlib.use('Agg')
from fastai.vision import *
import pandas as pd
import glob
import pickle

torch.cuda.set_device(2)

#load densenet201
learner_path = 'PATH_TO_WEIGHTS'
learn = load_learner(learner_path)

# Load on top prediction model
filename = 'PATH/confidence_final.sav'
confidence_model = pickle.load(open(filename, 'rb'))

def get_predictions(image_path):

    '''
    :param image_path: input path of the image here
    :return: predictions for the 5 tiles
    '''

    main_image = PIL.Image.open(image_path).convert('RGB')
    main_image = np.array(main_image)

    nx = 2
    ny = 2
    img_size_y = main_image.shape[0] // ny
    img_size_x = main_image.shape[1] // nx
    predictions = []
    for i_y in range(ny):
        for i_x in range(nx):
            y1 = i_y * img_size_y
            y2 = (i_y + 1) * img_size_y
            x1 = i_x * img_size_x
            x2 = (i_x + 1) * img_size_x
            if i_y == ny - 1 and i_x == nx - 1:
                img = main_image[y1:, x1:, :]
            if i_y != ny - 1 and i_x == nx - 1:
                img = main_image[y1:y2, x1:, :]
            if i_y == ny - 1 and i_x != nx - 1:
                img = main_image[y1:, x1:x2, :]
            if i_y != ny - 1 and i_x != nx - 1:
                img = main_image[y1:y2, x1:x2, :]

            img = PIL.Image.fromarray(img).convert('RGB')
            img = pil2tensor(img, np.float32)
            img = img.div_(255)
            img = Image(img)

            pred_class, pred_idx, outputs = learn.predict(img)
            output_prediction = outputs.detach().numpy()
            predictions.append(output_prediction[0])

    # CENTRAL CROP
    y1, y2 = (main_image.shape[0] // 2) - (main_image.shape[0] // 4), (main_image.shape[0] // 2) + (main_image.shape[0] // 4)
    x1, x2 = (main_image.shape[1] // 2) - (main_image.shape[1] // 4), (main_image.shape[1] // 2) + (main_image.shape[1] // 4)
    img = main_image[y1:y2, x1:x2, :]
    img = PIL.Image.fromarray(img).convert('RGB')
    img = pil2tensor(img, np.float32)
    img = img.div_(255)
    img = Image(img)

    pred_class, pred_idx, outputs = learn.predict(img)
    output_prediction = outputs.detach().numpy()
    predictions.append(output_prediction[0])

    predictions = np.asarray(predictions)
    return predictions


if __name__ == '__main__':

    test_path = 'PATH/data_other/test/'

    path = 'PATH/data_other/'
    sub = pd.read_csv(path + 'sample_sub_v2.csv')


    for i in range(len(sub)):
        filename = sub['image'][i]
        filename = filename[5:-5].split('.')[0]
        image_path = glob.glob(test_path + '*' + filename + '*')[0]

        # predict 5 tiles
        predictions = get_predictions(image_path)

        # tile predictions stats
        min_pred = np.min(predictions)
        max_pred = np.max(predictions)
        mean_pred = np.mean(predictions)

        # predict whole image
        img = open_image(image_path)
        pred_class, pred_idx, outputs = learn.predict(img)
        output_prediction = outputs.detach().numpy()
        output_prediction = output_prediction[0]

        # prepare input to rf
        input_x = [[min_pred, mean_pred, max_pred, output_prediction]]
        res = confidence_model.predict(input_x)[0]

        sub['target'][i] = str(res)

    sub.to_csv('confident_submission.csv', index=False)





