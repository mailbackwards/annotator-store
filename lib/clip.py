import os
import boto
from moviepy.editor import VideoFileClip


def make_clip(video_url, clip_id, start, end):
	# Hardcode to make it easy
	BUCKET_NAME = "video-quote"

	# First write clip to file
	clip_name = video_url.split('/')[-1]
	extension = clip_name.split('.')[-1]
	clip = VideoFileClip(video_url).subclip(start, end)
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