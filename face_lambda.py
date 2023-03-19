import pickle


'''
//TODO: Mukul
    Reading result known images encoding data from provided encoding file
    Processed encoding data into a dictionary in the form of "face names" : "encoding values"
'''

# Load the encodings from the file
with open('starter/encoding', 'rb') as f:
    known_encodings = pickle.load(f)

known_face_names = known_encodings["name"]
known_face_encodes = known_encodings["encoding"]

known_face_dict = {key : value for key, value in zip(known_face_names, known_face_encodes)}

known_faces = []
known_names = []

for name, encoding in known_face_dict.items():
    if name in ["denzel_washington","bush","travis_ragnar"]:
        continue
    else:
        known_names.append(name)
        known_faces.append(encoding) 

print(known_names)


'''
//TODO: Mukul
    Fetching image frame from uploaded video using ffmpeg
'''

# unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]




'''
//TODO: Mukul
    Running face_recognition on the input image frame and comparing with encoding values of known faces
'''

# results = face_recognition.compare_faces(known_faces, unknown_face_encoding)




'''
//TODO: Amartya
    Fetching person's data from DynamoDB
'''

