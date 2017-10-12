#-*- coding: utf-8 -*-
# You need to register your App first, and enter you API key/secret.
API_KEY = "EgyJfIlPo2PCIJc5Jmo2TqJeXuw7l7ho"
API_SECRET = "nAaJTapuIr4zvKKQWv3uGZnGXh-ZWP9H"
FACESET_ID = "wangbaoqiang"
target = 'wangbaoqiang'
threshold = 60
# The url of network picture, please fill in the contents before calling demo
face_one = '/Users/zhiminhe/wbq/out1.png'

# Local picture location, please fill in the contents before calling demo
face_two = '/Users/zhiminhe/wbq/out2.png'

# Local picture location, please fill in the contents before calling demo
face_search = '/Users/zhiminhe/wbq/out3.png'

#the server of international version
api_server_international = 'https://api-us.faceplusplus.com/facepp/v3/'

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


# First import the API class from the SDK
from facepp import API, File


#Create a API object, if you are an international user,code: api = API(API_KEY, API_SECRET, srv=api_server_international)
api = API(API_KEY, API_SECRET, srv=api_server_international)

api.faceset.delete(outer_id=FACESET_ID, check_empty=0)

#create a Faceset to save FaceToken
ret = api.faceset.create(outer_id=FACESET_ID)
print_result("faceset create", ret)

# detect image
Face = {}
res = api.detect(image_file=File(face_one))
print_result(target, res)
target_token = res["faces"][0]["face_token"]

"""res = api.detect(image_file=File(face_two))
print_result("person_two", res)
Face['person_two'] = res["faces"][0]["face_token"]
"""

# save FaceToken in Faceset
api.faceset.addface(outer_id=FACESET_ID, face_tokens=[target_token])


for i in range(1, 500):
    face_search = '/Users/zhiminhe/wbq/out'+ str(i) + '.png'
    print face_search,
    found = False
    # detect image and search same face
    ret = api.detect(image_file=File(face_search))
    # print_result("detect", ret)
    for face in ret["faces"]:
        search_result = api.search(face_token=face["face_token"], outer_id=FACESET_ID)

    # print result
    # print_result('search', search_result)
    # print '=' * 60
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

# delect faceset because it is no longer needed
#api.faceset.delete(outer_id=FACESET_ID, check_empty=0)
