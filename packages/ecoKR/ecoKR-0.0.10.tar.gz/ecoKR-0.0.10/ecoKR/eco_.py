def code():
    print('''
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        from scipy import stats
        import statsmodels.api as sm
        from statsmodels.stats.diagnostic import het_goldfeldquandt
        from scipy.stats import shapiro, spearmanr
                
        data = pd.read_excel('Контрольная работа атт ПМ22-7.xlsx', sheet_name = 'Лист8')
        X_df = data[['Индекс реальной зарплаты']]
        Y_df = data[['Индекс реального ВВП ']]
        X = data['Индекс реальной зарплаты']
        Y = data['Индекс реального ВВП ']
        X_df.head()
                
        Y_df.head()

        plt.scatter(X, Y)
        plt.title('График диаграммы рассеяния зависимой переменной с экзогенным фактором')
        plt.xlabel('Индекс реальной зарплаты')
        plt.ylabel('Индекс реального ВВП ')
        plt.show()        

        r = round(np.corrcoef(X, Y)[0,1], 2)

        r/(1-r**2)**0.5*38**0.5

        data['const'] = 1
        model = sm.OLS(data['Индекс реального ВВП '], data[['const', 'Индекс реальной зарплаты']])
        results = model.fit()
        print(results.summary())

        fvalue = results.fvalue
        pvalue = results.f_pvalue
        print(f'F-статистика = {round(fvalue,2)}, p = {round(pvalue, 2)}')

        tvalues = results.tvalues
        pvalues = results.pvalues
        print('t-статистики:')
        print(tvalues)
        print('p:')
        print(pvalues) 
                
        actual = data['Индекс реального ВВП ']
        predicted = results.predict()
        A = (abs(actual - predicted) / actual).mean()
        print(f'{round(A*100, 2)}%')
                
        from scipy.stats import shapiro
        residuals = results.resid
        shapiro_statistic, shapiro_pvalue = shapiro(residuals)
        print(shapiro_statistic, shapiro_pvalue)
                
        plt.hist(residuals)
                
        plt.scatter(X, residuals**2)
        plt.xlabel('X')
        plt.ylabel('e2')
        plt.show()
                
        spearman_corr, spearman_pvalue = spearmanr(X, residuals)
        print("Тест ранговой корреляции Спирмена:")
        print("Коэффициент корреляции:", spearman_corr)
        print("p-значение:", spearman_pvalue)
                
        spearman_corr, spearman_pvalue = spearmanr(X, abs(residuals))
        print("Тест ранговой корреляции Спирмена:")
        print("Коэффициент корреляции:", spearman_corr)
        print("p-значение:", spearman_pvalue)
                
        y0 = 71.4312 + 0.378*1.05*np.mean(X)
        y0
                
        g = (sum((actual-predicted)**2)/(len(X)-1))**0.5
        g
                
        m = g * (1 + 1/len(X)+((1.05*np.mean(X)-np.mean(X))**2)/sum((X-np.mean(X))**2))**0.5
        m
                
        y = y0 +- m * 2.0243942
                
        ymin = y0 - m * 2.0243942
        ymin
                
        ymax = y0 + m * 2.0243942
        ymax
        ''')
    
code()