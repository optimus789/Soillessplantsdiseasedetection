from django.shortcuts import render
#import tensorflow as tf
import numpy as np
import os
import json
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
#from tensorflow.keras.preprocessing import image

#testingdirect = "F://xampp//htdocs//upload"

testingdirect = "media"


#model = tf.keras.models.load_model('tomatoaugwithcnn2.h5',compile=False)
#model2 = tf.keras.models.load_model('tomatoaugwithoutcnn2.h5',compile=False)

# Create your views here.
name = ['Bacterial Spot', 'Early Blight', 'Healthy', 'Late Blight', 'Leaf Mold', 'Septoria Leaf Spot', 'Spider Mites Two-Spotted Spider Mite', 'Target Spot', 'Tomato Mosaic Virus', 'Tomato Yellow Leaf Curl Virus']


def titlename(arr):  
    loc = np.where(arr[i] == np.amax(arr[i]))
    x = np.array(loc, dtype=np.int64)
    y = x[0][0]
    return name[y]


def predict(request):
    '''os.remove('media/upload/uploads.jpg')
    #save_path = os.path.join(settings.MEDIA_ROOT, 'uploads',request.FILES['file'])

    path = default_storage.save("upload/uploads.jpg", request.FILES['file'])
    os.remove('media/data_file.json')

    testing_generator = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1. / 255).flow_from_directory(testingdirect,
                                              target_size=(299, 299),
                                              batch_size=1)
    imgs, labels = next(testing_generator)

    pred = new_model.predict(imgs)

    name1 = []
    value = []
    arr2 = []
    serv = []

    final = pred[0]

    for j in range(3):
        for i in range(101):
            if (float(final[i]) == np.amax(final)):
                name1.append(name[i])
                value.append(final[i] * 100)
                final[i] = 0
                break

    nutrvalall = []

    for i in range(3):

        a = fs.foods_search(name1[i].replace("_", " "))
        try:
            arr2 = a[0]['food_description'].split('-')
            serv.append(arr2[0])
            nutrvalall.append(arr2[1].split('|'))

        except:
            arr2 = a['food_description'].split('-')
            serv.append(arr2[0])
            nutrvalall.append(arr2[1].split('|'))

    nutr = []
    d = []

    for j in range(3):
        for i in range(4):
            arr2 = str(nutrvalall[j][i].split(':')[1])

            d.append(arr2)
        nutr.append(d)
        d = []
    """var text = '{"employees":[' +
    '{"firstName":"John","lastName":"Doe" },' +
    '{"firstName":"Anna","lastName":"Smith" },' +
    '{"firstName":"Peter","lastName":"Jones" }]}';
    """

    response = {
        'prediction': [
            {
                "Name": name1[0],
                "Value": value[0],
                "Serving": serv[0],
                "Calories": nutr[0][0],
                "Fat": nutr[0][1],
                "Carbs": nutr[0][2],
                "Protein": nutr[0][3]
            },
            {
                "Name": name1[1],
                "Value": value[1],
                "Serving": serv[1],
                "Calories": nutr[1][0],
                "Fat": nutr[1][1],
                "Carbs": nutr[1][2],
                "Protein": nutr[1][3]
            },
            {
                "Name": name1[2],
                "Value": value[2],
                "Serving": serv[2],
                
                "Calories": nutr[2][0],aq
                "Fat": nutr[2][1],
                "Carbs": nutr[2][2],
                "Protein": nutr[2][3]
            },
        ]
    }
    cont = str(response)

    save_path = os.path.join(settings.STATIC_ROOT, 'static')

    with open("media/data_file.json", "w+") as write_file:
        json.dump(response, write_file)

    a = "'" + cont.replace("'", '"') + "'"

    context = {'resultjson': a}'''
    return render(request, 'tomatopred/predict.html')

def filename(path):
    count = 0
    a = os.listdir(os.path.join(path,'oldfiles'))
    for i in a:
        count+=1

    upload_name = str('upload')+str(count)+str('.jpg')


def imgin(request):
    contex={}
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    media_dir = os.path.join(BASE_DIR, 'media')
    upload_name=filename(media_dir)
    print("no if")
    if(os.listdir(os.path.join(media_dir,'upload'))!=None):
        os.rename(os.path.join(media_dir,'upload','uploads.jpg'),os.path.join(media_dir,'oldfiles',upload_name))
        
    if request.method=='POST':
        print("in if")
        try:
            path = default_storage.save("upload/uploads.jpg", request.FILES['file'])
            name2 = "Correct file uploaded"
            context = {'result': name2}
        except MultiValueDictKeyError:
            name2 = "Wrong File OR No File uploaded"
            context = {'result': name2}
    else:
        context = {'result': None}
    return render(request, 'tomatopred/predict.html',context)
