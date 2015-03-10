from datetime import timedelta
import decimal
import json
import requests
 
#To grab video stats off a youtube video using JSON
 
def fetch_video_info(video_id):
    r = requests.get('https://gdata.youtube.com/feeds/api/videos/{id}?v=2&alt=json'.format(id=video_id))
    return json.loads(r.text)
 
_title = lambda video_info: video_info['entry']['title']['$t']
_length = lambda video_info: int(video_info['entry']['media$group']['yt$duration']['seconds'])
_view_count = lambda video_info: int(video_info['entry']['yt$statistics']['viewCount'])
_upvote_count = lambda video_info: int(video_info['entry']['yt$rating']['numLikes'])
_downvote_count = lambda video_info: int(video_info['entry']['yt$rating']['numDislikes'])
_human_readable_duration = lambda seconds: str(timedelta(seconds=seconds))
 
def stats_string(video_id):   #something useless
    video_info = fetch_video_info(video_id)
    return "[YouTube: {title} | Duration: {duration} | Views: {view_count} | Votes: {upvote_count} up - {downvote_count} down]".format(
        title=_title(video_info),
        duration=_human_readable_duration(_length(video_info)),
        view_count=_view_count(video_info),
        upvote_count=_upvote_count(video_info),
        downvote_count=_downvote_count(video_info)
        )
