from setuptools import setup, find_packages

setup(
    name = 'RouteAirPollEstimator',
    version = '0.0.2',
    description = "A library for estimating spatial-temporal air pollution exposure amounts by dividing routes.",
    url = 'https://github.com/MG-Choi/RouteAirPollEstimator',
    author = 'MoongiChoi',
    author_email = 'u1316663@utah.edu',
    packages = find_packages(),
    package_data = {'RouteAirPollEstimator': ['sampleData/AirPollutantSurface/*', 'sampleData/bicy_rental_loc/*', 'sampleData/bicy_route/*']},
    include_package_data = True,
    install_requires = ['numpy', 'pandas', 'geopandas >= 1.7', 'tqdm', 'shapely']
)




'''
note: How to make library
- 모두 seqC -> py로 저장.

- cmd (administrator) -> cd repository
- python setup.py sdist bdist_wheel
- twine upload dist/*
- 업데이트시에는 setup.py -> 0.02로 하고 다시 위 과정 반복


library test는 cmd에서 한다.

- pip uninstall 
- pip install sequentPSS


* 주의할 점:
random이나 os와 같이 깔려있는 library의 경우 위에 install_requires에 쓰지 않는다. py안에 바로 import로 쓰면 된다.

'''


#repository: C:\Users\MoongiChoi\Desktop\MG\양식, 코드 등\Python\Library\indoorCont

#참고:https://lsjsj92.tistory.com/592
#https://developer-theo.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-GitHub-Repository-%EC%83%9D%EC%84%B1%EB%B6%80%ED%84%B0-PyPI-Package-%EB%B0%B0%ED%8F%AC%EA%B9%8C%EC%A7%80

#위에서 버전 문제 발생: !pip install --upgrade requests
