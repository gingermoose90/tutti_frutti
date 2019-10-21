import numpy
import skimage.io, skimage.color, skimage.feature

def sigmoid(inpt):
    return 1.0 / (1.0 + numpy.exp(-1 * inpt))


def relu(inpt):
    result = inpt
    result[inpt < 0] = 0
    return result


def predict_output(weights_mat_path, data_inputs, activation="relu"):
    weights_mat = numpy.load(weights_mat_path, allow_pickle=True)
    r1 = data_inputs
    for curr_weights in weights_mat:
        r1 = numpy.matmul(r1, curr_weights)
        if activation == "relu":
            r1 = relu(r1)
        elif activation == "sigmoid":
            r1 = sigmoid(r1)
    r1 = r1[0, :]
    predicted_label = numpy.where(r1 == numpy.max(r1))[0][0]
    class_labels = ["apple", "raspberry", "mango", "lemon"]
    predicted_class = class_labels[predicted_label]
    return predicted_class


def extract_features(img_path):
    image_data = skimage.io.imread(fname=img_path, as_gray=False)
    image_data_hsv = skimage.color.rgb2hsv(image_data)

    #indices = numpy.load(file="machinelearning/indices.npy")
    ## my own generated indices would not work, numpy error relating to matrix size
    indices = numpy.load(file="indices2.npy")

    hist = numpy.histogram(a=image_data_hsv[:, :, 0], bins=360)
    im_features = hist[0][indices]
    img_features = numpy.zeros(shape=(1, im_features.size))
    img_features[0, :] = im_features[:im_features.size]
    return img_features