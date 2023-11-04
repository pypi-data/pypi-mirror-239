def aa():
    """
    체크사항 : 
    1. 캡처도구 잘 되는지 확인
    •	winow 시작 창에 캡처 도구 치시면 됩니다.
    2. 워드 or 한글 pdf 변환 잘 되는지 확인
    •	[File] [Download as] [HTML(.html)] 을 이용하여 HTML 저장 후 HTML 저장된 파일을 열어서 [Microsoft Print to PDF] 선택 [ ] .pdf(000000000.pdf) 후 인쇄 수험번호 로 저장
    •	워드 or 한글 파일에 코드 및 이미지, 결과를 캡처도구로 붙여넣고, pdf로 변환

    한글데이터 
    dat = pd.read_csv(‘00.csv’, encoding = ‘CP949’), or utf-8 
    폰트 
    폰트 위치 : /usr/share/fonts/nanum/ 폰트 종류 , : NanumMyeongjo.ttf, NanumGothic.ttf
    from matplotlib import font_manager, rc 
    rc('font', family='NanumGothic') 
    plt.rcParams['axes.unicode_minus'] = False
    from sklearn import set_config
    set_config(display="diagram")
    필수 코드

    pip install yellowbrick --no-deps
    import warnings
    warnings.filterwarnings('ignore')

    %config Completer.use_jedi = False
    %matplotlib inline
    #plt.tight_layout()
    import pandas as pd 
    import numpy as np 
    import janitor
    import matplotlib.pyplot as plt
    import seaborn as sns
    import time


    EDA 순서
    1.	데이터 불러오기 
    dat = pd.read_csv(‘00.csv’, encoding = ‘CP949’), or utf-8 

    2.	변수명 정리
    (dat 
        .rename(columns = {'school' : '학교'})
        .columns
    )

    3.	변수 속성 확인
    dat.info()

    4.	변수 속성 변환
    (dat
        .astype({'famrel' : 'int32', 'dalc' : 'float64'})
        .info()
    )
    5.	데이터 재구조화

    pd.melt() : wide form에서 long form으로 바꾸는 함수
    •	id_vars : 기준 칼럼
    •	value_vars : long form으로 바꾸고 싶은 칼럼
    •	var_name : long form으로 바꿨을 때 생성되는 변수의 변수명(default : variable)
    •	value_name : long form으로 쌓은 값(default : value)
    •	ignore_index = False : 기존 index 사용 여부

    cat_columns = dat.select_dtypes('object').columns

    long_df = pd.melt(dat,
            value_vars = cat_columns, 
            var_name = 'cat_variable', 
            value_name = 'value', 
            ignore_index = False)

    long_df.head(2)

    long form으로 변환된 데이터는.pivot() 함수를 통해 다시 wide form으로 재변환할 수 있습니다.
    .pivot()
    •	index : 인덱스로 사용될 칼럼
    •	columns : wide form으로 바꿀 칼럼
    •	values : 값으로 입력될 칼럼

    (long_df
        .pivot(columns = 'cat_variable', values = 'value')
        .head(2)
    )


    EDA


    박스 플랏, group by 

    dat.boxplot(column='count',  by='hour',figsize =(10,3))
    plt.tight_layout()

    교재 : dat.groupby(‘hour’).boxplt(column = [‘registered’], subplots = False)

    Pip 업로드
    Setup.py경로에서 
    python setup.py sdist bdist_wheel
    한후
    python -m twine upload dist/*
    id : __token__
    password : api key 복사후 우클릭
    pypi-AgEIcHlwaS5vcmcCJDcyNzBjOWM3LTc3ZjctNGJiMC1iNDc5LTg1ODYyZTAxZDdiMgACKlszLCI5NTZlNDgzNi00OThkLTQ2NjMtYmFjMC03ZjMxMGE4YmY5MjciXQAABiC8UyeWSGLQq7urPbeIKrEXAVhXqdkHbFrOiPiH1Kr0dQ


    Help(함수) ex) help(np.percentile)

    분산 
    Np.var(x, ddof = 1) 표본분산

    막대그래프
    plt.bar(x, y, width=1)

    랜덤 추출
    Chi2.rvs(자유도, size=sample_size)

    히스토그램 (비율)
    plt.hist(s_data, bins=50, density = True)

    히스토그램으로 상위 몇퍼 구하기, 배열 상위 구하기
    n np.percentile(s_data, 95)






    samples = []
    var = np.array([])
    for i in range(500):
        samples.append(norm.rvs(loc = 3, scale =2, size = 20 ))
    var = np.append(var,np.var(samples[i], ddof = 1))

    y2 = var*4.75

    x = np.linspace(0,50,1000)
    y = chi2(19).pdf(x)

    plt.plot(x,y)
    plt.hist(y2, density  = True, bins = 50)

    군집분석
    """

