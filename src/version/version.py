from ._version import *

class Version():
    """
    버전을 불러오고 관리하기 위한 클래스. 
    외부에서 호출할 땐 _version을 직접 부르지 않고 이것을 통과하도록 한다.
    """
    CURRENT = __version__
    
    def __init__(self):
        super().__init__()
    
    def parse(version_str):
        """앞 3자리 문자열을 tuple 형태로 리턴. 숫자로 비교 가능."""
        v_str = ".".join( version_str.split(".")[0:3] )
        print(v_str, "VSTR")
        return [int(x) for x in v_str.split(".")]

    def format(version_str):
        return "v" + version_str.lstrip('v')

    def current_formatted():
        """v로 시작하는 현재 버전 정보 str를 리턴."""
        return Version.format(Version.CURRENT)

    