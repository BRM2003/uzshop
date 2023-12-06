# requirement libraries
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
import face_recognition
import cv2
import base64
from PIL import Image
import io
import os


@api_view(['POST'])
@csrf_exempt
def main_script(request):
    try:
        path = '../media/sqb/'
        txt_file = path + 'codes/'
        result = {}
        if {'data', 'compare'} <= set(request.data):
            base64code = request.data['data']

            if 'file_name' in request.data:
                path += request.data['file_name'] + '_' + datetime.now().strftime('%Y%m%d_%H%M%S')
                txt_file += request.data['file_name'] + '_' + datetime.now().strftime('%Y%m%d_%H%M%S')
            else:
                path += 'user_' + datetime.now().strftime('%Y%m%d_%H%M%S')
                txt_file += 'user_' + datetime.now().strftime('%Y%m%d_%H%M%S')

            if base64code != '' and len(base64code) > 0:
                img = decode_base64_to_image(request.data['data'], path, txt_file)
                if request.data['compare']:
                    result = compare_faces([img, path + 'bekhzod.jpg'])
                    delete_jpg(path + 'jpg')
        else:
            result = {
                'success': False,
                'error': 'Bad requirement'
            }
    except Exception as e:
        result = {
            'success': False,
            'error': 'Something went wrong when getting images:' + str(e)
        }
    return Response(result)


def compare_process(file1, file2):
    try:
        # Load the images
        image1 = face_recognition.load_image_file(file1)
        image2 = face_recognition.load_image_file(file2)

        # Encode the faces found in the images
        face_encoding1 = face_recognition.face_encodings(image1)[0]
        face_encoding2 = face_recognition.face_encodings(image2)[0]

        # Compare the faces and return the face distance
        results = face_recognition.compare_faces([face_encoding1], face_encoding2)
        face_distances = face_recognition.face_distance([face_encoding1], face_encoding2)

        return results[0], face_distances[0]
    except Exception as e:
        return False, 'Somthing went wrong when comparing faces:' + str(e)


def compare_faces(files):
    try:
        match, similarity = compare_process(files[0], files[1])
        result = {
            'success': True,
            'face_match': match,
            'similarity_percentage': max(0, (1 - similarity) * 100)
        }
    except Exception as e:
        result = {
            'success': False,
            'error': 'Something went wrong with results:' + str(e)
        }
    return result


#                           DECODE OR ENCODE BASE64
def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string


def decode_base64_to_image(base64_string, output_path, txt_output_file):
    image_data = base64.b64decode(base64_string)
    with open(output_path + '.jpg', "wb") as file:
        file.write(image_data)
    with open(txt_output_file + '.txt', 'wb') as file:
        file.write(image_data)
    return output_path + 'jpg'


def delete_jpg(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        return "The file has been deleted successfully"
    else:
        return "The file does not exist"


