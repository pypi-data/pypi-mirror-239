
def parseSourceObject(source_object):
    # source_object 값이 이미 리스트인 경우 그대로 반환
    if isinstance(source_object, list):
        return source_object
    # source_object 값을 공백 또는 쉼표로 분할하여 어레이로 변환
    parts = [x.strip() for x in source_object.replace('\n', ' ').split()]
    return parts

def parseSourceObjectTest() :
    # 테스트
    source_object = "aaa bbb"
    result = parseSourceObject(source_object)
    print(result)  # ["aaa", "bbb"]

