import boto3
import json
import os

os.environ['AWS_DEFAULT_REGION'] = "us-east-1"
class VideoDetect:
   JobId = ''
   rek = boto3.client('rekognition','us-east-1')

   bucket=''
   video=''
   startJobId = ''

   def __init__(self, bucket, video):
      self.bucket = bucket
      self.video = video

   # ============== Faces==============
   def StartFaceDetection(self):
        response=self.rek.start_face_detection(
           FaceAttributes = "ALL",
           Video = {
              'S3Object': {
                 'Bucket': self.bucket,
                  'Name': self.video
               }
            }
        )

        self.startJobId=response['JobId']
      #   print('Start Job Id: ' + self.startJobId)
      # TODO: store JobId should be better than storing the name of the video in case of interrupts during the analyzing

   def GetFaceDetectionResults(self):
         maxResults = 1000 # use the default value, also the maximum to generate the most labels
         paginationToken = ''
         finished = False

         while finished == False:
            while(True):
               response = self.rek.get_face_detection(JobId=self.startJobId,
                                            MaxResults=maxResults,
                                            NextToken=paginationToken)
               if(response['JobStatus'] != 'IN_PROGRESS'):
                  print('Response is done: ' + response['JobStatus'])
                  break

            # print('Codec: ' + response['VideoMetadata']['Codec'])
            # print('Duration: ' + str(response['VideoMetadata']['DurationMillis']))
            # print('Format: ' + response['VideoMetadata']['Format'])
            # print('Frame rate: ' + str(response['VideoMetadata']['FrameRate']))
            # print('\n\n information about faces is gonna print\n----\n')

        
            data = []
            for faceDetection in response['Faces']:
               data.append('Emotions: ' + str(faceDetection['Face']['Emotions']))
               data.append('Timestamp: ' + str(faceDetection['Timestamp']))
               # data.append('')
               #  print('Emotions: ' + str(faceDetection['Face']['Emotions']))
               #  print('Timestamp: ' + str(faceDetection['Timestamp']))
               #  print()

            if 'NextToken' in response:
                paginationToken = response['NextToken']
            else:
                finished = True
                return data

# def main():
   # bucket = 'storagepennapps19'
   # video = 'smile_video_2.mov'
   # video = 'smile_video.mp4'
   # video = 'emotion_1.mp4'

   # analyzer=VideoDetect(bucket,video)
   # analyzer.StartFaceDetection()
   # analyzer.GetFaceDetectionResults()

def lambda_handler(event, context):
   bucket = event['bucket']
   video = event['video']

   ret = []
   ret.append('video: ' + video)
   analyzer = VideoDetect(bucket, video)
   analyzer.StartFaceDetection()
   ret.append(analyzer.GetFaceDetectionResults())
   return ret





