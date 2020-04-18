# Spot the mask
Zindi hackathon **Xth solution** disclosed

This is a binary classification problem with images as data input. CNNs are the state-of-the-art solution and most straight-forward option to achieve a high performing model. Here I show how to achive a perfect score:

![leaderboard](https://github.com/alfonmedela/spot_the_mask/blob/master/imgs/public_leaderboard.PNG)

## Algorithm 

### Classification CNN

I trained a DenseNet201 with fastai library with mixup and a final 2 epochs without mixup. I splitted the data into 90% train and 10% validation and achieved an logloss of 0.01019 on the public leaderboard. This without any further tricks. However, we can improve our models performance or at least its confidence by splitting the image into tiles and predicting all of them.

![submission](https://github.com/alfonmedela/spot_the_mask/blob/master/imgs/cnn_pred.PNG)

### Confident prediction

Here comes the most interesting part. I trained a Random Forest classifier to map the statistis on the soft predictions of the tiles to a confidence value of either 0 or 1. Technically this is not setting the values to 0 or 1 by hand as ZINDI organization made clear it wasn't allowed. Furthermore, it is not just a model that maps 0.9 into 1.0 but takes the general prediction, the mean, minimum and maximum prediction of the 5 tiles and predicts the confidence.

![tiles](https://github.com/alfonmedela/spot_the_mask/blob/master/imgs/tiles_diagram.png)

#### Training RF

I calculated the minimum, mean and maximum of the 5 predictions and used them as input to the RF together with the prediction for the whole image.

| x_1       |  x_2        | x_3    | x_4  | 
| ------------- | ------------- |------------- | ------------- |
| minimum pred   | mean pred        | maximum pred        | pred on the whole image        |

#### Predicting final test images

