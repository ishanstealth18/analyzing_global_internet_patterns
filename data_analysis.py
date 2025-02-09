import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

# Read and create Dataframe from CSV file
src_file = pd.read_csv("datalab_export_2025-01-26 22_41_23.csv", header=0, sep=",")
pd.set_option('display.max_columns',None)
pd.set_option('display.max_rows', None)


# data pre processing
# Check and remove nul values
def remove_null(input_data):
    # check any null values
    if input_data.isna().values.any():
        # drop rows where there is null values
        print("Null values found !!")
        input_data.dropna(inplace=True)
    else:
        print("No Null values !!!")

    return input_data


def replace_val(input_data):
    input_data.replace('..', 0, inplace=True)
    #print(input_data)

    return input_data


def bar_chart(data):
    #print(data['Country Name'].values)
    cleaned_data = data_clean(data)
    normalized_data = normalize_data(cleaned_data)
    country_list = normalized_data['Country Name'].values
    for i in range(len(country_list)):
        x = normalized_data.columns[3:27]
        y = normalized_data[normalized_data.columns[3:27]].iloc[i]
        print(y)
        plt.title(country_list[i])
        plt.xlabel("Year")
        plt.ylabel("Internet Usage")
        # Rotating X-axis labels
        plt.xticks(rotation=90)
        plt.bar(x, y, width=0.5)
        plt.show()

def box_plot(data):

    cleaned_data = data_clean(data)
    normalized_data = normalize_data(cleaned_data)
    country_list = normalized_data['Country Name'].values
    for i in range(len(country_list)):
        input_data = normalized_data[normalized_data.columns[3:27]].iloc[i]
        input_data = list(input_data)
        for j in range(len(input_data)):
            input_data[j] = float(input_data[j])

        #print(input_data)
        fig = plt.figure(figsize=(10, 7))
        plt.title(country_list[i])
        # Creating plot
        plt.boxplot(input_data)
        # show plot
        plt.show()


def data_clean(data):
    data_null_removed = remove_null(data)
    replace_junk_val = replace_val(data_null_removed)
    row_drop_index = replace_junk_val[replace_junk_val['Country Name'] == "American Samoa"].index
    replace_junk_val.drop(row_drop_index, inplace=True)
    #print(replace_junk_val.info())
    #print(replace_junk_val.columns[3:])

    for x in replace_junk_val.columns[3:]:
        replace_junk_val[x] = pd.to_numeric(replace_junk_val[x], errors='coerce')

    #print(replace_junk_val.describe(include='all'))

    return replace_junk_val


def normalize_data(data):
    clean_data = data_clean(data)
    df_copy = clean_data.iloc[:, 3:].copy()

    # normalize using max min scaling
    for col in df_copy.columns:
        df_copy[col] = (df_copy[col] - df_copy[col].min()) / (df_copy[col].max() - df_copy[col].min())

    # drop old columns
    clean_data.drop(clean_data.iloc[:, 3:], axis=1, inplace=True)
    normalized_df = pd.concat([clean_data, df_copy], axis=1)
    print(normalized_df)


    return normalized_df


def find_correlation(data):
    normalized_data = normalize_data(data)
    df_copy = normalized_data.iloc[:, 3:].copy()
    # find correlation
    df_corr = df_copy.corr()
    print("correlation matrix shape:", df_corr.shape)

    corr_array = df_corr.to_numpy()
    print("corr array:", corr_array)

    df_corr.to_csv("correlation_matrix.csv")


def histogram(data):
    cleaned_data = data_clean(data)
    normalized_data = normalize_data(cleaned_data)
    country_list = normalized_data['Country Name'].values
    for c in range(len(country_list)):
        d = normalized_data[normalized_data.columns[3:27]].iloc[c]
        plt.title(country_list[c])
        plt.xlabel("Internet Usage")
        plt.ylabel("Number of years")

        plt.hist(d)
        plt.show()


#data_info(src_file)
#remove_null(src_file)
#replace_val(src_file)
#bar_chart(src_file)
box_plot(src_file)
#data_clean(src_file)
#normalize_data(src_file)
#find_correlation(src_file)
#histogram(src_file)