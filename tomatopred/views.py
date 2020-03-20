from django.shortcuts import render
import tensorflow as tf
import numpy as np
import os
import json
from django.core.files.storage import default_storage
from django.utils.datastructures import MultiValueDictKeyError
from django.conf import settings
from tensorflow.keras.preprocessing import image

#testingdirect = "F://xampp//htdocs//upload"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

testingdirect = os.path.join(BASE_DIR,'media')


model = tf.keras.models.load_model(os.path.join(BASE_DIR,'trainedmodels','tomatoaugwithcnn2.h5'),compile=False)
model2 = tf.keras.models.load_model(os.path.join(BASE_DIR,'trainedmodels','tomatoaugwithoutcnn2.h5'),compile=False)

# Create your views here.
name = ['Bacterial Spot', 'Early Blight', 'Healthy', 'Late Blight', 'Leaf Mold', 'Septoria Leaf Spot', 'Spider Mites Two-Spotted Spider Mite', 'Target Spot', 'Mosaic Virus', 'Yellow Leaf Curl Virus']


def titlename(arr):  
    loc = np.where(arr == np.amax(arr))
    x = np.array(loc, dtype=np.int64)
    y = x[0][0]
    return name[y]

def floatconv(arr):
    arr2=[]
    for i in range(10):
        arr2.append(arr[0][i])
    return arr2

# this function does the work of above function but it will give an average of prediction of  both the models and then the resulted model will be given as a result 
def finpred(imgs,model,new_model):
    
    pred1 = model.predict(imgs)
    
    pred2 = new_model.predict(imgs)
    
    final_pred = pred2
    
    for j in range(10):            
        final_pred[0][j] = max(float(pred1[0][j]),float(pred2[0][j]))
    
    final_pred=floatconv(final_pred)
    print(final_pred)

    return final_pred

def filename(path):
    count = 0
    a = os.listdir(os.path.join(path,'oldfiles'))
    for i in a:
        count+=1

    upload_name = str('uploads')+str(count)+str('.jpg')
    return upload_name


def imgin(request):
    contex={}
    print(BASE_DIR)
    media_dir = os.path.join(BASE_DIR, 'media')
    print(media_dir)
    upload_name=filename(media_dir)
    print("no if")
        
    if request.method=='POST':
        print("in if")
        try:
            
            if(os.path.exists(os.path.join(media_dir,'upload',"uploads.jpg"))):
                os.rename(os.path.join(media_dir,'upload','uploads.jpg'),os.path.join(media_dir,'oldfiles',upload_name))

            path = default_storage.save("upload/uploads.jpg", request.FILES['file'])
            print("Testing Directory: ",testingdirect)
            testing_generator = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255).flow_from_directory(testingdirect,target_size=(256, 256),batch_size=1,classes=['upload'])
            imgs, labels = next(testing_generator)
            name2 = titlename(finpred(imgs,model,model2))
            context = {'result': name2,'flag':True}
            return render(request, 'tomatopred/predict.html',context)
        except MultiValueDictKeyError:
            name2 = "Wrong File OR No File uploaded"
            context = {'result': name2,'flag':False}
            return render(request, 'tomatopred/predict.html',context)

    else:
        context = {'result': None, 'flag':False}
        return render(request, 'tomatopred/predict.html',context)
    
