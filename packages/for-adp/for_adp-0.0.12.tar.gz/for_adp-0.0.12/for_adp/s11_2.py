def s11_2():
    """
    Chapter 4. 비모수 검정 친해지기
    문제 1. 신제품 촉매제
    슬통 회사에서는 이번에 출시한 새로운 촉매제의 효능을 검증하고 싶어한다. 신제품 촉매재는 기존
    공정에서 사용되는 화학반응 속도를 혁신적으로 줄여주는 기능이 탑재되어 있다고 한다.
    회사 제품 검증 부서에서는 기존 공정의 화학 반응속도와 촉매제를 넣은 후의 반응 속도를 측정하여
    표 4.4 데이터를 만들었다.
    1. 유의수준 5%하에서 신제품 촉매제가 기존의 화학 공정을 단축시킨다고 할 수 있는지에 대하여
    검정하시오.
    2. 촉매제로 인한 단축된 공정 시간에 대하여 90% 신뢰구간을 구하시오.
    import pandas as pd
    import numpy as np
    # 파이썬 코드
    time = [2.17, 0.86, 0.91, 3.11, 1.29, 1.25, 0.76, 2.98, 1.21,
    2.23, 0.67, 1.22, 1.23, 1.21, 1.71, 1.80, 1.41, 1.01,
    0.82, 1.03, 2.03, 0.65, 1.01, 0.45, 0.98, 1.04]
    treat = ['before']*13 + ['add_catalyst']*13
    id = list(range(1,27))
    prac4_1 = pd.DataFrame({'ID':id,
    'Time':time,
    'treat':treat})
    prac4_1.head()
    ^༈ ID Time treat
    ^༈ 0 1 2.17 before
    ^༈ 1 2 0.86 before
    ^༈ 2 3 0.91 before
    ^༈ 3 4 3.11 before
    ^༈ 4 5 1.29 before
    챕터별 연습문제 풀이 | 227
    표 11.4: 촉매제 성능 비교 데이터
    ID Time Treat
    1 2.17 before
    2 0.86 before
    3 0.91 before
    4 3.11 before
    5 1.29 before
    6 1.25 before
    7 0.76 before
    8 2.98 before
    9 1.21 before
    10 2.23 before
    11 0.67 before
    12 1.22 before
    13 1.23 before
    14 1.21 add_catalyst
    15 1.71 add_catalyst
    16 1.80 add_catalyst
    17 1.41 add_catalyst
    18 1.01 add_catalyst
    19 0.82 add_catalyst
    20 1.03 add_catalyst
    21 2.03 add_catalyst
    22 0.65 add_catalyst
    23 1.01 add_catalyst
    24 0.45 add_catalyst
    25 0.98 add_catalyst
    26 1.04 add_catalyst
    가설 설정
    • 𝐻0
    : 신제품 촉매제는 화학 공정 시간을 단축시키지 않는다.
    – 𝜇𝑏𝑒𝑓𝑜𝑟𝑒 ≤ 𝜇𝑐𝑎𝑡𝑎𝑙𝑦𝑠𝑡
    • 𝐻𝐴: 신제품 촉매제는 화학 공정 시간을 단축시킨다.
    – 𝜇𝑏𝑒𝑓𝑜𝑟𝑒 > 𝜇𝑐𝑎𝑡𝑎𝑙𝑦𝑠𝑡
    정규성 검정
    각 그룹에 대한 정규성 검정을 시각화 기법과 Shapiro‑wilk 검정을 사용하여 시행한다.
    before = prac4_1[prac4_1['treat']^༰'before']
    add_catalyst = prac4_1[prac4_1['treat']^༰'add_catalyst']
    import pingouin as pg
    import matplotlib.pyplot as plt
    228 | 챕터별 연습문제 풀이
    11
    plt.subplot(1,2,1)
    ^༈ <AxesSubplot:>
    ax = pg.qqplot(before['Time'], dist='norm')
    plt.subplot(1,2,2)
    ^༈ <AxesSubplot:>
    ax = pg.qqplot(add_catalyst['Time'], dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.show()
    0 2
    Theoretical quantiles
    1
    0
    1
    2
    Ordered quantiles
    R
    2 = 0.849
    2 0 2
    Theoretical quantiles
    2
    0
    2
    Ordered quantiles
    R
    2 = 0.943
    두 그룹의 QQ plot을 판단해 보았을 때, 신뢰구간 안에 모든 데이터가 들어있으나 가운데 부분에서
    두 그룹 모두 기준선을 벗어나는 경향성을 보인다. 좀 더 정확한 검정을 위하여 유의수준 5% 하에서
    Shapiro‑Wilk 검정을 시행한다.
    • Shapiro‑Wilk 검정의 귀무가설과 대립가설은 다음과 같다.
    – 귀무가설: 데이터가 정규분포를 따른다.
    – 대립가설: 데이터가 정규분포를 따르지 않는다.
    from scipy.stats import shapiro
    shapiro(before['Time'])
    ^༈ ShapiroResult(statistic=0.8367362022399902, pvalue=0.019262485206127167)
    챕터별 연습문제 풀이 | 229
    shapiro(add_catalyst['Time'])
    ^༈ ShapiroResult(statistic=0.941055178642273, pvalue=0.4707110524177551)
    두 그룹 중 before 그룹에 대응하는 p‑value 값 0.01926이 유의수준인 5%보다 작으므로 귀무가설
    을 기각한다. 따라서 데이터가 정규성을 따른다고 판단할 수 없으므로, 비모수 검정을 진행하도록 한다.
    따라서, 앞에서 설정한 귀무가설, 대립가설의 모수가 모분포의 중앙값을 나타내는 것에 주의하자.
    등분산성 검정 유의수준 5%하에서 두 그룹 데이터의 등분산성 가정을 Levene’s test를 통하여 확
    인한다.
    plt.subplot(1,2,1)
    ^༈ <AxesSubplot:>
    plt.hist(before['Time'], bins=30);
    plt.subplot(1,2,2)
    ^༈ <AxesSubplot:>
    plt.hist(add_catalyst['Time'],bins=30);
    plt.show();
    1 2 3
    0
    1
    2
    3
    1 2
    0
    1
    2
    3
    before 그룹의 히스토그램으로 판단했을때 정규성이 보장되지 않는 데이터이며, 오른쪽으로 살짝
    치우쳐있는 데이터 이므로, 좀 더 robust한 검정을 위하여 center 옵션은 median으로 설정한 후 진행
    하였다.
    • 귀무가설: 두 그룹의 모분산이 같다.
    • 대립가설: 두 그룹의 모분산은 같지 않다.
    230 | 챕터별 연습문제 풀이
    11
    from scipy.stats import levene
    a = before['Time']
    b = add_catalyst['Time']
    levene(b, a, center='median')
    ^༈ LeveneResult(statistic=1.404486168289024, pvalue=0.24757651251351717)
    검정의 p‑value값 0.2476이 유의수준인 5% 보다 크므로 귀무가설을 기각하지 못한다. 따라서 두
    그룹 데이터는 등분산 가정을 만족한다고 판단하였다.
    위와 같은 이유로, 가장 적합한 검정은 Mann‑Whitney‑Wilcoxon U test로 판단하여 검정을 진
    행한다.
    • 𝐻0
    : 신제품 촉매제는 화학 공정 시간을 단축시키지 않는다.
    – 𝜂𝑏𝑒𝑓𝑜𝑟𝑒 = 𝜂𝑐𝑎𝑡𝑎𝑙𝑦𝑠𝑡
    • 𝐻𝐴: 신제품 촉매제는 화학 공정 시간을 단축시킨다.
    – 𝜂𝑏𝑒𝑓𝑜𝑟𝑒 > 𝜂𝑐𝑎𝑡𝑎𝑙𝑦𝑠𝑡
    from scipy.stats import mannwhitneyu
    mannwhitneyu(before['Time'],add_catalyst['Time'], alternative='greater')
    ^༈ MannwhitneyuResult(statistic=106.5, pvalue=0.1350263415415442)
    검정에 대응하는 p‑value 값 0.135가 유의수준 0.05보다 크므로, 귀무가설을 기각하지 못한다.
    따라서 신제품 촉매제가 기존 화학 공정 시간을 단축 시키지 않는다고 판단한다.
    • 참고: 데이터에 tie가 존재하는 경우 mannwhitneyu() 함수는 정규근사에 의한 유의 확률을 계산
    한다.
    len(prac4_1['Time']) - len(prac4_1["Time"].unique())
    ^༈ 2
    신뢰구간
    비모수 검정의 정확한 신뢰구간을 구하는 것은 상당히 까다롭다. 따라서 주어진 표본으로 가능한 감소
    시간의 표본들을 만들고, 이를 통하여 유추하도록 한다.
    # 'before' 그룹과 'add_catalyst' 그룹의 score 값을 추출
    u = prac4_1[prac4_1['treat'] ^༰ 'before']['Time'].values
    v = prac4_1[prac4_1['treat'] ^༰ 'add_catalyst']['Time'].values
    챕터별 연습문제 풀이 | 231
    # u와 v의 가능한 모든 조합 생성
    df = pd.DataFrame({'Var1': np.repeat(u, len(v)),
    'Var2': np.tile(v, len(u))})
    # 각 조합에 대해 Var1과 Var2의 차이 계산
    m = df['Var1'] - df['Var2']
    # m의 5% 및 95% 분위수 계산
    quantiles = m.quantile([0.05, 0.95])
    quantiles
    ^༈ 0.05 -0.920
    ^༈ 0.95 2.092
    ^༈ dtype: float64
    따라서 우리는 촉매제로 인한 공정 시간의 분포 실제 중앙값 감소 시간은 (−0.920, 2.092) 구간에
    존재할 것이라 90% 신뢰한다.
    문제 2. 심장 질환 약 효능
    슬통제약의 신약이 심장 질환 환자의 혈압을 낮출 수 있는지 검증하려고 한다. 표본으로 15명의 환자가
    선택되었으며, 약을 복용하기 전과 복용한 후의 혈압을 측정하였다.
    • 복용전: 130, 125, 120, 135, 140, 136, 129, 145, 150, 135, 128, 140, 139, 130, 145
    • 복용후: 125, 120, 115, 130, 135, 134, 128, 140, 145, 134, 127, 140, 138, 129, 142
    약이 혈압을 실제로 낮추는 것인지 검증하기 위하여 부호 검정을 실시하라. 유의 수준은 0.05로
    하고, 검정을 수행하시오.
    예시 답안
    부호 검정은 각 쌍의 차이에 대해 부호를 검사하여, 이 경우에는 복용 전, 후의 혈압 차이가 0인지
    아니면 혈압이 낮아졌는지(전 ‑ 후 혈압 차이가 0보다 큰 지)를 검사하고자 합니다. 진행하고자 하는
    검정의 귀무가설과 대립가설은 다음과 같습니다.
    • 귀무 가설: 약 복용 전과 복용 후 혈압차 분포의 중앙값은 0이다.
    – Δ ∶= 𝜂𝑝𝑎𝑖𝑟1
    − 𝜂𝑝𝑎𝑖𝑟2
    = 0
    • 대립 가설: 약 복용 전과 복용 후 혈압차 분포의 중앙값은 0보다 크다.
    – Δ > 0
    먼저, 각 환자의 혈압 차이(복용 전 ‑ 복용 후)를 계산하고, 양수와 0의 개수를 세어보겠습니다.
    from scipy.stats import binom_test
    import numpy as np
    232 | 챕터별 연습문제 풀이
    11
    # 복용 전 후의 혈압
    before_np = np.array([130, 125, 120, 135, 140, 136, 129,
    145, 150, 135, 128, 140, 139, 130, 145])
    after_np = np.array([125, 120, 115, 130, 145, 134, 128,
    140, 145, 134, 127, 140, 140, 129, 142])
    # 차이 계산
    diff = before_np - after_np
    # 차이가 0보다 큰 경우를 세기 (혈압이 낮아진 경우)
    successes = sum(diff > 0)
    successes
    ^༈ 12
    Python에서 제공하는 sign_test() 함수의 경우 단측검정 옵션을 제공하고 있지 않습니다.
    from statsmodels.stats.descriptivestats import sign_test
    # statsmodels의 sign_test 함수를 사용하여 부호 검정 수행
    test_statistic, p_value = sign_test(diff, mu0=0)
    test_statistic, p_value
    ^༈ (5.0, 0.012939453125)
    binom_test() 함수를 사용하여 단측검정 p‑vlaue를 계산하면 다음과 같습니다.
    # 이항 검정 수행
    # from scipy.stats import binom
    # 1༡binom.cdf(11, 14, 0.5)
    p_value = binom_test(successes, 14, alternative='greater')
    successes, len(diff[diff ^໻ 0]), p_value
    ^༈ (12, 14, 0.0064697265625)
    이항분포 (14, 0.5)에서 검정 통계량 값 12보다 크거나 같은 값이 나올 확률은 0.6%로 유의 수준
    5%보다 낮아 귀무가설을 기각한다. 따라서 신약이 심장 질환 환자의 혈압을 낮출 수 있다고 판단한다.
    Chapter 5. 카이제곱 검정 친해지기
    챕터별 연습문제 풀이 | 233
    문제 1. 휴대전화 사용자들의 정치 성향은 다를까?
    다음은 휴대전화와 유선전화를 모두 사용하는 사용자들과 유선전화만을 사용하는 사용자들의 정치
    성향을 조사한 데이터이다. 유의수준 5%하에서 정당 지지와 핸드폰 사용 유무 사이에 상관성을 검정
    해보세요.
    표 11.5: 정치 성향 설문조사 결과
    정당지지 핸드폰 유선전화
    진보 49 47
    중도 15 27
    보수 32 30
    데이터 입력
    import pandas as pd
    data = [[49,47],[15,27],[32,30]]
    columns = ["핸드폰", "유선전화"]
    index = ["진보", "중도", "보수"]
    phone_data = pd.DataFrame(data, columns=columns, index=index)
    phone_data
    ^༈ 핸드폰 유선전화
    ^༈ 진보 49 47
    ^༈ 중도 15 27
    ^༈ 보수 32 30
    귀무가설 vs. 대립가설
    • 𝐻0
    : 핸드폰 사용 여부와 정당 지지 성향은 독립이다.
    • 𝐻𝐴: 핸드폰 사용 여부와 정당 지지 성향은 독립이 아니다.
    기대빈도 체크하기 독립성 검정은 각 셀의 기대빈도가 모두 5 이상 되어야 결과를 신뢰할 수 있다.
    아래의 결과를 살펴보면, 각 셀의 기대빈도가 모두 5 이상인 것을 확인할 수 있다.
    from scipy.stats import chi2_contingency
    result = chi2_contingency(phone_data)
    result[3]
    ^༈ array([[46.08, 49.92],
    ^༈ [20.16, 21.84],
    ^༈ [29.76, 32.24]])
    234 | 챕터별 연습문제 풀이
    11
    검정통계량과 p‑value
    x_squared, p_value, df, expected = result
    print('x༡squared:',x_squared)
    ^༈ x༡squared: 3.2199060739887355
    print('p༡value:',p_value)
    ^༈ p༡value: 0.19989700161872206
    카이제곱 통계량 3.219에 대응하는 p‑value 0.199는 유의수준 5%보다 크므로, 귀무가설을 기각하
    지 못한다. 따라서, 휴대폰 사용여부는 정당지지와는 관련이 없다 (독립이다) 라고 판단한다.
    문제 2. 여자아이 vs. 남자아이
    다음은 4자녀를 둔 130가구를 조사하여 여자아이의 수를 조사한 자료이다. 여자 아이의 출생 비율이
    50% 인지 유의수준 5%하에서 검정해보세요.
    표 11.6: 4자녀 가정 여자아이 숫자 조사 결과
    Girl Frequency
    0 10
    1 31
    2 44
    3 34
    4 11
    이항분포
    확률변수 𝑋가 이항분포 𝑛, 𝑝를 따를 때, 𝑋의 확률질량함수는 다음과 같다.
    𝑝 (𝑥; 𝑛, 𝑝) = ( 𝑛
    𝑥
    ) 𝑝𝑥
    (1 − 𝑝)𝑛−𝑥
    귀무가설 vs. 대립가설
    • 𝐻0
    : 여자아이의 출생율은 0.5이다.
    • 𝐻𝐴: 여자아이의 출생율은 0.5가 아니다.
    기대빈도
    귀무가설 하에서 4자녀 가정에서 여자아이의 숫자는 이항분포 𝑛 = 4, 𝑝 = 0.5에서 관찰된 관찰값이
    라 생각할 수 있다. 따라서 4자녀 가구에서 여자아이가 0명에서 4명이 있을 확률을 다음과 같이 구할
    수 있다.
    챕터별 연습문제 풀이 | 235
    from scipy.stats import binom
    binom.pmf(range(5), 4, 0.5)
    ^༈ array([0.0625, 0.25 , 0.375 , 0.25 , 0.0625])
    위의 확률을 사용하여 기대빈도를 구하면 다음과 같다.
    130 * binom.pmf(range(5), 4, 0.5)
    ^༈ array([ 8.125, 32.5 , 48.75 , 32.5 , 8.125])
    기대 빈도가 모두 5이상이므로 카이제곱 검정을 실시할 수 있다.
    적합도검정
    chisq.test()에서는 다음과 같이 관찰값과 대응하는 확률값을 사용하여 검정을 진행할 수 있다.
    from scipy.stats import chisquare
    import numpy as np
    observed_frequencies = [10, 31, 44, 34, 11]
    expected_frequencies = binom.pmf(range(5), 4, 0.5) * sum(observed_frequencies)
    chisquare(observed_frequencies, expected_frequencies)
    ^༈ Power_divergenceResult(statistic=2.0512820512820507, pvalue=0.726327096627745)
    검정통계량 2.0513에 대응하는 유의확률인 p‑value 값 0.7263이 유의수준 5%보다 크므로, 귀무
    가설을 기각하지 못한다. 따라서 여자아이 출생비율이 50%라고 판단한다.
    문제 3. 지역별 대선 후보의 지지율
    어느 도시에 있는 3개의 선거구에서 특정후보 A를 지지하는 유권자의 비율을 비교하기 위해 각 선거
    구에서 300명을 무작위를 추출하여 조사한 데이터이다. 주어진 데이터를 대상으로 후보A를 지지하는
    비율이 3개 선거구 간에 차이가 있는지를 5% 유의수준에서 검정하라.
    표 11.7: 지역별 대선 후보의 지지율
    구분 선거구 1 선거구 2 선거구 3
    지지함 176 193 159
    지지하지 않음 124 107 141
    236 | 챕터별 연습문제 풀이
    11
    귀무가설 vs. 대립가설
    • 𝐻0
    : 각 선거구 별 A 후보의 지지율은 동일하다. 𝑝1 = 𝑝2 = 𝑝3
    • 𝐻𝐴: 지지율이 다른 선거구가 적어도 하나 존재한다.
    p‑value 계산 및 결론 도출
    import numpy as np
    from scipy.stats import chi2_contingency
    # 데이터 설정: 교차표
    data = np.array([[176, 124], # 선거구 1
    [193, 107], # 선거구 2
    [159, 141]]) # 선거구 3
    chi2, p, df, expected = chi2_contingency(data)
    expected
    ^༈ array([[176., 124.],
    ^༈ [176., 124.],
    ^༈ [176., 124.]])
    각 셀의 기대빈도가 5보다 크므로 카이제곱 동질성 검정의 결과를 신뢰 할 수 있다.
    print(chi2.round(3), p.round(3))
    ^༈ 7.945 0.019
    검정통계량 7.9454에 대응하는 p‑value 값 0.019가 유의수준 0.05보다 작으므로, 귀무가설을 기
    각한다. 따라서 모든 선거구의 지지율이 같지 않다고 판단할 통계적 근거가 충분하다.
    문제 4. 데이터가 특정분포를 따를까?
    다음의 데이터가 주어졌을때, 카이제곱 검정법을 사용하여 데이터가 모수가 2인 지수분포를 따르는지
    유의수준 5% 하에서 검정해보세요.
    0.211, 0.098, 0.736, 0.091, 0.756, 1.039, 0.391, 0.172, 2.113, 0.013, 0.073, 0.812, 0.132,
    0.263, 0.124, 0.339, 0.092, 0.24, 0.438, 0.584, 0.722, 0.231, 0.033, 0.203, 0.177, 0.095, 0.352,
    0.023
    • 데이터는 3개 구간 (0, 0.2], (0.2, 0.4], (0.4, Inf )을 사용해서 검정하세요.
    데이터 구간 나누기
    챕터별 연습문제 풀이 | 237
    x = [0.211, 0.098, 0.736, 0.091, 0.756, 1.039, 0.391, 0.172,
    2.113, 0.013, 0.073, 0.812, 0.132, 0.263, 0.124, 0.339,
    0.092, 0.24, 0.438, 0.584, 0.722, 0.231, 0.033, 0.203,
    0.177, 0.095, 0.352, 0.023]
    result = pd.cut(x,
    bins=[0, 0.2, 0.4, float("inf")],
    labels=["0,0.2", "0.2,0.4", "0.4,Inf"])
    print(result.value_counts())
    ^༈ 0,0.2 12
    ^༈ 0.2,0.4 8
    ^༈ 0.4,Inf 8
    ^༈ dtype: int64
    기대빈도 구하기
    주어진 구간에 대응하는 확률을 구하면 다음과 같다.
    from scipy.stats import expon
    import numpy as np
    x = [0.2, 0.4, float("inf")]
    rate = 2
    exp_cdf = expon.cdf(x, scale=1/rate)
    exp_p = exp_cdf - np.insert(exp_cdf, 0, 0)[:-1]
    print(exp_p)
    ^༈ [0.32967995 0.22099108 0.44932896]
    주어진 확률로 기대빈도를 구하면 다음과 같다.
    exp_p * 28
    ^༈ array([ 9.23103871, 6.18775029, 12.581211 ])
    각 셀의 기대빈도 값이 5보다 크므로, 카이제곱 적합도 검정을 수행할 수 있다.
    적합도 검정
    238 | 챕터별 연습문제 풀이
    11
    from scipy.stats import chisquare
    chi2, p_value = chisquare(f_obs=result.value_counts(), f_exp=exp_p * 28)
    print("Chi༡square statistic:", chi2)
    ^༈ Chi༡square statistic: 3.0295112382237264
    print("p༡value:", p_value)
    ^༈ p༡value: 0.2198619083314235
    검정통계량 값 3.0295에 대응하는 유의확률 0.2199는 유의수준 5%보다 크므로, 귀무가설을 기각할
    수 없다.
    설문조사 환자 수
    슬통 병원에서는 최근 도입한 진료 서비스에 대한 환자 만족도를 평가하고자 합니다. 병원은 환자들에
    게 만족도 설문지를 무작위로 분배하려고 합니다. 설문을 시작하기 전에, 병원은 적절한 표본 크기를
    결정하려고 합니다.
    설문지는 환자의 진료 서비스에 대한 만족도를 7점 척도로 묻습니다. 병원은 특히 환자 중 만족하거
    나 매우 만족하는 비율 𝑝에 관심이 있습니다 (이는 7점 척도 중 상위 두 단계에 해당합니다).
    병원은 만족도 추정의 신뢰 수준을 95%로 설정하려고 하며, 오차 범위는 3% 또는 0.03 이하로 원
    합니다. 보수적인 추정을 위하여 확률은 0.5로 가정하고자 합니다. 조건 만족을 위하여 설문에 필요한
    최소 환자 수를 구해주세요.
    공식을 사용한 표본수 구하기
    신뢰구간 공식을 사용하여 표본수와 관련한 다음과 같은 공식을 유도할 수 있다.
    ̂𝑝(1 − ̂𝑝)
    (
    0.03
    𝑧𝛼/2 )
    2 ≤ 𝑛
    여기에 ̂𝑝 값을 0.5로 가정하고 𝑛 구하면 다음과 같다.
    from scipy.stats import norm
    p_hat = 0.5
    p_hat * (1-p_hat) / (0.03 / norm.ppf(0.975))^*2
    ^༈ 1067.0718946372572
    따라서 필요한 표본 수는 1068개 이다.
    챕터별 연습문제 풀이 | 239
    설문조사 환자 수 2
    다음은 슬통 병원에서 작년에 조사해놓은 환자들의 만족도 조사 결과 입니다.
    7, 7, 6, 7, 6, 3, 6, 4, 5, 2, 7, 6, 6, 6, 6, 6, 6, 6, 7, 6
    위의 데이터를 사용하여 설문에 필요한 최소 환자 수를 구해주세요. 병원은 만족도 추정의 신뢰
    수준을 98%로 설정하려고 하며, 오차 범위는 2% 또는 0.02 이하로 원합니다.
    표본 수 구하기 (데이터 사용)
    표본을 구하는 것은 위에서 사용한 공식을 그대로 이용할 수 있다. 주어진 데이터에서 6점과 7점의
    비율을 구하자.
    import numpy as np
    # Convert data to numpy array
    data_np = np.array([7, 7, 6, 7, 6, 3, 6, 4, 5, 2,
    7, 6, 6, 6, 6, 6, 6, 6, 7, 6])
    # Calculate the proportion using numpy
    p_hat_np = np.mean((data_np ^༰ 6) | (data_np ^༰ 7))
    p_hat_np
    ^༈ 0.8
    만족도 추정값은 0.8로 설정한다.
    from scipy.stats import norm
    p_hat = 0.8
    p_hat * (1-p_hat) / (0.02 / norm.ppf(0.99))^*2
    ^༈ 2164.757772421736
    따라서 주어진 조건을 만족하기 위한 필요한 총 표본수는 2165명이다.
    유권자의 마음
    슬통 신문사에서는 다음과 같은 42명의 시민들을 대상으로 지난 1월 A 대통령 후보를 지지하는 조사
    하였습니다. 다음은 대통령이 된 A 후보의 임기 시작 후 6개월이 지난 오늘, 다시 한번 동일 인원들에게
    전화를 걸어 대통령 후보를 지지하는지 물어본 결과입니다.
    당선 후 지지여부
    당선 전 지지여부 지지함 지지하지 않음
    지지함 17 7
    240 | 챕터별 연습문제 풀이
    11
    당선 후 지지여부
    지지하지 않음 5 13
    사람들의 A 후보에 대한 지지율이 당선 전과 당선 후 변하였는지 검정해보세요.
    McNemar 검정
    McNemar 검정은 2x2 교차표(contingency table)에 대한 카이제곱 검정의 특별한 경우입니다.
    주로, 두 시점 또는 두 조건에서 동일한 대상들의 범주형 응답을 비교할 때 사용됩니다.
    전처리 결과 A 전처리 결과 B
    처리 전 A a b
    처리 전 B c d
    • 검정 통계량: 𝜒
    2 =
    (𝑏−𝑐)2
    𝑏+𝑐 ∼ 𝜒2
    (1)
    먼저, McNemar 검정의 귀무 가설과 대립 가설을 설정합니다:
    귀무 가설 : 당선 전과 당선 후의 지지율은 동일하다. 대립 가설 : 당선 전과 당선 후의 지지율은
    다르다.
    from scipy.stats import chi2
    b = 7
    c = 5
    # 검정통계량 계산
    stat = (b - c)^*2 / (b + c)
    stat
    # 유의확률
    ^༈ 0.3333333333333333
    1 - chi2.cdf(stat, 1)
    ^༈ 0.5637028616507731
    검정통계량 값 0.3에 대응하는 p‑value 값이 유의 수준 0.05보다 크므로 귀무가설을 기각하지 못
    한다. 따라서 당선 전과 후의 지지율은 동일하다고 판단한다.
    statsmodels 버전 (참고)
    챕터별 연습문제 풀이 | 241
    from statsmodels.stats.contingency_tables import mcnemar
    # 주어진 데이터
    observed = [[17, 7], [5, 13]]
    # McNemar 검정 수행 (옵션 2개 꼭 꺼줘야 함)
    result = mcnemar(observed, exact=False, correction=False)
    print("검정 통계량:", result.statistic)
    ^༈ 검정 통계량: 0.3333333333333333
    print("p-값:", result.pvalue)
    ^༈ p-값: 0.5637028616507731
    Chapter 6. 분산분석 친해지기
    펭귄의 부리길이
    palmerpenguins 패키지의 penguins 데이터에는 펭귄 종류별 부리길이 ( bill_length_mm ) 정보가 들
    어있다. 펭귄의 종류에 따라서 부리길이가 다르다고 할 수 있는지 유의수준 1% 하에서 검정해보세요.
    from palmerpenguins import load_penguins
    penguins = load_penguins()
    penguins.isnull().sum()
    ^༈ species 0
    ^༈ island 0
    ^༈ bill_length_mm 2
    ^༈ bill_depth_mm 2
    ^༈ flipper_length_mm 2
    ^༈ body_mass_g 2
    ^༈ sex 11
    ^༈ year 0
    ^༈ dtype: int64
    변수 별 결측치 정보를 조사해 보았을 때, 독립 변수인 부리길이가 결측인 데이터 2개가 존재한다.
    이를 제외한 나머지 데이터를 사용하여 분석을 진행하도록 하자.
    242 | 챕터별 연습문제 풀이
    11
    my_penguins = penguins[['species', 'bill_length_mm']].dropna()
    print(my_penguins.shape)
    ^༈ (342, 2)
    총 342개의 관찰값이 존재한다. 펭귄 종 별 부리 길이의 모평균이 다른지 검정하기 위하여 ANOVA
    를 진행하도록 한다.
    귀무 vs. 대립가설
    • 귀무가설: 펭귄 종별 부리길이 평균은 동일하다.
    – 𝜇𝑎𝑑𝑒𝑙𝑖𝑒 = 𝜇𝑐ℎ𝑖𝑛𝑠𝑡𝑟𝑎𝑝 = 𝜇𝑔𝑒𝑛𝑡𝑜𝑜
    • 대립가설: 펭귄 종 간 부리 길이가 다른 그룹이 적어도 하나 존재한다.
    – Not all of the 𝜇𝑖
    are equal
    Python에서 ANOVA 테이블 구하기
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    model = ols('bill_length_mm ~ C(species)', data=my_penguins).fit()
    aov_table = sm.stats.anova_lm(model, typ=2)
    print(aov_table)
    ^༈ sum_sq df F PR(>F)
    ^༈ C(species) 7194.317439 2.0 410.600255 2.694614e-91
    ^༈ Residual 2969.888087 339.0 NaN NaN
    ANOVA 테이블 결과를 보면, 귀무가설 하에서 검정 통계량인 F 값이 410.6이 나왔고, 대응하는
    p‑value는 2e‑91보다 작은 것을 확인하였다. 따라서 유의수준 1%보다 훨씬 작으므로 귀무가설을
    기각한다. 펭귄 종 간 부리길이가 다른 종이 적어도 하나 존재한다.
    위의 ANOVA 검정 결과를 신뢰할 수 있는지 ANOVA 모델의 가정을 체크하자.
    • 잔차의 정규성
    • 잔차의 등분산성
    import matplotlib.pyplot as plt
    import scipy.stats as stats
    fig = plt.figure(figsize= (10, 10))
    ax = fig.add_subplot(111)
    챕터별 연습문제 풀이 | 243
    normality_plot, stat = stats.probplot(model.resid, plot= plt, rvalue= True)
    ax.set_title("Probability plot of model residual's", fontsize= 10)
    ^༈ Text(0.5, 1.0, "Probability plot of model residual's")
    ax.set;
    plt.show()
    3 2 1 0 1 2 3
    Theoretical quantiles
    5
    0
    5
    10
    Ordered Values
    R
    2 = 0.9878
    Probability plot of model residual's
    그래프로 보아 잔차의 QQ plot이 기준선을 따라 분포하는 것을 확인할 수 있다. 따라서, 정규성을
    만족할 것으로 판단된다. 최종 판단을 위해서 샤피로‑윌크 검정을 수행한다.
    • 귀무가설: 잔차가 정규분포를 따른다.
    • 대립가설: 잔차가 정규분포를 따르지 않는다.
    stats.shapiro(model.resid)
    ^༈ ShapiroResult(statistic=0.989031195640564, pvalue=0.011304551735520363)
    샤피로 윌크 검정의 검정 통계량 값 𝑊 = 0.98903에 대응하는 p‑value값이 0.01131로 주어진
    유의수준 0.01보다 크므로 귀무가설을 기각할 수 없다. 따라서 잔차가 정규성을 만족한다고 판단한다.
    다음은 잔차의 등분산 검정을 위하여 levene’s 검정을 수행하도록 한다.
    • 귀무가설: 펭귄 종별 잔차의 분산은 같다.
    244 | 챕터별 연습문제 풀이
    11
    – 𝜎
    2
    𝑎𝑑𝑒𝑙𝑖𝑒 = 𝜎2
    𝑐ℎ𝑖𝑛𝑠𝑡𝑟𝑎𝑝 = 𝜎2
    𝑔𝑒𝑛𝑡𝑜𝑜
    • 대립가설: 펭귄 종별 잔차의 분산 중 다른 쌍이 적어도 하나 존재한다.
    – Not all of the 𝜎
    2
    𝑖
    s are equal
    stats.levene(my_penguins[my_penguins['species'] ^༰ 'Adelie']['bill_length_mm'],
    my_penguins[my_penguins['species'] ^༰ 'Chinstrap']['bill_length_mm'],
    my_penguins[my_penguins['species'] ^༰ 'Gentoo']['bill_length_mm'],
    center='mean')
    ^༈ LeveneResult(statistic=2.833610648953925, pvalue=0.060193797718201124)
    검정통계량 값 2.833에 대응하는 p‑value는 0.06019로 유의수준 1% 하에서 귀무가설을 기각하지
    못한다. 따라서, 잔차의 집단간 등분산성 가정 역시도 만족한다고 판단한다.
    사후검정
    ANOVA의 귀무가설이 기각되었으므로, 사후 분석을 통하여 모평균이 다른 그룹을 판변하기 위한
    사후분석을 수행한다. 사후 분석은 aov() 함수의 결과값을 입력값으로 받을 수 있는 TukeyHSD()을
    사용하여 수행하도록 한다.
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    tukey_result = pairwise_tukeyhsd(my_penguins['bill_length_mm'], my_penguins['species'], alpha=0.01)
    print(tukey_result)
    ^༈ Multiple Comparison of Means - Tukey HSD, FWER=0.01
    ^༈ ==========================================================
    ^༈ group1 group2 meandiff p༡adj lower upper reject
    ^༈ ----------------------------------------------------------
    ^༈ Adelie Chinstrap 10.0424 -0.0 8.7745 11.3104 True
    ^༈ Adelie Gentoo 8.7135 -0.0 7.659 9.768 True
    ^༈ Chinstrap Gentoo -1.3289 0.0089 -2.6409 -0.017 True
    ^༈ ----------------------------------------------------------
    결과를 확인해보면, 모든 펭귄 종별 부리 길이는 통계적으로 유의미한 차이를 보인다고 판단할 수
    있다. (각 사후 검정의 adjusted p‑value 값이 0.01보다 작다.)
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.set_palette(["#00AFBB", "#E7B800", "#FC4E07"])
    plt.figure(figsize=(8, 6))
    챕터별 연습문제 풀이 | 245
    ^༈ <Figure size 800x600 with 0 Axes>
    sns.boxplot(x='species', y='bill_length_mm', data=my_penguins)
    ^༈ <AxesSubplot:xlabel='species', ylabel='bill_length_mm'>
    sns.swarmplot(x='species', y='bill_length_mm', data=my_penguins, color='black', size=2)
    ^༈ <AxesSubplot:xlabel='species', ylabel='bill_length_mm'>
    sns.pointplot(x='species', y='bill_length_mm', data=my_penguins, color='red', markers='o', errorbar=None)
    ^༈ <AxesSubplot:xlabel='species', ylabel='bill_length_mm'>
    plt.xlabel('Species')
    ^༈ Text(0.5, 26.722222222222207, 'Species')
    plt.ylabel('Bill length (mm)')
    ^༈ Text(52.847222222222214, 0.5, 'Bill length (mm)')
    plt.show()
    Adelie Gentoo Chinstrap
    Species
    35
    40
    45
    50
    55
    60
    Bill length (mm)
    따라서, 유의수준 0.01을 기준으로 각 펭귄 종별 부리 길이는 통계적으로 유의미한 차이를 보인다고
    판단하며, Adelie < Gentoo < Chinstrap의 순서대로 평균이 증가한다고 판단한다.
    246 | 챕터별 연습문제 풀이
    11
    드릴 도구 검정 절차 (Drilling process)
    drilling༡tool༡exam.csv 데이터를 사용하여 다음 물음에 답하세요.
    슬통 철공 회사에서는 5개의 브랜드의 드릴 소재를 사용하여 철판에 구멍을 뚫은 작업을 하고 있다.
    회사 제품은 2.5cm 직경을 가진 철판인데, 브랜드 별 사용하는 소재들이 미세하게 달라, 직경에 차이
    가 발생하는지 알아보고자 한다. 품질 팀은 제품 품질을 유지하기 위하여 온도의 영향도 조사하기로
    하였다. 슬통이는 한 명의 품질 관리사에게 각기 다른 온도에서 브랜드별 드릴을 무작위로 20개씩
    선택하여 뚫은 구멍의 직경을 측정하도록 하였다.
    1) 데이터를 사용 각 브랜별, 온도별 평균과 표준편차 정리 표를 만드세요.
    데이터 로드 및 전처리 (Wide 형태 데이터 전처리 연습)
    import pandas as pd
    # Load the dataset
    data = pd.read_csv("./data/drilling༡tool༡exam.csv", skiprows=1)
    data.head()
    ^༈ Brand Temp Mesurement 1 ^^. Mesurement 18 Mesurement 19 Mesurement 20
    ^༈ 0 A 100 25.031768 ^^. 25.029239 25.029938 25.032016
    ^༈ 1 A 200 25.027100 ^^. 25.028416 25.028347 25.028968
    ^༈ 2 A 300 25.024713 ^^. 25.023498 25.026318 25.025532
    ^༈ 3 B 100 25.018161 ^^. 25.017452 25.018334 25.016180
    ^༈ 4 B 200 25.020642 ^^. 25.020781 25.018409 25.021757
    ^༈
    ^༈ [5 rows x 22 columns]
    데이터를 불러오면 브랜드별 온도별로 총 20개의 직경 데이터가 존재한다. 각 그룹별 평균과 표준
    편차값을 계산하면 다음과 같다.
    drill_long = pd.melt(
    data, id_vars=['Brand', 'Temp'],
    value_vars=[col for col in data.columns if 'Mesurement' in col],
    var_name='Mesurement',
    value_name='mm')
    drill_long.head()
    ^༈ Brand Temp Mesurement mm
    ^༈ 0 A 100 Mesurement 1 25.031768
    ^༈ 1 A 200 Mesurement 1 25.027100
    ^༈ 2 A 300 Mesurement 1 25.024713
    챕터별 연습문제 풀이 | 247
    ^༈ 3 B 100 Mesurement 1 25.018161
    ^༈ 4 B 200 Mesurement 1 25.020642
    • 브랜드별 온도별 평균, 표준편차표
    drill_long['mm'] = pd.to_numeric(drill_long['mm'])
    # Calculate mean and standard deviation grouped by Tool and Temp
    drilling_summary = drill_long.groupby(['Brand', 'Temp'])
    drilling_summary.agg(mean_mm=('mm', 'mean'), sd_mm=('mm', 'std')).reset_index()
    ^༈ Brand Temp mean_mm sd_mm
    ^༈ 0 A 100 25.030796 0.001195
    ^༈ 1 A 200 25.028082 0.000762
    ^༈ 2 A 300 25.025773 0.001013
    ^༈ 3 B 100 25.016513 0.001040
    ^༈ 4 B 200 25.020340 0.000814
    ^༈ 5 B 300 25.015927 0.000888
    ^༈ 6 C 100 25.006082 0.001162
    ^༈ 7 C 200 25.012751 0.001289
    ^༈ 8 C 300 25.009271 0.000939
    ^༈ 9 D 100 25.011982 0.000761
    ^༈ 10 D 200 25.019303 0.000846
    ^༈ 11 D 300 25.014145 0.001145
    ^༈ 12 E 100 24.997342 0.001214
    ^༈ 13 E 200 25.005625 0.001305
    ^༈ 14 E 300 25.000520 0.001012
    2) 브랜드별 온도별로 ANOVA main effect & interaction plot을 그려보세요.
    import matplotlib.pyplot as plt
    import seaborn as sns
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    from statsmodels.graphics.factorplots import interaction_plot
    fig = interaction_plot(
    drill_long['Temp'], drill_long['Brand'], drill_long['mm'],
    colors=['red', 'blue', 'green', 'purple', 'orange'],
    markers=['D', '^', 'o', 's', '*'], ms=10)
    plt.show()
    248 | 챕터별 연습문제 풀이
    11
    100 150 200 250 300
    Temp
    25.00
    25.01
    25.02
    25.03
    mean of mm
    Brand
    A
    B
    C
    D
    E
    3) Two‑way ANOVA 분석을 진행해 주세요.
    Two‑way ANOVA의 경우 3개의 귀무가설이 존재한다.
    • 귀무가설1: Brand 변수의 main effect가 존재하지 않는다.
    • 대립가설1: Brand 변수의 main effect가 존재한다.
    • 귀무가설2: Temp 변수의 main effect가 존재하지 않는다.
    • 대립가설2: Temp 변수의 main effect가 존재한다.
    • 귀무가설3: Brand 변수와 Temp 변수의 interaction이 존재하지 않는다.
    • 대립가설3: Brand 변수와 Temp 변수의 interaction이 존재한다.
    # Conduct two༡way ANOVA
    formula = 'mm ~ C(Brand) + C(Temp) + C(Brand):C(Temp)'
    model = ols(formula, data=drill_long).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    anova_table
    ^༈ sum_sq df F PR(>F)
    ^༈ C(Brand) 0.024130 4.0 5561.567051 4.952237e-269
    ^༈ C(Temp) 0.001299 2.0 598.805667 8.790226e-103
    ^༈ C(Brand):C(Temp) 0.000893 8.0 102.903992 1.874030e-79
    ^༈ Residual 0.000309 285.0 NaN NaN
    ANOVA 테이블을 살펴보면, 각 변수의 main effect에 대한 검정 통계량값인 F값이 5561.6과 598.8
    이 계산되었고, 대응하는 p‑value값이 모두 2e‑16보다 낮아서 유의수준 5%하에서 귀무가설 1과 2가
    기각된다. 따라서, 두 변수의 main effect가 존재한다고 판단한다.
    두 변수의 교호작용을 검정하는 F 값의 경우 역시 102.9가 나왔으며, 대응하는 유의수준 역시 2e‑16
    보다 낮아서 유의수준 5%하에서 귀무가설이 기각된다.
    챕터별 연습문제 풀이 | 249
    따라서, 브랜드별, 온도별 구멍 평균 직경은 다르다고 판단하고, 두 변수의 교호작용에 영향을 받는
    다고 판단한다. 앞에서 작성한 그래프를 참고하면, 브랜드 별 구멍 직경의 차이가 온도가 낮은 경우에
    온도가 중간인 경우에 비하여 좀 더 많이 차이가 나는 것을 확인할 수 있다.
    4) 각 메인 effect가 통계적으로 유의한 경우 사후 분석을 진행해주세요.
    브랜드와 온도 변수에 대하여 각 그룹의 평균 구멍 직경이 다르다고 나왔으므로, 각 변수에 대하여
    사후 분석을 진행한다. 먼저 Brand 변수에 대하여 사후분석을 진행하기 위해 TukeyHSD() 함수를
    사용한다.
    from statsmodels.stats.multicomp import pairwise_tukeyhsd
    posthoc_brand = pairwise_tukeyhsd(drill_long['mm'], drill_long['Brand'])
    print(posthoc_brand.summary())
    ^༈ Multiple Comparison of Means - Tukey HSD, FWER=0.05
    ^༈ ====================================================
    ^༈ group1 group2 meandiff p༡adj lower upper reject
    ^༈ ----------------------------------------------------
    ^༈ A B -0.0106 -0.0 -0.0121 -0.0092 True
    ^༈ A C -0.0188 -0.0 -0.0203 -0.0174 True
    ^༈ A D -0.0131 -0.0 -0.0145 -0.0116 True
    ^༈ A E -0.0271 -0.0 -0.0285 -0.0256 True
    ^༈ B C -0.0082 -0.0 -0.0097 -0.0068 True
    ^༈ B D -0.0024 0.0001 -0.0039 -0.001 True
    ^༈ B E -0.0164 -0.0 -0.0179 -0.015 True
    ^༈ C D 0.0058 -0.0 0.0043 0.0072 True
    ^༈ C E -0.0082 -0.0 -0.0097 -0.0067 True
    ^༈ D E -0.014 -0.0 -0.0154 -0.0125 True
    ^༈ ----------------------------------------------------
    결과를 살펴보면 브랜드 변수의 모든 레벨에 대하여 사후 분석을 진행한 경과, p‑value값이 모두 다
    낮게 나오고, 따라서 통계적으로 유의한 차이를 보인다고 판단할 수 있다.
    posthoc_temp = pairwise_tukeyhsd(drill_long['mm'], drill_long['Temp'])
    print(posthoc_temp.summary())
    ^༈ Multiple Comparison of Means - Tukey HSD, FWER=0.05
    ^༈ ===================================================
    ^༈ group1 group2 meandiff p༡adj lower upper reject
    ^༈ ---------------------------------------------------
    ^༈ 100 200 0.0047 0.0012 0.0016 0.0078 True
    ^༈ 100 300 0.0006 0.8956 -0.0025 0.0037 False
    ^༈ 200 300 -0.0041 0.0054 -0.0072 -0.001 True
    250 | 챕터별 연습문제 풀이
    11
    ^༈ ---------------------------------------------------
    온도 변수 역시 Low, Medium, High 그룹 간 평균 차이가 통계적으로 유의한 차이를 보인다는
    것을 확인할 수 있다. 또한 계산된 diff 값에 비추어보면 Low < High < Medium 순으로 평균 구멍
    직경이 커져간다고 판단 할 수 있다.
    가정체크
    Two way ANONA의 결과를 신뢰하기 위해서는 ANOVA에서 가정하고 있는 잔차의 정규성과 등분
    산성에 대한 검정이 필요하다.
    import scipy.stats as stats
    import pingouin as pg
    # QQ plot
    ax = pg.qqplot(model.resid, dist='norm')
    plt.ylim(-3, 3);
    plt.xlim(-3, 3);
    plt.show()
    잔차의 정규성
    2 0 2
    Theoretical quantiles
    3
    2
    1
    0
    1
    2
    3
    Ordered quantiles
    R
    2 = 0.997
    잔차 그래프를 살펴보면 잔차들이 0을 중심으로 퍼져있고, QQ plot 역시 정규성을 만족하는 것으로
    판단된다. 정확한 검정을 위하여 샤피로 윌크 검정을 사용하여 정규성 체크를 하도록 하자.
    • 귀무가설: 잔차가 정규성을 따른다.
    • 대립가설: 잔차가 정규성을 따르지 않는다.
    stats.shapiro(model.resid)
    ^༈ ShapiroResult(statistic=0.9961785078048706, pvalue=0.6853092312812805)
    챕터별 연습문제 풀이 | 251
    검정 통계량 값 0.996에 대응하는 p‑value값이 0.6852이므로 유의수준 5%하에서 귀무가설을
    기각하지 못한다. 따라서 정규성을 만족한다고 판단한다.
    잔차의 등분산성
    • 귀무가설: 잔차들의 그룹별 모분산이 동일하다.
    • 대립가설: 잔차들의 그룹별 모분산 중 다른 것이 적어도 하나 존재한다.
    # 인터렉션 그룹 만들기
    drill_long['Brand_Temp'] = drill_long['Brand'] + "_" + drill_long['Temp'].astype(str)
    group_vec = drill_long['Brand_Temp']
    levene_test = stats.levene(
    *[model.resid[group_vec ^༰ i] for i in group_vec.unique()], center='mean')
    levene_test
    ^༈ LeveneResult(statistic=1.3624630069062795, pvalue=0.17083426897357204)
    검정통계량 값 1.3625에 대응하는 p‑value 값 0.1708이 유의수준 5%보다 크므로 귀무 가설을
    기각할 수 없다. 따라서, 등분산 가정도 만족한다고 판단한다.
    결과적으로 앞에서 수행한 two way ANOVA 의 결과를 신뢰할 수 있다.
    Chapter 7. 회귀분석의 이해
    펭귄 부리길이와 깊이의 관계
    palmerpenguins 패키지에는 남극 Palmer station에서 관측한 펭귄 정보들이 포함된 데이터이다.
    import pandas as pd
    import numpy as np
    from palmerpenguins import load_penguins
    penguins = load_penguins()
    print(penguins.head())
    ^༈ species island bill_length_mm ^^. body_mass_g sex year
    ^༈ 0 Adelie Torgersen 39.1 ^^. 3750.0 male 2007
    ^༈ 1 Adelie Torgersen 39.5 ^^. 3800.0 female 2007
    ^༈ 2 Adelie Torgersen 40.3 ^^. 3250.0 female 2007
    ^༈ 3 Adelie Torgersen NaN ^^. NaN NaN 2007
    ^༈ 4 Adelie Torgersen 36.7 ^^. 3450.0 female 2007
    ^༈
    ^༈ [5 rows x 8 columns]
    252 | 챕터별 연습문제 풀이
    11
    1) train_index 를 사용하여 펭귄 데이터에서 인덱스에 대응하는 표본들을 뽑아서 train_data를
    만드세요. (단, 결측치가 있는 경우 제거)
    np.random.seed(2022)
    train_index=np.random.choice(penguins.shape[0],200)
    train_data = penguins.iloc[train_index]
    train_data = train_data.dropna()
    train_data.head()
    ^༈ species island bill_length_mm ^^. body_mass_g sex year
    ^༈ 220 Gentoo Biscoe 43.5 ^^. 4700.0 female 2008
    ^༈ 173 Gentoo Biscoe 45.1 ^^. 5000.0 female 2007
    ^༈ 112 Adelie Biscoe 39.7 ^^. 3200.0 female 2009
    ^༈ 177 Gentoo Biscoe 46.1 ^^. 5100.0 male 2007
    ^༈ 240 Gentoo Biscoe 47.5 ^^. 4875.0 female 2009
    ^༈
    ^༈ [5 rows x 8 columns]
    2) train_data의 펭귄 부리길이 (bill_length_mm)를 부리 깊이 (bill_depth_mm)를 사용하여
    산점도를 그려보세요.
    import matplotlib.pyplot as plt
    import seaborn as sns
    # Scatter plot using seaborn
    plt.figure(figsize=(10,6))
    ^༈ <Figure size 1000x600 with 0 Axes>
    sns.scatterplot(data=train_data,
    x='bill_length_mm',
    y='bill_depth_mm',
    hue='species',
    palette='deep', edgecolor='w', s=50)
    ^༈ <AxesSubplot:xlabel='bill_length_mm', ylabel='bill_depth_mm'>
    plt.title('Bill Length vs Bill Depth by Species')
    ^༈ Text(0.5, 1.0, 'Bill Length vs Bill Depth by Species')
    챕터별 연습문제 풀이 | 253
    plt.grid(True)
    plt.show()
    35 40 45 50 55
    bill_length_mm
    13
    14
    15
    16
    17
    18
    19
    20
    21
    bill_depth_mm
    Bill Length vs Bill Depth by Species
    species
    Gentoo
    Adelie
    Chinstrap
    3) 펭귄 부리길이 (bill_length_mm)를 부리 깊이 (bill_depth_mm)의 상관계수를 구하고, 두
    변수 사이에 유의미한 상관성이 존재하는지 검정해보세요.
    • 귀무가설 𝐻0
    : 두 변수의 상관계수 𝜌 = 0
    • 대립가설 𝐻𝐴: 두 변수의 상관계수 𝜌 ≠ 0
    두 변수의 상관계수 검정은 pearsonr() 함수를 사용하여 수행할 수 있다.
    from scipy.stats import pearsonr
    # Calculate the Pearson correlation coefficient
    # and the p༡value for testing non༡correlation
    corr_coef, p_value = pearsonr(train_data['bill_length_mm'], train_data['bill_depth_mm'])
    print(corr_coef)
    ^༈ -0.24938519717051547
    print(p_value)
    ^༈ 0.00040929638362032476
    유의수준 5%하에서 상관계수 값 ‑0.2493에 해당하는 p‑value 값 0.000409296이 상당히 작으므로,
    귀무가설을 기각한다. 따라서, 두 변수의 상관계수가 0이 아니라는 통계적 근거가 충분하다.
    위의 검정 결과를 신뢰 할 수 있는지 확인하기 위하여, 상관관계 분석에서 가정하고 있는 정규성을
    체크해보도록 하자.
    import statsmodels.api as sm
    import matplotlib.pyplot as plt
    import pingouin as pg
    254 | 챕터별 연습문제 풀이
    11
    # Set up the subplots: 1 row, 2 columns
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    # Q-Q plot for bill_depth_mm on the left
    pg.qqplot(train_data['bill_depth_mm'], dist='norm', confidence=0.95, ax=axs[0])
    ^༈ <AxesSubplot:xlabel='Theoretical quantiles', ylabel='Ordered quantiles'>
    axs[0].set_title("bill_depth_mm")
    ^༈ Text(0.5, 1.0, 'bill_depth_mm')
    axs[0].set_ylim(-3, 3);
    axs[0].set_xlim(-3, 3);
    # Q-Q plot for bill_length_mm on the right
    ^༈ (-3.0, 3.0)
    pg.qqplot(train_data['bill_length_mm'], dist='norm', confidence=0.95, ax=axs[1])
    ^༈ <AxesSubplot:xlabel='Theoretical quantiles', ylabel='Ordered quantiles'>
    axs[1].set_title("bill_length_mm")
    ^༈ Text(0.5, 1.0, 'bill_length_mm')
    axs[1].set_ylim(-3, 3);
    axs[1].set_xlim(-3, 3);
    # Display the plots
    ^༈ (-3.0, 3.0)
    plt.tight_layout()
    plt.show()
    챕터별 연습문제 풀이 | 255
    3 2 1 0 1 2 3
    Theoretical quantiles
    3
    2
    1
    0
    1
    2
    3
    Ordered quantiles
    R
    2 = 0.966
    bill_depth_mm
    3 2 1 0 1 2 3
    Theoretical quantiles
    3
    2
    1
    0
    1
    2
    3
    Ordered quantiles
    R
    2 = 0.967
    bill_length_mm
    각 변수에 해당하는 QQ plot을 그려 보았을 때, 부리 길이 (bill length) 변수와 부리 깊이 (bill
    depth) 변수에 해당하는 그래프는 정규성을 띄지 않는 것을 알 수 있다. Shapiro‑Wilk 검정 결과
    역시 두 그룹 표본이 정규성 가정을 위반한 다는 것을 말해주고 있다.
    Shapiro‑Wilk 검정
    • 귀무가설 𝐻0
    : 데이터의 분포가 정규성을 띈다.
    • 대립가설 𝐻𝐴: 데이터의 분포가 정규성을 띄지 못한다.
    import scipy.stats as sp
    sp.shapiro(train_data['bill_depth_mm'])
    ^༈ ShapiroResult(statistic=0.9621433019638062, pvalue=3.906726124114357e-05)
    sp.shapiro(train_data['bill_length_mm'])
    ^༈ ShapiroResult(statistic=0.9634734988212585, pvalue=5.4907886806176975e-05)
    즉, 유의수준 5%하에서 두 변수 모두 귀무가설을 기각하게 되므로, 위의 상관계수 검정 결과는
    신뢰할 수 없다.
    4) 펭귄 부리길이 (bill_length_mm)를 부리 깊이 (bill_depth_mm)를 사용하여 설명하는 회귀
    모델을 적합시킨 후 2번의 산점도에 회귀 직선을 나타내 보세요. (모델 1)
    from statsmodels.formula.api import ols
    model1 = ols("bill_length_mm ~ bill_depth_mm", data=train_data).fit()
    model1.params
    ^༈ Intercept 55.410976
    ^༈ bill_depth_mm -0.706191
    ^༈ dtype: float64
    256 | 챕터별 연습문제 풀이
    11
    sns.scatterplot(data=train_data,
    x='bill_depth_mm', y='bill_length_mm',
    palette='deep', edgecolor='w', s=50)
    # Use the slope and intercept to plot the regression line
    ^༈ <AxesSubplot:xlabel='bill_depth_mm', ylabel='bill_length_mm'>
    x_values = train_data['bill_depth_mm']
    y_values = 55.4110 - 0.7062 * x_values
    plt.plot(x_values, y_values, color='red', label='Regression Line')
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA622F708>]
    plt.title('Scatter plot of Bill Length vs Bill Depth with Regression Line')
    ^༈ Text(0.5, 1.0, 'Scatter plot of Bill Length vs Bill Depth with Regression Line')
    plt.grid(True)
    plt.legend()
    ^༈ <matplotlib.legend.Legend object at 0x000001ABA77E6F88>
    plt.show()
    14 16 18 20
    bill_depth_mm
    35
    40
    45
    50
    55
    bill_length_mm
    Scatter plot of Bill Length vs Bill Depth with Regression Line
    Regression Line
    5) 적합된 회귀 모델이 통계적으로 유의한지 판단해보세요.
    부리 깊이 변수를 사용하여 부리 길이 변수를 설명하는 회귀 모델을 설정한다.
    챕터별 연습문제 풀이 | 257
    model1.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: bill_length_mm R༡squared: 0.062
    ^༈ Model: OLS Adj. R༡squared: 0.057
    ^༈ Method: Least Squares F༡statistic: 12.93
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 0.000409
    ^༈ Time: 14:03:42 Log-Likelihood: -602.49
    ^༈ No. Observations: 197 AIC: 1209.
    ^༈ Df Residuals: 195 BIC: 1216.
    ^༈ Df Model: 1
    ^༈ Covariance Type: nonrobust
    ^༈ =================================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ ---------------------------------------------------------------------------------
    ^༈ Intercept 55.4110 3.392 16.336 0.000 48.721 62.101
    ^༈ bill_depth_mm -0.7062 0.196 -3.596 0.000 -1.093 -0.319
    ^༈ ==============================================================================
    ^༈ Omnibus: 4.987 Durbin-Watson: 1.786
    ^༈ Prob(Omnibus): 0.083 Jarque-Bera (JB): 3.609
    ^༈ Skew: 0.193 Prob(JB): 0.165
    ^༈ Kurtosis: 2.461 Cond. No. 159.
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ ""
    유의수준 5%하에서 F 검정 통계량 값 12.93에 대응하는 p‑value값 0.000409에 비추어 보았을 때,
    회귀 모델은 통계적으로 유의한 것으로 판단한다.
    6) 𝑅2 값을 구한 후 의미를 해석해 보세요.
    위의 결과값에서 R square 값은 0.062이며, 이는 회귀모델이 데이터 전체 변동성의 6.21%를 설
    명하고 있다는 의미이다. 상대적으로 낮은 R square 값을 미루어 보았을때, 추가 변수를 사용하여
    모델의 설명력을 높이는 것을 고려할 수 있다.
    7) 적합된 회귀 모델의 계수를 해석해 보세요.
    • 절편과 기울기가 모두 유의하게 나오지만, 각 변수의 뜻을 고려하면, 절편의 해석은 무의미하다.
    (부리 깊이 0인 경우, 부리 길이 56 mm)
    258 | 챕터별 연습문제 풀이
    11
    • 기울기 ‑0.7062 값의 의미는, 팔머 펭귀의 경우 부리 깊이가 1 mm 증가할 때, 부리 길이는
    0.7062 mm 만큰 감소하는 경향을 보인다고 해석할 수 있다.
    8) 1번에서 적합한 회귀 모델에 새로운 변수 (종 ‑ species) 변수를 추가하려고 합니다. 성별 변수
    정보를 사용하여 점 색깔을 다르게 시각화 한 후 적합된 모델의 회귀 직선을 시각화 해보세요.
    (모델 2)
    model2 = ols("bill_length_mm ~ bill_depth_mm + species", data=train_data).fit()
    model2.params
    # Set up the plot
    ^༈ Intercept 14.577564
    ^༈ species[T.Chinstrap] 9.886486
    ^༈ species[T.Gentoo] 12.912783
    ^༈ bill_depth_mm 1.320354
    ^༈ dtype: float64
    sns.scatterplot(data=train_data,
    x='bill_depth_mm', y='bill_length_mm',
    hue='species', palette='deep', edgecolor='w', s=50)
    # Generate regression lines for each species
    ^༈ <AxesSubplot:xlabel='bill_depth_mm', ylabel='bill_length_mm'>
    for species in train_data['species'].unique():
    # Filter data by species
    subset = train_data[train_data['species'] ^༰ species]
    # Predict values using the regression model
    x_vals = subset['bill_depth_mm'].sort_values()
    y_vals = model2.predict(pd.DataFrame({'bill_depth_mm': x_vals, 'species': species}))
    # Plot regression line for this species
    sns.lineplot(x=x_vals, y=y_vals, label=f'Regression Line ({species})')
    ^༈ <AxesSubplot:xlabel='bill_depth_mm', ylabel='bill_length_mm'>
    ^༈ <AxesSubplot:xlabel='bill_depth_mm', ylabel='bill_length_mm'>
    ^༈ <AxesSubplot:xlabel='bill_depth_mm', ylabel='bill_length_mm'>
    챕터별 연습문제 풀이 | 259
    plt.title('Scatter plot of Bill Depth vs Bill Length with Regression Lines by Species')
    ^༈ Text(0.5, 1.0, 'Scatter plot of Bill Depth vs Bill Length with Regression Lines ↩
    by Species')
    plt.grid(True)
    plt.legend()
    ^༈ <matplotlib.legend.Legend object at 0x000001AB97FCD488>
    plt.show()
    14 16 18 20
    bill_depth_mm
    35
    40
    45
    50
    55
    bill_length_mm
    Scatter plot of Bill Depth vs Bill Length with Regression Lines by Species
    Gentoo
    Adelie
    Chinstrap
    Regression Line (Gentoo)
    Regression Line (Adelie)
    Regression Line (Chinstrap)
    결과를 살펴보면, 종 (species) 변수를 추가하므로써 회귀직선의 방향이 바뀌었다. 또한, 전체적인
    데이터의 추세를 회귀 직선이 더 잘 설명하고 있는 것을 볼 수 있다. 이러한 현상을 심슨’s 패러독스라고
    부른다.
    9) 종 변수가 새로 추가된 모델 2가 모델 1 보다 더 좋은 모델이라는 근거를 제시하세요.
    table = sm.stats.anova_lm(model1, model2) #anova
    print(table)
    ^༈ df_resid ssr df_diff ss_diff F Pr(>F)
    ^༈ 0 195.0 5228.862451 0.0 NaN NaN NaN
    ^༈ 1 193.0 1044.226281 2.0 4184.63617 386.714449 3.071739e-68
    모델 2는 모델 1을 포함하는 Full 모델과 Reduced 모델로 볼 수 있다. 두 모델 사이의 통계적 유의
    성을 F 검정을 통하여 보일 수 있다.
    • 귀무가설 𝐻0
    : Reduced 모델이 알맞음.
    • 대립가설 𝐻𝐴: Full 모델이 알맞음.
    260 | 챕터별 연습문제 풀이
    11
    위의 ANOVA 코드의 결과에서 F 검정 통계량 386.71에 대응하는 p‑value값 3.07e‑68이 유의수준
    5% 하에서 귀무가설을 기각할 수 있으므로, 모델 1 보다 모델 2가 더 알맞은 모델이라 판단한다.
    10) 모델 2의 계수에 대한 검정과 그 의미를 해석해 보세요.
    model2.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: bill_length_mm R༡squared: 0.813
    ^༈ Model: OLS Adj. R༡squared: 0.810
    ^༈ Method: Least Squares F༡statistic: 279.2
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 6.28e-70
    ^༈ Time: 14:03:46 Log-Likelihood: -443.81
    ^༈ No. Observations: 197 AIC: 895.6
    ^༈ Df Residuals: 193 BIC: 908.8
    ^༈ Df Model: 3
    ^༈ Covariance Type: nonrobust
    ^༈ ↩
    ========================================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ ↩
    ----------------------------------------------------------------------------------------
    ^༈ Intercept 14.5776 2.855 5.107 0.000 8.947 20.208
    ^༈ species[T.Chinstrap] 9.8865 0.446 22.159 0.000 9.007 10.766
    ^༈ species[T.Gentoo] 12.9128 0.638 20.243 0.000 11.655 14.171
    ^༈ bill_depth_mm 1.3204 0.156 8.448 0.000 1.012 1.629
    ^༈ ==============================================================================
    ^༈ Omnibus: 0.570 Durbin-Watson: 2.084
    ^༈ Prob(Omnibus): 0.752 Jarque-Bera (JB): 0.322
    ^༈ Skew: -0.074 Prob(JB): 0.851
    ^༈ Kurtosis: 3.132 Cond. No. 304.
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ ""
    회귀분석의 결과 모형이 통계적으로 유의미하고, 모든 계수 역시 통계적으로 유의한 것을 확인할 수
    있다.
    챕터별 연습문제 풀이 | 261
    • 부리 깊이에 대응하는 계수는 1.3204로, 의미는 부리깊이 1mm가 증가하면, 부리길이가
    1.3204mm가 증가하는 경향성을 보인다고 해석할 수 있다.
    • 기준 레벨이 되는 아델리 펭귄 종의 부리깊이에 따른 부리길이 추세는 14.5776 + 1.3204 ×
    𝑏𝑖𝑙𝑙𝑑
    𝑒𝑝𝑡ℎ를 따른다.
    • species[T.Chinstrap] 변수의 계수 9.8865, species[T.Gentoo] 변수의 계수 12.9128에서 친
    스트랩 펭귄 종은 아델리 펭귄 종보다 평균적으로 약 9.88mm, 겐투 펭귄 종은 아델리 펭귄
    종보다 평균적으로 약 12.91mm 가 긴 경향성을 보인다고 해석할 수 있다.
    11) 모델 2 에 잔차 그래프를 그리고, 회귀모델 가정을 만족하는지 검증을 수행해주세요.
    import scipy.stats as stats
    # Set up the subplots: 1 row, 2 columns
    residuals = model2.resid
    fitted_values = model2.fittedvalues
    plt.figure(figsize=(16,8))
    ^༈ <Figure size 1600x800 with 0 Axes>
    plt.subplot(1,2,1)
    ^༈ <AxesSubplot:>
    plt.scatter(fitted_values, residuals);
    plt.subplot(1,2,2)
    ^༈ <AxesSubplot:>
    pg.qqplot(residuals, dist='norm', confidence=0.95);
    # Display the plots
    ^༈ <AxesSubplot:xlabel='Theoretical quantiles', ylabel='Ordered quantiles'>
    plt.tight_layout()
    plt.show()
    262 | 챕터별 연습문제 풀이
    11
    36 38 40 42 44 46 48 50 52
    8
    6
    4
    2
    0
    2
    4
    6
    2 1 0 1 2
    Theoretical quantiles
    2
    1
    0
    1
    2
    Ordered quantiles
    R
    2 = 0.991
    잔차 그래프와 잔차의 QQ plot 그래프로 보아 잔차의 등분산성과 정규성을 만족하는 것으로 판단
    된다.
    from scipy.stats import shapiro
    from statsmodels.stats.diagnostic import het_breuschpagan
    from statsmodels.stats.stattools import durbin_watson
    shapiro(residuals)
    ^༈ ShapiroResult(statistic=0.9919706583023071, pvalue=0.35017824172973633)
    durbin_watson(residuals)
    ^༈ 2.083836063916197
    labels = ['Lagrange multiplier statistic', 'p༡value', 'f༡value', 'f p༡value']
    bp_test = het_breuschpagan(residuals, model2.model.exog)
    bp_result = dict(zip(labels, bp_test))
    bp_result
    ^༈ {'Lagrange multiplier statistic': 12.575027525429496, 'p༡value': ↩
    0.005651859166962036, 'f༡value': 4.3865720927834015, 'f p༡value': 0.005177711883822766}
    유의수준 5%하에서 잔차 정규성을 검정하는 Shapiro‑Wilk 검정, 잔차의 등분산성을 검정하는
    Breusch–Pagan 검정, 잔차의 독립성을 검정하는 Durbin‑Watson 검정의 결과가 회귀모델의 가정
    을 만족하는 것을 확인할 수 있다.
    Durbin‑Watson 통계량의 값은 0에서 4 사이에 있으며, 2 근처의 값은 잔차 간에 상관관계가 없음을
    나타냅니다. 값이 2보다 크면 음의 상관관계, 2보다 작으면 양의 상관관계가 있을 가능성이 있습니다.
    12) 모델 2 의 잔차를 통하여 영향점, 혹은 이상치의 유무를 판단해보세요.
    챕터별 연습문제 풀이 | 263
    influence = model2.get_influence()
    stud_res = influence.resid_studentized_external
    # 2. Identify observations with studentized residuals
    # greater than 3 in absolute value
    outliers = np.where(np.abs(stud_res) > 3)[0]
    # 3. Retrieve these rows from train_data
    outlier_data = train_data.iloc[outliers]
    outlier_data["bill_depth_mm"]
    ^༈ 14 21.1
    ^༈ Name: bill_depth_mm, dtype: float64
    outlier_data["bill_length_mm"]
    ^༈ 14 34.6
    ^༈ Name: bill_length_mm, dtype: float64
    print(outlier_data)
    ^༈ species island bill_length_mm ^^. body_mass_g sex year
    ^༈ 14 Adelie Torgersen 34.6 ^^. 4400.0 male 2007
    ^༈
    ^༈ [1 rows x 8 columns]
    스튜던트화 잔차를 기준으로 3 표준편차 밖으로 벗어나 있는 표본은 위와 같다. Adelie 표본의 경우
    비슷한 부리 깊이의 표본들과는 너무 많은 차이를 보이므로 이상치로 판단한다.
    """