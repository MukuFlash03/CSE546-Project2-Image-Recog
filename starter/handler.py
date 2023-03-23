import face_recognition

input_bucket = "546proj2"
output_bucket = "546proj2output"

import pickle

import boto3
import os
# import face_recognition
import csv
from glob import glob

# Function to read the 'encoding' file
def open_encoding(filename):
	file = open(filename, "rb")
	data = pickle.load(file)
	file.close()
	return data

def face_recognition_handler(event, context):	
	# print("Hello")
	if event['Records'][0]['eventSource'] == 'aws:s3':
		region = 'us-east-1'

		dynamodb_student_table = 'student-data'
		dynamodb = boto3.resource('dynamodb', region_name=region)

		input_bucket = 'input-bucket-1523'
		output_bucket = 'output-bucket-results231'
		s3 = boto3.resource('s3', region_name=region)

		with open('tmp/encoding', 'rb') as f:
			known_encodings = pickle.load(f)

		known_face_names = known_encodings["name"]
		known_face_encodes = known_encodings["encoding"]

		# Creating dictionary with face names and encoding values as per data from encoding file and in order of entries in DynamoDB table
		known_face_dict = {key: value for key, value in zip(known_face_names, known_face_encodes)}
		custom_order = ['mr_bean', 'president_biden', 'vin_diesel', 'floki', 'president_trump', 'morgan_freeman',
						'president_obama', 'johnny_dep', 'denzel_washington', 'bush', 'travis_ragnar']
		sorted_dict = {key: value for key, value in
					   sorted(known_face_dict.items(), key=lambda item: custom_order.index(item[0]))}

		known_faces = []
		known_names = []

		for name, encoding in sorted_dict.items():
			if name in ['denzel_washington', 'bush', 'travis_ragnar']:
				continue
			else:
				known_names.append(name)
				known_faces.append(encoding)

		object_id = event['Records'][0]['s3']['object']['key']
		response = s3.get_object(Bucket=input_bucket, Key=object_id)
		data = response['Body'].read()
		with open(os.getcwd() + "\\" + object_id, 'wb') as f:
			f.write(data)
		response = s3.delete_object(Bucket=input_bucket, Key=object_id)
		print(response)
		# Fetch the current working directory to store the image frames from the input video
		image_frame_path = os.getcwd() + "/"

		# Use os.system() to call ffmpeg
		# -r specifies the frame rate (how many frames are extracted into images in one second, default: 25)
		# The last parameter (the output file) simply numbers your images with 3 digits (000, 001, etc.).
		os.system("ffmpeg -i " + str(object_id) + " -r 1 " + str(image_frame_path) + "image-%3d.jpeg")

		# Uploading and encoding only the first image frame from the input video
		unknown_image = face_recognition.load_image_file("image-001.jpeg")
		unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

		results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

		# Get a reference to the table
		table = dynamodb.Table(dynamodb_student_table)

		# Scan the table to read all items
		response = table.scan()

		# Create a new dictionary with Item ID as the key for easier access
		new_dict = {}
		# Create a new dictionary for storing the matched id/true values with their data
		true_dict = {}

		for d in response['Items']:
			id = d['id']
			del d['id']
			new_dict[id] = d

		# Checking for true values in results and creating a new dict with the data obtained from the DynamoDB response
		for i in range(len(results)):
			if results[i] == True:
				true_dict = new_dict[i + 1]

		print(true_dict)

		csv_data = [value for value in true_dict.values()]
		csv_data.reverse()
		# print(type(csv_data))
		print(csv_data)

		csv_file = "face_result.csv"

		with open(csv_file, "w", newline="") as f:
			writer = csv.writer(f)
			writer.writerow(csv_data)

		# Upload the CSV file to the S3 bucket
		# The upload_file method takes three parameters:
		# the name of the local file to upload, the name of the S3 bucket,
		# and the key (or path) of the file in the S3 bucket.

		# s3.upload_file(csv_file, output_bucket, input_video[:-4])
		s3.upload_file(csv_file, output_bucket, object_id[:-4])

		os.remove(object_id)

		for file in glob(image_frame_path + 'image-*.jpeg'):
			os.remove(file)
	else:
		print("Not an s3 event")