import pickle
import boto3
import os

# Set the AWS access key and secret key
aws_access_key_id = 'AKIA4XD6E4L7SF4ANDQ2'
aws_secret_access_key = '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'
region = 'us-east-1'
table_name = 'student-data'

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
custom_order = ['mr_bean','president_biden','vin_diesel','floki','president_trump','morgan_freeman','president_obama','johnny_dep','denzel_washington','bush','travis_ragnar']
sorted_dict = {key: value for key, value in sorted(known_face_dict.items(), key=lambda item: custom_order.index(item[0]))}

known_faces = []
known_names = []

for name, encoding in sorted_dict.items():
    if name in ['denzel_washington','bush','travis_ragnar']:
        continue
    else:
        known_names.append(name)
        known_faces.append(encoding) 

print(sorted_dict)
print(known_names)

'''
//TODO: Mukul
    Fetching image frame from uploaded video using ffmpeg
'''

# Replace 'input_video.mp4' with the path to your video file
input_video = 'test_0.mp4'

# Replace 'output_dir' with the directory where you want to save the frames
current_file_path = os.path.abspath(__file__)
last_index = current_file_path.rfind("/")
frame_path = current_file_path[:last_index+1]

# Replace 'frame_rate' with the frame rate you want to extract
frame_rate = 1

# Use os.system() to call ffmpeg
# os.system(f'ffmpeg -i {input_video} -vf fps={frame_rate} {frame_path}/frame_%04d.jpg')
os.system("ffmpeg -i " + str(input_video) + " -r 1 " + str(frame_path) + "image-%3d.jpeg")

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
# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb', region_name=region,aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

# Get a reference to the table
table = dynamodb.Table(table_name)

# Scan the table to read all items
response = table.scan()

# Print all items in the table
for item in response['Items']:
    print(item)

# Create a new dictionary with Item ID as the key for easier access
new_dict = {}
# Create a new dictionary for storing the matched id/true values with their data
true_dict = {}

for d in response['Items']:
    id = d['id']
    del d['id']
    new_dict[id] = d
new_dict

Checking for true values in results and creating a new dict with the data obtain from the DynamoDB response
for i in range(len(results)):
    if results[i] == True:
        true_dict[i] = new_dict[i+1]



