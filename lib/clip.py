import os
import boto
from moviepy.editor import VideoFileClip, TextClip
#from moviepy.config import change_settings

#change_settings({"IMAGEMAGICK_BINARY": r"path/to/your/imageMagick/convert.exe"})

def make_clip(video_url, clip_id, start, end, text="", attribution="", date=None):
	# Hardcode to make it easy
	BUCKET_NAME = "video-quote"

	# First write clip to file
	clip_name = video_url.split('/')[-1]
	filename = clip_name.split('.')[0]
	extension = clip_name.split('.')[-1]
	clip = VideoFileClip(video_url).subclip(start, end)
	# if text:
	# 	txt_clip = TextClip(text, fontsize=12, color='white')
	# 	txt_clip.set_position('bottom').set_duration(end-start)
	# 	clip = CompositeVideoClip([clip, txt_clip])
	clip.write_videofile(clip_name)
	# Put it on S3
	conn = boto.connect_s3()
	bucket = conn.get_bucket(BUCKET_NAME)
	key_name = clip_id + "." + extension
	key = bucket.new_key(key_name)
	key.set_contents_from_filename(clip_name, policy='public-read')
	# Delete clip
	os.remove(clip_name)
	# Get url
	clip_url = 'http://{bucket}.{host}/{key}'.format(
		bucket=BUCKET_NAME,
	    host=conn.server_name(),
	    key=key_name)
	return clip_url