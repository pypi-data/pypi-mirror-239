def bb():    
    """
    제 28회 ADP 통계기출 문제 풀이 - Python
    1. 문제 4
    다음의 질문에 답하시오.
    1) Geartool 데이터 셋을 이용하여 시간별, 제조사별 불량률 데이터로 생존분석을 시행한 후 25, 30, 35
    개월 후의 불량률을 계산하시오.
    2) 로그 순위법으로 제조사별 불량률이 차이가 있는지 검정하시오.
    예시 답안
    • 데이터 불러오기
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    # Read and manipulate the data
    geartool = pd.read_csv("data/geartool.csv")
    geartool['company'] = geartool['company'].astype('category')
    geartool.head()
    ^༈ time status company
    ^༈ 0 8 1 X
    ^༈ 1 10 1 X
    ^༈ 2 8 0 X
    ^༈ 3 12 1 X
    ^༈ 4 20 1 X
    geartool.status.unique()
    ^༈ array([1, 0], dtype=int64)
    데이터 셋에 의하면 고장여부(0: 정상, 1:고장) 변수를 사용하여 그 시점까지 고장이 난 것을 확인 할 수
    있는 것들 (1)이 있고, 그 시점까지 고장인 난 것을 확인 못한 관찰값들 (0)이 있는 것을 알 수 있다.
    Issac Lee from Statistics Playbook 1
    • 시각화
    각 제조사별 불량품 데이터를 시각화하면 다음과 같다.
    sns.lmplot(data=geartool, x='time', y='status', hue='company', fit_reg=False);
    plt.show()
    20 40 60 80 100 120 140 160
    time
    0.0
    0.2
    0.4
    0.6
    0.8
    1.0
    status
    company
    X
    Y
    • lifelines 패키지를 사용한 불량률 적합
    lifelines 패키지의 KaplanMeierFitter() 함수는 Kaplan༡Meier 생존함수를 적합시켜주는 함수이며,
    관찰 시점과 관찰 상태 (0: right-censored, 1: observed)를 사용하여 수식을 구성할 수 있다. 이는 데이터의
    고장 여부 변수의 값과 일치하므로 (고장 관찰 1, 고장 미관찰 0), 그대로 사용한다.
    from lifelines import KaplanMeierFitter
    # 각 회사에 대한 KaplanMeierFitter 객체 초기화
    kmf_X = KaplanMeierFitter()
    kmf_Y = KaplanMeierFitter()
    # 각 회사별 데이터 필터링
    data_X = geartool[geartool['company'] ^༰ 'X']
    data_Y = geartool[geartool['company'] ^༰ 'Y']
    # 회사 X, Y에 대한 데이터 적합
    kmf_X.fit(data_X['time'], event_observed=data_X['status'], label='X');
    kmf_Y.fit(data_Y['time'], event_observed=data_Y['status'], label='Y');
    슬기로운통계생활 ADP 실기반 2
    • 생존함수 시각화
    각 제조사별 불량품 데이터에 적합된 생존함수를 시각화하면 다음과 같다.
    sns.lmplot(data=geartool, x='time', y='status', hue='company', fit_reg=False);
    kmf_X.plot_survival_function()
    kmf_Y.plot_survival_function()
    plt.show()
    0 20 40 60 80 100 120 140 160
    timeline
    0.0
    0.2
    0.4
    0.6
    0.8
    1.0
    status
    X
    Y
    company
    X
    Y
    • 불량률 추정하기
    생존함수는 주어진 t시점까지 살아있을 확률이므로, 제조사 X와 Y의 25, 30, 35개월에 대응하는 생존률은
    각각 다음과 같이 계산할 수 있다.
    # 회사 X, Y에 대해 시간 25, 30, 35에서의 생존 함수 얻기
    survival_X = kmf_X.survival_function_at_times([25, 30, 35])
    survival_Y = kmf_Y.survival_function_at_times([25, 30, 35])
    survival_X; survival_Y
    ^༈ 25 0.641667
    ^༈ 30 0.641667
    ^༈ 35 0.550000
    ^༈ Name: X, dtype: float64
    ^༈ 25 0.56250
    ^༈ 30 0.46875
    ^༈ 35 0.28125
    ^༈ Name: Y, dtype: float64
    Issac Lee from Statistics Playbook 3
    불량률은 전체 확률에서 생존확률을 빼줘서 계산한다. 각 제조사의 불량률은 다음과 같다.
    1 - survival_X # 제조사 X
    ^༈ 25 0.358333
    ^༈ 30 0.358333
    ^༈ 35 0.450000
    ^༈ Name: X, dtype: float64
    1 - survival_Y # 제조사 Y
    ^༈ 25 0.43750
    ^༈ 30 0.53125
    ^༈ 35 0.71875
    ^༈ Name: Y, dtype: float64
    로그 순위법은 두 함수가 차이가 있는지 검정하는 비모수적 방법이며, logrank_test 함수에 구현되어
    있습니다. 유의 수준 0.05 하에서 검정을 실시하도록 하겠습니다.
    • 귀무가설: 두 생존함수는 동일하다. ( SX(t) = SY (t) for all t)
    • 대립가설: 두 생존함수는 같지 않다.( SX(t) ̸= SY (t) for some t)
    from lifelines.statistics import logrank_test
    results = logrank_test(data_X['time'], data_Y['time'],
    event_observed_A=data_X['status'],
    event_observed_B=data_Y['status'])
    results.print_summary()
    ^༈ <lifelines.StatisticalResult: logrank_test>
    ^༈ t_0 = -1
    ^༈ null_distribution = chi squared
    ^༈ degrees_of_freedom = 1
    ^༈ test_name = logrank_test
    ^༈
    ^༈ ---
    ^༈ test_statistic p ༡log2(p)
    ^༈ 3.64 0.06 4.15
    로그 순위 검정의 통계량값 3.64에 대응하는 p-value값이 0.06으로 이는 유의수준 0.05보다 크므로, 귀무
    가설을 기각할 수 없습니다. 따라서, 두 제조사의 불량률에는 유의미한 차이가 있다고 판단할 통계적 근거가
    충분치 않다고 판단할 수 있습니다.
    슬기로운통계생활 ADP 실기반 4
    2. 문제 5
    다음 표는 슬통 Food의 신제품 홍보 설문 조사 결과이다. 시식 행사에 참여한 고객들의 시식 후 구매 의사의
    변화가 있는지 없는지 검정하시오.
    표 1.1: 시식 전후 비교
    구분 시식전 있음 없음
    시식전 있음 23 7
    NA 없음 18 12
    예시답안
    두 시점에 동일한 대상들의 범주형 응답을 비교하는 것이므로 McNemar 검정을 실시합니다. 먼저, 검정의
    귀무 가설과 대립 가설을 설정합니다.
    • 귀무 가설 : 시식 전과 시식 후의 구매의사에는 변화가 없다.
    • 대립 가설 : 시식 전과 시식 후의 구매의사에 변화가 있다.
    from statsmodels.stats.contingency_tables import mcnemar
    observed = [[23, 18], [7, 12]]
    result = mcnemar(observed, exact=False, correction=False)
    print(f"검정 통계량: {result.statistic:.3f}")
    ^༈ 검정 통계량: 4.840
    print(f"p-값: {result.pvalue:.3f}")
    ^༈ p-값: 0.028
    검정통계량 값 4.84에 대응하는 p-value 값 0.028이 유의 수준 0.05보다 작으므로 귀무 가설을 기각한다.
    따라서 시식 전과 후 구매 의사에 변화가 있다는 통계적인 근거가 충분하다.
    3. 문제 6
    school_exam.csv 파일에는 2개의 고등학교 시험 표준 점수가 들어있습니다. 두 학교 표준 점수의 분포 차이가
    있는지 검정하시오. (단, 각 학생들의 성적은 독립이라고 가정)
    예시 답안
    데이터를 불러오고, 알맞은 형태로 변환합니다.
    # 데이터 불러오기
    school_exam = pd.read_csv("data/school_exam.csv")
    school_exam.head()
    Issac Lee from Statistics Playbook 5
    ^༈ school_A school_B
    ^༈ 0 89.0 94
    ^༈ 1 44.0 49
    ^༈ 2 66.0 69
    ^༈ 3 25.0 30
    ^༈ 4 78.0 37
    • 각 학교별 표본 수 계산
    school_exam.count()
    ^༈ school_A 12
    ^༈ school_B 24
    ^༈ dtype: int64
    두 학교의 표준 점수 분포를 검정하기 위하여 two-sample Kolmogorov-Smirnov 검정을 유의수준 0.05
    하에서 수행합니다.
    • 귀무가설: 두 표본이 같은 분포에서 뽑혀져 나왔다.
    • 대립가설: 두 표본이 다른 분포에서 뽑혀져 나왔다.
    from scipy.stats import ks_2samp
    school_A_scores = school_exam['school_A'].dropna().values
    school_B_scores = school_exam['school_B'].dropna().values
    ks_statistic, p_value = ks_2samp(school_A_scores, school_B_scores)
    print(f'KS༡statistic: {ks_statistic:.3f}, p༡value: {p_value:.3f}')
    ^༈ KS༡statistic: 0.292, p༡value: 0.485
    검정 통계량 값 0.292에 대응하는 p-value값 0.485이 유의수준 값 0.05보다 크므로 귀무가설을 기각 할 수
    없습니다. 두 표본이 같은 분포에서 뽑혀져 나왔다는 가설을 기각 할 수 있는 통계적 근거가 충분히 않으므로
    같은 분포에서 나왔다고 판단합니다.
    4. 문제 7
    health_check.csv파일에는 슬통 병원 환자들의 건강 검진 정보가 들어있습니다. 다음의 물음에 답하시오.
    1) 몸무게를 제어했을 때, 나이와 콜레스테롤 상관계수 및 유의확률 구하라.
    2) 유의수준 0.05 하에서 통계적 의사결정를 수행하라.
    예시답안
    데이터를 불러온 후, 필요한 변수인 몸무게, 나이, 콜레스테롤 변수를 선택합니다.
    슬기로운통계생활 ADP 실기반 6
    import pandas as pd
    school_exam = pd.read_csv("./data/health_check.csv")
    school_exam.columns = school_exam.columns.str.lower()
    school_exam = school_exam[['weight', 'age_group', 'tot_chole']]
    school_exam.head()
    ^༈ weight age_group tot_chole
    ^༈ 0 50 13 44
    ^༈ 1 90 9 44
    ^༈ 2 60 14 50
    ^༈ 3 55 16 52
    ^༈ 4 55 17 54
    몸무게를 제어한 상태에서 두 변수의 상관계수와 그에 대응하는 유의확률은 편상관계수를 구해주는 ppcor
    패키지 함수의 pcor.test() 함수를 사용하여 구할 수 있습니다.
    • 귀무가설: 몸무게가 통제되었을 때, 나이 변수와 콜레스테롤 변수의 상관계수는 0이다.
    • 대립가설: 몸무게가 통제되었을 때, 나이 변수와 콜레스테롤 변수의 상관계수는 0이 아니다.
    import pingouin as pg
    pg.partial_corr(data=school_exam, x='age_group', y='tot_chole', covar='weight')
    ^༈ n r CI95% p༡val
    ^༈ pearson 4098 0.016787 [-0.01, 0.05] 0.282698
    구해진 편상관계수값 0.016787에 대응하는 유의 확률값 0.2826이며, 이는 유의수준 0.05보다 큰 값이므
    로, 귀무가설을 기각할 수 없다. 따라서 몸무게가 통제되었을 때, 나이와 콜레스테롤 상관계수가 0이라고
    판단한다.
    Issac Lee from Statistics Playbook 7
    
    제 30회 ADP 통계기출 문제 풀이 - Python
    1. 문제 5
    아래 데이터는 3개의 철강 제조공장(공장A,공장B,공장C)에서 생산된 제품을3개의 지역(지역1, 지역2, 지역
    3)으로 배송할 때 발생하는 운송비용과 공장별 총 생산량, 지역별 총 수요량이다.
    이 데이터를 활용하여 총 운송비를 최소로 하는 운송계획을 수립하시오. (단, 각 공장에서는 3개 지역으
    로만 운송되고, 공장간 또는 지역 간 운송은 없다고 가정한다.)
    표 1.1: 운송비용과 공장별 총 생산량, 지역별 총 수요량
    구분 지역1 지역2 지역3 총생산량
    공장 A 12만원 5만원 34만원 70개
    공장 B 22만원 2만원 21만원 55개
    공장 C 3만원 23만원 15만원 25개
    총 수요량 30개 50개 70개 NA
    예시답안
    주어진 조건을 선형계획법에 적용할 수 있도록 목적 함수과 제약 사항을 수식으로 나타내보면 다음과 같다.
    Objective :min
    x
    z = 12x1 + 5x2 + 34x3 + 22x4 + 2x5 + 21x6 + 3x7 + 23x8 + 15x9
    Constraints :x1 + x2 + x3 ≤ 70,
    x4 + x5 + x6 ≤ 55,
    x7 + x8 + x9 ≤ 25,
    x1 + x4 + x7 ≥ 30,
    x2 + x5 + x8 ≥ 50,
    x3 + x6 + x9 ≥ 70,
    x1, x2, x3, x4, x5, x6, x7, x8, x9 ≥ 0.
    여기서 x1, x2, x3은 공장 A에서 지역 1, 2, 3으로 운송하는 개수를 나타내고, x4, x5, x6은 공장 B에서 지역
    1, 2, 3으로 운송하는 개수, x7, x8, x9은 공장 C에서 지역 1, 2, 3으로 운송하는 개수를 나타냅니다. 그러나
    python에서 linprog 모듈의 경우 무조건 조건이 ’작거나 같다’라는 것으로 맞춰줘야 하므로, 위의 제약 조건을
    다음과 같이 다시 표현 해줘서 입력해야 한다.
    Issac Lee from Statistics Playbook 1
    x1 + x2 + x3 ≤ 70,
    x4 + x5 + x6 ≤ 55,
    x7 + x8 + x9 ≤ 25,
    −x1 − x4 − x7 ≤ −30,
    −x2 − x5 − x8 ≤ −50,
    −x3 − x6 − x9 ≤ −70.
    import numpy as np
    from itertools import product
    from scipy.optimize import linprog
    # Data
    costs = [12, 5, 34, 22, 2, 21, 3, 23, 15]
    supply = [70, 55, 25]
    demand = [-30, -50, -70]
    # Constraints
    A_ub = [
    [1, 1, 1, 0, 0, 0, 0, 0, 0], # x1 + x2 + x3 ^ཏ 70
    [0, 0, 0, 1, 1, 1, 0, 0, 0], # x4 + x5 + x6 ^ཏ 55
    [0, 0, 0, 0, 0, 0, 1, 1, 1], # x7 + x8 + x9 ^ཏ 25
    [-1, 0, 0, -1, 0, 0, -1, 0, 0], # ༡x1 - x4 - x7 ^ཏ -30 (x1 + x4 + x7 ^༺ 30)
    [0, -1, 0, 0, -1, 0, 0, -1, 0], # ༡x2 - x5 - x8 ^ཏ -50 (x2 + x5 + x8 ^༺ 50)
    [0, 0, -1, 0, 0, -1, 0, 0, -1], # ༡x3 - x6 - x9 ^ཏ -70 (x3 + x6 + x9 ^༺ 70)
    ]
    b_ub = [70, 55, 25, -30, -50, -70]
    # linprog로 해찾기
    result = linprog(c=costs, A_ub=A_ub, b_ub=b_ub, bounds=(0, None), method = "highs")
    result.x.reshape(3, 3)
    ^༈ array([[20., 50., 0.],
    ^༈ [ 0., 0., 55.],
    ^༈ [10., 0., 15.]])
    result.fun
    ^༈ 1900.0
    따라서, 각 공장에서 지역으로 보내는 운송계획은 공장 A에서 지역 1, 2로 20개, 50개, 공장 B에서 지역
    3으로 55개, 공장 C에서 지역 1과 3으로 10개 15개를 운송한다. 이때의 운송비용은 1900만원이 들어간다.
    슬기로운통계생활 ADP 실기반 2
    2. 문제 6
    아래 데이터를 이용하여 헤드셋에 대한 연령대별 선호도 차이가 있는지를 유의수준5%로 검정하시오. (단,
    반올림하여 소수점 셋째 자리까지 표시하시오.)
    • 데이터: headset.csv
    • 데이터는 ID, 헤드셋 종류, 연령대로 구성
    1) 연구가설(H1)과 귀무가설(H0)을 설정하시오.
    2) 유의확률을 계산하고 가설의 채택 여부를 결정하시오.
    예상문제
    • 데이터 불러오기
    import pandas as pd
    import numpy as np
    # 데이터 불러오기
    headset = pd.read_csv("data/headset.csv")
    headset['age'] = headset['age'].astype('category')
    cross_tab = pd.crosstab(headset['headset'], headset['age'])
    cross_tab
    ^༈ age 1 2 3
    ^༈ headset
    ^༈ 1 19 21 25
    ^༈ 2 32 19 27
    ^༈ 3 25 16 16
    데이터는 각 age 그룹 1, 2, 3 별 헤드셋 선호 종류 정보를 포함하고 있습니다. 따라서, 연구가설(H1)과
    귀무가설(H0)을 다음과 같이 설정할 수 있습니다.
    • 귀무가설: 연령대별 헤드셋 분포는 동일하다.
    • 대립가설: 연령대별 헤드셋 분포가 동일하지 않은 그룹이 적어도 하나 존재한다.
    주어진 가설은 카이제곱 동질성 검정을 사용하여 검정할 수 있습니다.
    from scipy.stats import chi2_contingency
    chi2, p, df, expected = chi2_contingency(cross_tab)
    print('X༡squared:', chi2.round(3), 'df:', 2, 'p༡value:', p.round(3))
    ^༈ X༡squared: 3.797 df: 2 p༡value: 0.434
    Issac Lee from Statistics Playbook 3
    검정통계량값 3.797에 대응하는 p‑value가 0.434이므로 유의수준 0.05에 비하여 큽니다. 따라서 귀무가
    설을 기각하지 못하며, 각 연령대별 헤드셋 선호도에는 차이가 없다고 판단할 수 있습니다.
    print(expected)
    ^༈ [[24.7 18.2 22.1 ]
    ^༈ [29.64 21.84 26.52]
    ^༈ [21.66 15.96 19.38]]
    각 셀의 기대빈도가 5이상이므로, 위 검정의 결과를 신뢰 할 수 있습니다.
    3. 문제 7
    각각 6명의 자녀를 가진 다섯 가족이 있다. 각각의 자녀가 아들 또는 딸일 확률은 0.5일 때 아래 질문에 답하
    시오. (단, 반올림하여 소수점 셋째 자리까지 표시하시오.)
    1) 4명 이상의 딸을 가진 가족이 세 가족 이상일 확률을 0에서 1 사이 숫자로 구하시오.
    2) 다섯 가족 중 몇 가족이 4명 이상의 딸을 가질 것으로 기대되는지 계산하시오.
    예시답안
    1) 4명 이상의 딸을 가진 가족이 세 가족 이상일 확률 구하기
    먼저, 6자녀 중 4명 이상의 딸을 가질 확률을 구합니다.
    from scipy.stats import binom
    p_4d = 1 - binom.cdf(3, n=6, p=0.5)
    p_4d
    ^༈ 0.34375
    다섯 가족 중 세 가족 이상일 확률은 이항분포 B(5, 0.34375)를 따르는 확률변수가 3이상 나올 확률과
    동일합니다.
    result = 1 - binom.cdf(2, 5, p_4d)
    result.round(4)
    ^༈ 0.2255
    4명 이상의 딸을 가진 가족이 세 가족 이상일 확률은 약 0.2255입니다.
    2) 이항분포의 기대값은 np이므로, 다음과 같이 계산 가능합니다.
    5 * p_4d
    ^༈ 1.71875
    1.718, 즉, 약 두 가족이 4명 이상의 딸을 가질 것이라 예상됩니다.
    슬기로운통계생활 ADP 실기반 4
    """