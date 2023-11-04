def s7():
    """
    제 7 장
    회귀분석의 이해
    7.1 단순 선형회귀 (Simple linear regression)
    데이터를 나타내는 기호들
    • 반응변수 𝑦𝑖
    , 𝑖 = 1, ..., 𝑛
    • 독립변수 𝑥𝑖
    , 𝑖 = 1, ..., 𝑛
    • 잡음변수 𝑒𝑖
    , 𝑖 = 1, ..., 𝑛
    y =
    ⎛⎜⎜⎜⎜⎜
    ⎝
    𝑦1
    𝑦2
    ...
    𝑦𝑛
    ⎞⎟⎟⎟⎟⎟
    ⎠
    , 𝑋𝛽 =
    ⎛⎜⎜⎜⎜⎜⎜⎜
    ⎝
    1 𝑥1
    1 𝑥2
    ... ...
    1 𝑥𝑛−1
    1 𝑥𝑛
    ⎞⎟⎟⎟⎟⎟⎟⎟
    ⎠
    (
    𝛽0
    𝛽1
    ) , 𝑒 = ⎛⎜⎜⎜⎜⎜
    ⎝
    𝑒1
    𝑒2
    ...
    𝑒𝑛
    ⎞⎟⎟⎟⎟⎟
    ⎠
    모델 가정
    반응변수의 관찰값들은 다음과 같은 모델을 통해서 발생되었다고 가정한다.
    𝑦 ∼ 𝒩(𝑋𝛽, 𝜎2
    𝐼)
    • 관찰값 𝑦𝑖은 독립변수 𝑥𝑖와 잡음 𝑒𝑖의 선형결합으로 이루어져있다.
    𝑦𝑖 = 𝛽0 + 𝛽1𝑥𝑖 + 𝑒𝑖
    , 𝑖 = 1, ..., 𝑛
    • 잡음 𝑒𝑖들의 분포는 평균이 0이고 분산이 𝜎
    2인 독립인 정규분포를 따른다고 가정
    • 원래 잡음 분포에 대한 가정이 없었으나, 추후에 추가 됨.
    Best fitting line
    𝛽 = (𝑋 ̂ 𝑇 𝑋)−1 𝑋𝑇 𝑦
    회귀분석 계수 추정을 하는 방법은 다음의 슬기로운 통계생활 영상을 참고하자.
    회귀분석의 이해 | 139
    • 영상1
    • 영상2
    # 파이썬 코드
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.datasets import load_iris
    iris = load_iris()
    iris = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    iris.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width'] #컬럼명 변경시
    x = iris['Petal_Width']
    y = iris['Petal_Length']
    data_X = np.column_stack((np.ones(len(x)), x))
    beta = np.linalg.solve(np.dot(data_X.T, data_X), np.dot(data_X.T, y))
    plt.scatter(x, y, color='blue')
    ^༈ <matplotlib.collections.PathCollection object at 0x000001AB9878D248>
    plt.xlabel("Width")
    ^༈ Text(0.5, 0, 'Width')
    plt.ylabel("Length")
    ^༈ Text(0, 0.5, 'Length')
    plt.axhline(y=np.mean(y), color='blue', linestyle='-')
    ^༈ <matplotlib.lines.Line2D object at 0x000001ABA23EB508>
    plt.plot(x, np.dot(data_X, beta), color='red', linestyle='-')
    ^༈ [<matplotlib.lines.Line2D object at 0x000001ABA23EB448>]
    140 | 회귀분석의 이해
    7
    plt.show()
    0.0 0.5 1.0 1.5 2.0 2.5
    Width
    1
    2
    3
    4
    5
    6
    7
    Length
    • 파란색 선의 의미: 독립변수 𝑋의 정보가 없었다면 반응 변수 𝑦에 대한 최적 추정치는 𝑦의 표본
    평균을 사용해서 예측
    • 빨간색 선의 의미: 독립변수 𝑋의 정보가 추가된 최적의 예측 직선
    파이썬에서 회귀분석
    from statsmodels.formula.api import ols
    model = ols("Petal_Length ~ Petal_Width", data=iris).fit()
    model.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: Petal_Length R༡squared: 0.927
    ^༈ Model: OLS Adj. R༡squared: 0.927
    ^༈ Method: Least Squares F༡statistic: 1882.
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 4.68e-86
    ^༈ Time: 14:01:32 Log-Likelihood: -101.18
    ^༈ No. Observations: 150 AIC: 206.4
    ^༈ Df Residuals: 148 BIC: 212.4
    ^༈ Df Model: 1
    ^༈ Covariance Type: nonrobust
    ^༈ ===============================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    단순 선형회귀 (Simple linear regression) | 141
    ^༈ -------------------------------------------------------------------------------
    ^༈ Intercept 1.0836 0.073 14.850 0.000 0.939 1.228
    ^༈ Petal_Width 2.2299 0.051 43.387 0.000 2.128 2.332
    ^༈ ==============================================================================
    ^༈ Omnibus: 2.438 Durbin-Watson: 1.430
    ^༈ Prob(Omnibus): 0.295 Jarque-Bera (JB): 1.966
    ^༈ Skew: 0.211 Prob(JB): 0.374
    ^༈ Kurtosis: 3.369 Cond. No. 3.70
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ ""
    계수에 따른 모델식
    𝑃 𝑒𝑡𝑎𝑙 𝐿𝑒𝑛𝑔𝑡ℎ = 1.08356 + 2.22994 × 𝑃 𝑒𝑡𝑎𝑙 𝑊𝑖𝑑𝑡ℎ
    회귀분석의 효용성 측정 지표들
    SST, SSM, and SSE
    붓꽃의 꽃잎 길이 아무런 추가 정보가 없을 경우 평균 ( ̄𝑦 ) 으로 예측할 것이다. 이렇게 반응변수 평균값
    ( ̄𝑦 ) 에서 각 관측치들까지의 변동성의 제곱합은 다음과 같이 분해 할 수 있음.
    142 | 회귀분석의 이해
    7
    𝑆𝑆𝑇 = 𝑆𝑆𝑅 + 𝑆𝑆𝐸
    • 관측치들의 편차 제곱합 (SST): ∑(𝑦𝑖 − ̄𝑦)2
    – 붓꽃의 꽃잎 너비 정보( 𝑋1
    )를 사용하여 회귀모델을 수립하여 예측 ( ̂𝑦𝑖
    )
    • 예측치의 오차들의 제곱합(SSE): ∑(𝑦𝑖 − ̂𝑦𝑖
    )
    2
    • 향상된 예측력들의 제곱합(SSR): ∑( ̂𝑦𝑖 − ̄𝑦)2
    – 회귀모델을 사용 예측함으로서 향상된 예측력 ( ̂𝑦𝑖 − ̄𝑦 )
    7.2 회귀분석 ANOVA
    귀무가설 vs. 대립가설
    • 𝐻0
    : 모든 회귀계수들이 0이다. 𝛽1 = 0
    • 𝐻𝐴: 0이 아닌 회귀계수가 존재한다. 𝛽1 ≠ 0
    검정통계량
    𝐹 = 𝑆𝑆𝑅/1
    𝑆𝑆𝐸/(𝑛 − 2) ∼ 𝐹1,𝑛−2
    • ANOVA에서 그룹별 평균이 다르다고 결론 내리는 논리와 동일함.
    • 회귀분석을 통해서 향상된 예측 효과 (분자 부분)가 모델의 잡음보다 훨씬 크다면, 회귀분석
    모델의 효과가 통계적으로 의미가 있다고 판단한다.
    • 독립변수를 고려하는 것이 정말 효과가 있는지를 검정한다.
    • 설명력이 많이 좋아졌는지를 체크!
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    model = ols("Petal_Length ~ Petal_Width", data=iris).fit()
    sm.stats.anova_lm(model)
    ^༈ df sum_sq mean_sq F PR(>F)
    ^༈ Petal_Width 1.0 430.480647 430.480647 1882.452368 4.675004e-86
    ^༈ Residual 148.0 33.844753 0.228681 NaN NaN
    • 유의수준 5% 하에서 F value (1882.5)와 대응하는 p‑value 2.2−16을 고려할 때, 너무 작으므
    로, 귀무가설을 기각한다.
    회귀분석 ANOVA | 143
    알아두면 좋은 분포 정보
    자유도가 𝑎인 𝑡 분포를 따르는 확률변수를 제곱하면 자유도가 1, 𝑎인 F 분포를 따르게 된다.
    (𝑡𝑛−2)
    2 = 𝐹1,𝑛−2
    회귀분석의 성능측정 지표 ‑ 𝑅2 vs. adjusted 𝑅2
    𝑅2
    ‑ 회귀 직선의 성능은 얼마나 좋아?
    • 회귀직선으로 인하여 향상된 예측력이 전체 관측치 변동성에서 차지하는 비율
    𝑅2 =
    𝑆𝑆𝑅
    𝑆𝑆𝑇 = 1 −
    𝑆𝑆𝐸
    𝑆𝑆𝑇
    • 𝑅2 해석: 𝑅2 만큼의 데이터 변동성이 독립변수에 의하여 설명됨
    • 주의: Adjusted 𝑅2는 𝑅2처럼 해석하면 안 됨.
    Adjusted 𝑅2
    ‑ 모델 복잡도를 고려한 지표
    • 모델에 들어있는 독립 변수 갯수 𝑝 가 많아지면 𝑅2은 항상 높아지는 경향을 보인다.
    • 변수 갯수가 다른 모델간 적합도를 비교하려 한다면 adjusted 𝑅2를 사용하여 비교한다.
    𝑅2
    𝑎 = 1 −
    𝑆𝑆𝐸/(𝑛 − 𝑝 − 1)
    𝑆𝑆𝑇 /(𝑛 − 1) = 1 −
    𝑛 − 1
    𝑛 − 𝑝 − 1
    (1 − 𝑅2
    )
    𝑅2에 대한 오해
    • 단순선형회귀에서만 𝑅2와 표본 상관계수 𝑟이 같음.
    𝑟𝑥𝑦 =
    1
    𝑛 − 1
    𝑛
    ∑
    𝑖=1
    (
    𝑥𝑖 − ̄𝑥
    𝑠𝑥
    ) (𝑦𝑖 − ̄𝑦
    𝑠𝑦
    )
    • 𝑅2 값만을 가지고 판단할 수 없는 이유 (잔차 그래프)
    • 𝑅2 값은 선형적인 모델이 데이터 변동성에 대하여 얼마나 설명력을 가지고 있는가를 나타낸다.
    • 𝑅2 값이 높다는 것이 항상 회귀분석 모델이 데이터에 잘 적합 (fitting) 되어 있다는 의미가
    아니다.
    회귀모델 잡음의 분산 (Regression standard error)
    다음 중 어느 회귀 직선의 예측값이 더 정확할까?
    • 잡음을 발생시키는 분포의 분산 (𝜎
    2
    )을 다음의 값을 통하여 추정한다.
    ̂𝜎
    2 = 𝑀𝑆𝐸 = ∑ (𝑦𝑖 − ̂𝑦𝑖
    )
    2
    𝑛 − 𝑝 − 1
    144 | 회귀분석의 이해
    7
    7.3 다중 선형회귀 (Multiple linear regression)
    단순 선형 회귀분석에서 독립변수의 숫자가 𝑝개로 늘어난 모형이다.
    • 기본 가정은 동일함.
    𝑦𝑖 = 𝛽0 + 𝛽1𝑥𝑖1 + ... + 𝛽𝑝𝑥𝑖𝑝 + 𝑒𝑖
    , 𝑖 = 1, ..., 𝑛
    위의 형태를 다음과 같이 벡터 형태로 표현 할 수 있음.
    𝑦𝑖 = x
    𝑇
    𝑖 𝛽 + 𝑒𝑖
    , 𝑖 = 1, ..., 𝑛
    𝑋 =
    ⎡
    ⎢
    ⎢
    ⎣
    1 𝑥11 … 𝑥1𝑝
    1 𝑥21 … 𝑥2𝑝
    ⋮ ⋮ ⋮ ⋮
    1 𝑥𝑛1 … 𝑥𝑛𝑝
    ⎤
    ⎥
    ⎥
    ⎦
    𝛽 = ⎛⎜⎜
    ⎝
    𝛽1
    ...
    𝛽𝑝
    ⎞⎟⎟
    ⎠
    다중 선형회귀 (Multiple linear regression) | 145
    R에서 다중회귀분석 실행하기
    꽃잎의 길이를 세가지 독립변수들 (꽃잎 너비, 꽃받침 길이와 너비)을 사용하여 설명하는 회귀분석
    모델을 만들어보자.
    model2 = ols("Petal_Length ~ Petal_Width + Sepal_Length + Sepal_Width",
    data=iris).fit()
    model2.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: Petal_Length R༡squared: 0.968
    ^༈ Model: OLS Adj. R༡squared: 0.967
    ^༈ Method: Least Squares F༡statistic: 1473.
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 6.98e-109
    ^༈ Time: 14:01:33 Log-Likelihood: -39.408
    ^༈ No. Observations: 150 AIC: 86.82
    ^༈ Df Residuals: 146 BIC: 98.86
    ^༈ Df Model: 3
    ^༈ Covariance Type: nonrobust
    ^༈ ================================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ --------------------------------------------------------------------------------
    ^༈ Intercept -0.2627 0.297 -0.883 0.379 -0.850 0.325
    ^༈ Petal_Width 1.4468 0.068 21.399 0.000 1.313 1.580
    ^༈ Sepal_Length 0.7291 0.058 12.502 0.000 0.614 0.844
    ^༈ Sepal_Width -0.6460 0.068 -9.431 0.000 -0.781 -0.511
    ^༈ ==============================================================================
    ^༈ Omnibus: 2.520 Durbin-Watson: 1.783
    ^༈ Prob(Omnibus): 0.284 Jarque-Bera (JB): 2.391
    ^༈ Skew: 0.073 Prob(JB): 0.303
    ^༈ Kurtosis: 3.601 Cond. No. 79.3
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ ""
    146 | 회귀분석의 이해
    7
    모델 비교하기 ‑ Model 1 vs. Model 2
    독립변수 2개 추가 효용성이 있는지를 검정해보자.
    • 모델 1: 독립변수 1개 ‑ Petal.Width
    • 모델 2: 독립변수 3개 ‑ Petal.Width + Sepal.Length + Sepal.Width
    귀무가설 vs. 대립가설
    𝐻0
    : Reduced Model이 알맞음.
    𝐻𝐴: Full Model이 알맞음.
    Full model vs. Reduced model
    • 같은 구조를 가지고 있는 모델 중 한 모델이 다른 모델을 포함하는 형식의 2 모델을 비교
    – Full model: Petal.Width + Sepal.Length + Sepal.Width
    – Reduced model: Petal.Width
    F‑검정
    • 두 모델의 오차제곱합 차이를 비교
    𝐹 = [(𝑆𝑆𝐸 (𝑅𝑀)) − 𝑆𝑆𝐸 (𝐹𝑀)] / (𝑝 + 1 − 𝑘)
    𝑆𝑆𝐸 (𝐹𝑀) / (𝑛 − 𝑝 − 1) ∼ 𝐹(𝑝+1−𝑘,𝑛−𝑝−1)
    • Full 모델의 독립변수 갯수 𝑝
    • Reduced 모델의 모수 갯수 (Intercept 포함) 𝑘
    # 파이썬 코드
    import statsmodels.api as sm
    from statsmodels.formula.api import ols
    model1 = ols('Petal_Length ~ Petal_Width', data=iris).fit() #mod1
    model2 = ols('Petal_Length ~ Petal_Width + Sepal_Length + Sepal_Width',
    data=iris).fit() #mod2
    table = sm.stats.anova_lm(model1, model2) #anova
    print(table)
    ^༈ df_resid ssr df_diff ss_diff F Pr(>F)
    ^༈ 0 148.0 33.844753 0.0 NaN NaN NaN
    ^༈ 1 146.0 14.852948 2.0 18.991805 93.341859 7.752746e-27
    F 검정 통계량과 p‑value로 미루어보아 귀무가설을 기각할 수 있으며, Full model을 선택할 수
    있음.
    다중 선형회귀 (Multiple linear regression) | 147
    model2.summary()
    ^༈ <class 'statsmodels.iolib.summary.Summary'>
    ^༈ ""
    ^༈ OLS Regression Results
    ^༈ ==============================================================================
    ^༈ Dep. Variable: Petal_Length R༡squared: 0.968
    ^༈ Model: OLS Adj. R༡squared: 0.967
    ^༈ Method: Least Squares F༡statistic: 1473.
    ^༈ Date: 토, 28 10 2023 Prob (F༡statistic): 6.98e-109
    ^༈ Time: 14:01:35 Log-Likelihood: -39.408
    ^༈ No. Observations: 150 AIC: 86.82
    ^༈ Df Residuals: 146 BIC: 98.86
    ^༈ Df Model: 3
    ^༈ Covariance Type: nonrobust
    ^༈ ================================================================================
    ^༈ coef std err t P>|t| [0.025 0.975]
    ^༈ --------------------------------------------------------------------------------
    ^༈ Intercept -0.2627 0.297 -0.883 0.379 -0.850 0.325
    ^༈ Petal_Width 1.4468 0.068 21.399 0.000 1.313 1.580
    ^༈ Sepal_Length 0.7291 0.058 12.502 0.000 0.614 0.844
    ^༈ Sepal_Width -0.6460 0.068 -9.431 0.000 -0.781 -0.511
    ^༈ ==============================================================================
    ^༈ Omnibus: 2.520 Durbin-Watson: 1.783
    ^༈ Prob(Omnibus): 0.284 Jarque-Bera (JB): 2.391
    ^༈ Skew: 0.073 Prob(JB): 0.303
    ^༈ Kurtosis: 3.601 Cond. No. 79.3
    ^༈ ==============================================================================
    ^༈
    ^༈ Notes:
    ^༈ [1] Standard Errors assume that the covariance matrix of the errors is correctly ↩
    specified.
    ^༈ ""
    각 독립변수들의 계수들이 0이 아닌 값을 갖는 것이 통계적으로 유의하다고 판단할 수 있음.
    모델 진단하기
    1변수 그래프: Histogram, Box plot
    주요 체크 사항 ‑ 각 변수들 중 skew한 분포가 없는지 확인
    148 | 회귀분석의 이해
    7
    2변수 그래프: Correlation plot
    # 파이썬 코드
    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    cols = ["Petal_Length", "Sepal_Length", "Sepal_Width", "Petal_Width"]
    corr_mat = iris[cols].corr().round(2)
    sns.heatmap(corr_mat, annot=True, cmap=plt.cm.Reds);
    plt.show()
    Petal_Length Sepal_Length Sepal_Width Petal_Width
    Petal_Length
    Sepal_Length
    Sepal_Width
    Petal_Width
    1 0.87 -0.43 0.96
    0.87 1 -0.12 0.82
    -0.43 -0.12 1 -0.37
    0.96 0.82 -0.37 1
    0.4
    0.2
    0.0
    0.2
    0.4
    0.6
    0.8
    1.0
    잔차 그래프와 검정
    잔차의 정규성과 잔차의 등분산성 체크
    • 정규성
    – Anderson‑Darling Test 혹은 Shapiro‑Wilk Test를 실시한다.
    • 잔차 등분산성 검정
    – 어떻게 체크할까? F test, Bartlett 검정 혹은 Levene 검정?
    – 잔차를 그룹을 나눠서 체크 할 카테고리 변수 존재하지 않음.
    # 파이썬 코드
    import scipy.stats as stats
    residuals = model2.resid
    fitted_values = model2.fittedvalues
    다중 선형회귀 (Multiple linear regression) | 149
    plt.figure(figsize=(15,4))
    ^༈ <Figure size 1500x400 with 0 Axes>
    plt.subplot(1,2,1)
    ^༈ <AxesSubplot:>
    plt.scatter(fitted_values, residuals);
    plt.subplot(1,2,2)
    ^༈ <AxesSubplot:>
    stats.probplot(residuals, plot=plt);
    plt.show()
    1 2 3 4 5 6 7
    1.0
    0.5
    0.0
    0.5
    1.0
    2 1 0 1 2
    Theoretical quantiles
    1.0
    0.5
    0.0
    0.5
    1.0
    Ordered Values
    Probability Plot
    Breusch–Pagan / Cook–Weisberg 검정
    • 아이디어: 우리의 잔차가 등분산을 갖는다는 의미는 독립변수에 의하여 설명이 안된다는 의미
    • Breusch–Pagan 선형성
    – 𝐻0
    : 모든 계수 0
    – 𝐻𝐴: 0이 아닌 계수 존재
    귀무가설 하에서 검정통계량은 카이제곱분포 𝑝를 따름.
    ̂𝑟
    2
    𝑖
    / ̂𝜎2 = 𝛿0 + 𝛿1𝑋1 + ... + 𝛿𝑝𝑋𝑝 + 𝑛𝑜𝑖𝑠𝑒
    from statsmodels.stats.diagnostic import het_breuschpagan
    model = ols('Petal_Length ~ Petal_Width + Sepal_Length + Sepal_Width', data=iris).fit()
    bptest = het_breuschpagan(model.resid, model.model.exog)
    print('BP༡test statistics: ', bptest[0])
    ^༈ BP༡test statistics: 6.039114919618932
    150 | 회귀분석의 이해
    7
    print('p༡value: ', bptest[1])
    ^༈ p༡value: 0.10972262962330982
    오차 독립성
    특정 패턴을 띄지 않는지, 분산이 변하지는 않는지를 체크한다.
    • Durbin‑Watson test 실시
    – 귀무가설: 잔차들간의 상관성이 존재하지 않는다.
    – 대립가설: 잔차들간의 자기 상관성이 존재한다.
    그림 7.1: (왼쪽) 비선형성을 설명할 수 있는 모형을 고려 vs. (오른쪽) 등분산성을 만족하지 못하는 경우
    from statsmodels.stats.stattools import durbin_watson
    dw_stat = durbin_watson(model2.resid)
    print(dw_stat)
    ^༈ 1.782966528592163
    7.4 연습문제
    palmerpenguins 패키지에는 남극 Palmer station에서 관측한 펭귄 정보들이 포함된 데이터이다.
    import pandas as pd
    import numpy as np
    from palmerpenguins import load_penguins
    penguins = load_penguins()
    print(penguins.head())
    연습문제 | 151
    ^༈ species island bill_length_mm ^^. body_mass_g sex year
    ^༈ 0 Adelie Torgersen 39.1 ^^. 3750.0 male 2007
    ^༈ 1 Adelie Torgersen 39.5 ^^. 3800.0 female 2007
    ^༈ 2 Adelie Torgersen 40.3 ^^. 3250.0 female 2007
    ^༈ 3 Adelie Torgersen NaN ^^. NaN NaN 2007
    ^༈ 4 Adelie Torgersen 36.7 ^^. 3450.0 female 2007
    ^༈
    ^༈ [5 rows x 8 columns]
    np.random.seed(2022)
    train_index = np.random.choice(penguins.shape[0], 200)
    1) train_index 를 사용하여 펭귄 데이터에서 인덱스에 대응하는 표본들을 뽑아서 train_data를
    만드세요. (단, 결측치가 있는 경우 제거)
    2) train_data의 펭귄 부리길이 (bill_length_mm)를 부리 깊이 (bill_depth_mm)를 사용하여
    산점도를 그려보세요.
    3) 펭귄 부리길이 (bill_length_mm)를 부리 깊이 (bill_depth_mm)의 상관계수를 구하고, 두
    변수 사이에 유의미한 상관성이 존재하는지 검정해보세요.
    4) 펭귄 부리길이 (bill_length_mm)를 부리 깊이 (bill_depth_mm)를 사용하여 설명하는 회귀
    모델을 적합시킨 후 2번의 산점도에 회귀 직선을 나타내 보세요. (모델 1)
    5) 적합된 회귀 모델이 통계적으로 유의한지 판단해보세요.
    6) 𝑅2 값을 구한 후 의미를 해석해 보세요.
    7) 적합된 회귀 모델의 계수를 해석해 보세요.
    8) 1번에서 적합한 회귀 모델에 새로운 변수 (종 ‑ species) 변수를 추가하려고 합니다. 성별 변수
    정보를 사용하여 점 색깔을 다르게 시각화 한 후 적합된 모델의 회귀 직선을 시각화 해보세요.
    (모델 2)
    9) 종 변수가 새로 추가된 모델 2가 모델 1 보다 더 좋은 모델이라는 근거를 제시하세요.
    10) 모델 2의 계수에 대한 검정과 그 의미를 해석해 보세요.
    11) 모델 2 에 잔차 그래프를 그리고, 회귀모델 가정을 만족하는지 검증을 수행해주세요.
    12) 모델 2 의 잔차를 통하여 영향점, 혹은 이상치의 유무를 판단해보세요.
    """