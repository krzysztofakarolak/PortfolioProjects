# Project number 2

import pandas as pd


def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('/workspace/boilerplate-demographic-data-analyzer/adult.data.csv')

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = pd.Series([df['race'][df['race'].str.contains('White')].count(),df['race'][df['race'].str.contains('Black')].count(),df['race'][df['race'].str.contains('Asian-Pac-Islander')].count(),df['race'][df['race'].str.contains('Amer-Indian-Eskimo')].count(),df['race'][df['race'].str.contains('Other')].count()],['White','Black','Asian-Pac-Islander','Amer-Indian-Eskimo','Other'])

    # What is the average age of men?
    average_age_men = round(df['age'][df['sex'].str.contains('Male')].sum()/df['sex'][df['sex'].str.contains('Male')].count(),1)

    # What is the percentage of people who have a Bachelor's degree?
    percentage_bachelors = round((df['education'][df['education'].str.contains('Bachelors')].count()/df['education'].count())*100,1)
        # or percentage_bachelors = print(str(round((df['education'][df['education'].str.contains('Bachelors')].count()/df['education'].count())*100,1)),'%')

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = df['education'][df['education'].str.contains('Bachelors')].count()+df['education'][df['education'].str.contains('Masters')].count()+df['education'][df['education'].str.contains('Doctorate')].count()
    lower_education = df['education'].count()-(df['education'][df['education'].str.contains('Bachelors')].count()+df['education'][df['education'].str.contains('Masters')].count()+df['education'][df['education'].str.contains('Doctorate')].count())

    # People who eran more than 50k
    o50k=df['salary'][df['salary'].str.contains('>50K')].count()
    # People who earn more than 50k and has Bachelors 
    Bwo50k=df['salary'][df['salary'].str.contains('>50K')&df['education'].str.contains('Bachelors')].count()
    # People who earn more than 50k and has Masters
    Mwo50k=df['salary'][df['salary'].str.contains('>50K')&df['education'].str.contains('Masters')].count()
    # People who earn more than 50k and has Doctorate
    Dwo50k=df['salary'][df['salary'].str.contains('>50K')&df['education'].str.contains('Doctorate')].count()
    # People who earn more than 50k and has higher education
    D50k=Bwo50k+Mwo50k+Dwo50k

    # percentage with salary >50K
    higher_education_rich = round((D50k/higher_education)*100,1)
    lower_education_rich = round(((o50k-D50k)/lower_education)*100,1)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    num_min_workers = df['hours-per-week'][df['hours-per-week']<=min_work_hours].count()
    rich_percentage = round((df['hours-per-week'][df['hours-per-week']<=min_work_hours & df['salary'].str.contains('>50K')].count()/num_min_workers)*100,1)


    # What country has the highest percentage of people that earn >50K?
    ##chsdf=df[['native-country','salary']][df['salary'].str.contains('>50K')].sort_values(['native-country'])
    ##nbchsdf=chsdf['native-country'].value_counts()
    ##casdf=df[['native-country','salary']].sort_values(['native-country'])
    ##nbcasdf=casdf['native-country'].value_counts()
    ##df3=pd.merge(nbchsdf,nbcasdf, on='native-country')
    ##percdf3=df3.iloc[:,0]/df3.iloc[:,1]
    percdf3=(df.groupby('native-country')['salary'].apply(lambda x: (x == '>50K').mean()))

    highest_earning_country = percdf3.idxmax()
    highest_earning_country_percentage = round(percdf3.max()*100,1)

    # Identify the most popular occupation for those who earn >50K in India.
    ind_highearn=df[['native-country','salary','occupation']][(df['native-country'].str.contains('India')) &(df['salary'].str.contains('>50K'))]

    top_IN_occupation = ind_highearn['occupation'].value_counts().idxmax()

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }
