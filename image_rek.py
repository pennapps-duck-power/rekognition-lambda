import boto3

S3 = boto3.resource('s3')
BUCKET = S3.Bucket('storagepennapps19')
KEY = "test_smile.jpg"
IMAGE_ID = KEY
S3_client = boto3.client("s3")

def get_emotions(bucket, key, ):
   rekognition_client = boto3.client("rekognition")
   response = rekognition_client.detect_faces(
      Image = {
         "S3Object": {
            "Bucket" : bucket,
            "Key" : key,
         }
      },
      
   )


for record in index_faces(BUCKET, KEY, COLLECTION, IMAGE_ID):
	face = record['Face']
	# details = record['FaceDetail']
   print "Face ({}%)".format(face['Confidence'])
	print "  FaceId: {}".format(face['FaceId'])
	print "  ImageId: {}".format(face['ImageId'])