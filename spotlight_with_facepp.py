#-*- coding: utf-8 -*-
# You need to register your App first, and enter you API key/secret.
from moviepy.editor import VideoFileClip, concatenate_videoclips
# First import the API class from the SDK
from facepp import API, File

# Import system libraries and define helper functions
from pprint import pformat

def print_result(hit, result):
    def encode(obj):
        if type(obj) is unicode:
            return obj.encode('utf-8')
        if type(obj) is dict:
            return {encode(v): encode(k) for (v, k) in obj.iteritems()}
        if type(obj) is list:
            return [encode(i) for i in obj]
        return obj
    print hit
    result = encode(result)
    print '\n'.join("  " + i for i in pformat(result, width=75).split('\n'))


def split_and_join(file_path, split_list, output_file_path):
    # file_path = file path to the mp4 file you want to process. e.g. "sample.mp4" if in same folder, "/home/ashu_ix/Videos/sample.mp4" if in Videos filder, etc.
    # split_list = list/array of tuples with start and end time in seconds, in order you want to join. e.g., [(1, 10), (40,50), (150,200)]
    # outpu_file_path = file path to save the outpot mp4 file. e.g. "output.mp4" if in same folder, "/home/ashu_ix/Videos/output.mp4" if in Videos filder, etc.
    _clips = []
    _video = VideoFileClip(filename=file_path)
    for (start, end) in split_list:
        _clips.append(_video.subclip(t_start=start, t_end=end))

    _final_clip = concatenate_videoclips(_clips)
    _final_clip.write_videofile(output_file_path)
    _final_clip.write_videofile()

def save_frame(file_path, frame_second, out_file_path):
    # file_path = file path to the mp4 file you want to process. e.g. "sample.mp4" if in same folder, "/home/ashu_ix/Videos/sample.mp4" if in Videos filder, etc.
    # frame_second = the second for which you want to save the frame. e.g., 5
    # output_file_path = file path to save the output JPG/JPEG/PNG file. e.g. "output.png" if in same folder, "/home/ashu_ix/Pictures/output.png" if in Pictures folder, etc.
    _video = VideoFileClip(filename=file_path)
    _video.save_frame(out_file_path, t=frame_second)

if __name__ == '__main__':

    API_KEY = "EgyJfIlPo2PCIJc5Jmo2TqJeXuw7l7ho"
    API_SECRET = "nAaJTapuIr4zvKKQWv3uGZnGXh-ZWP9H"
    FACESET_ID = "wangbaoqiang"
    target = 'wangbaoqiang'
    threshold = 60
    # The url of network picture, please fill in the contents before calling demo
    target_face = '/Users/zhiminhe/wbq/out1.png'

    # the server of international version
    api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'

    # Create a API object, if you are an international user,code: api = API(API_KEY, API_SECRET, srv=api_server_international)
    api = API(API_KEY, API_SECRET, srv=api_server_international)

    api.faceset.delete(outer_id=FACESET_ID, check_empty=0)

    # create a Faceset to save FaceToken
    ret = api.faceset.create(outer_id=FACESET_ID)
    print_result("faceset create", ret)

    # detect image
    Face = {}
    res = api.detect(image_file=File(target_face))
    print_result(target, res)
    target_token = res["faces"][0]["face_token"]

    # save FaceToken in Faceset
    api.faceset.addface(outer_id=FACESET_ID, face_tokens=[target_token])

    t = 0
    last_found = False
    clips = []

    t = 0
    last_found = False
    clips = []
    video = VideoFileClip(filename= '/Users/zhiminhe/wbq.mp4')

    while t < 300:
        print 'processing frame', t,
        # extra one frame from the video
        video.save_frame('unknown.png', t=t )
        found = False
        # detect image and search same face
        ret = api.detect(image_file=File('unknown.png'))
        # print_result("detect", ret)
        for face in ret["faces"]:
            search_result = api.search(face_token=face["face_token"], outer_id=FACESET_ID)
            for result in search_result['results']:
                if target_token == result['face_token'] and  result['confidence'] > threshold:
                    found = True
                    break
            if found:
                break
        if found:
            print 'found'
        else:
            print 'not found'
        if found and (not last_found):
            # start a new clip
            start_time = t
        elif (not found) and last_found:
            # close a clip
            end_time = t
            clips.append((start_time, end_time))
            print clips
        last_found = found
        t = t +1


    print clips
    split_and_join("/Users/zhiminhe/wbq.mp4", clips, "/Users/zhiminhe/wbq_only.mp4")


# delect faceset because it is no longer needed
#api.faceset.delete(outer_id=FACESET_ID, check_empty=0)

# a sample run
