from collections import defaultdict
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

df_data = pd.read_csv('dataset/dataset.csv', sep=',')
df_results = pd.read_csv('results/combined_arity.csv', sep=',')
# Groupy results by orthogroups
df_results_grouped = df_results.groupby('Orthogroup')
dict_arity = defaultdict(dict)
for key, group in df_results_grouped:
    # Compute the arity for each orthogroup
    gp = group.groupby('arity')
    dict_arity["mean_arity"][key] = sum([i * len(g) for i, g in gp])
    dict_arity["arity2"][key] = len(gp.get_group(2)) if 2 in gp.groups else 0
    dict_arity["arity3"][key] = len(gp.get_group(3)) if 3 in gp.groups else 0

# Add a new column to the dataset
for key in dict_arity.keys():
    df_data[key] = df_data['key'].map(dict_arity[key])
    df_data[key] = df_data[key].fillna(0)


def mutation_rate(x):
    return "Low" if "LowMut" in x else ("High" if "HighMut" in x else "Medium")


df_data["MutationRate"] = df_data["experiment"].apply(mutation_rate)
df_data["Dataset"] = df_data["experiment"].apply(lambda x: "498Sites" if "498Sites" in x else "1ExonNP")
df_high_mut = df_data[df_data["MutationRate"].isin(["High"])]
df_pop_size = df_data[(df_data["PopSizeRelative"] < 0.5) & (df_data["MutationRate"].isin(["High"]))]

orders_dict = {'FixPopSize': ["fixed", "slow", "change", "fast"],
               "MutationRate": ['Low', 'Medium', 'High']}
factors = set(df_data.columns) - {'key', "experiment"} - set(dict_arity.keys())

sm_model = sm.OLS.from_formula('mean_arity ~ C(FixPopSize) + C(MutationRate) + C(Dataset) + PopSizeRelative',
                               data=df_data).fit()
print(sm_model.summary())
for factor in factors:
    for name, df in [("All", df_data), ("HighMut", df_high_mut), ("PopSize", df_pop_size)]:
        if name == "HighMut" and factor == "MutationRate":
            continue
        if factor not in orders_dict:
            orders_dict[factor] = sorted(set(df[factor]))

        # Sort the dataset by the factor using the order defined in orders_dict
        df = df.sort_values(by=factor, key=lambda x: x.map({v: k for k, v in enumerate(orders_dict[factor])}))
        # Boxplot of arity as a function of each factor (using seaborn)
        for arity in dict_arity.keys():
            # Boxplot with as much information as possible (whiskers, outliers, etc.)
            sns.boxplot(x=factor, y=arity, data=df, showfliers=True, showmeans=True, meanline=True, showbox=True)
            plt.xlabel(factor)
            plt.ylabel(arity)
            # Linear model and r-squared of the relationship between the factor (category) and the arity (continuous) using statsmodels
            sm_model = sm.OLS.from_formula(f'{arity} ~ {factor}', data=df).fit()
            plt.title(f'{arity} ~ {factor} (R²={sm_model.rsquared:.2f}, p={sm_model.f_pvalue:.2e}, n={len(df)})')
            # Orientation of the x-axis labels
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            # Save the plot
            plt.savefig(f'results/boxplot_{name}_{factor}_{arity}.pdf')
            plt.clf()
            plt.close("all")
