import pickle
import boto3
import os
import face_recognition

# Set the AWS access key and secret key
aws_access_key_id = 'AKIA4XD6E4L7SF4ANDQ2'
aws_secret_access_key = '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'
region = 'us-east-1'
table_name = 'student-data'


input_bucket = 'input-bucket-1523'
output_bucket_name = 'output-bucket-results231'
s3 = boto3.client('s3', region_name='us-east-1')


'''
//DONE: Mukul
    Reading result known images encoding data from provided encoding file
    Processed encoding data into a dictionary in the form of "face names" : "encoding values"
'''

# Load the encodings from the file
with open('starter/encoding', 'rb') as f:
    known_encodings = pickle.load(f)

known_face_names = known_encodings["name"]
known_face_encodes = known_encodings["encoding"]

# Creating dictionary with face names and encoding values as per data from encoding file and in order of entries in DynamoDB table
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




'''
//TODO: Mukul
    Obtaining input video from input S3 bucket
'''

# Using local videos for testing
input_video = 'test_2.mp4'




'''
//TODO: Mukul
    Fetching image frame from uploaded video using ffmpeg and encoding the image data
'''

# Fetch the current working directory to store the image frames from the input video
image_frame_path = os.getcwd() + "/"

# Use os.system() to call ffmpeg
# -r specifies the frame rate (how many frames are extracted into images in one second, default: 25)
# The last parameter (the output file) simply numbers your images with 3 digits (000, 001, etc.). 
os.system("ffmpeg -i " + str(input_video) + " -r 1 " + str(image_frame_path) + "image-%3d.jpeg")


# Uploading and encoding only the first image frame from the input video
unknown_image = face_recognition.load_image_file("image-001.jpeg")
unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]




'''
//DONE: Mukul
    Running face_recognition on the input image frame and comparing with encoding values of known faces
'''

results = face_recognition.compare_faces(known_faces, unknown_face_encoding)




'''
//DONE: Amartya
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

# Checking for true values in results and creating a new dict with the data obtain from the DynamoDB response
for i in range(len(results)):
    if results[i] == True:
        true_dict[i] = new_dict[i+1]

print(true_dict)
print()
