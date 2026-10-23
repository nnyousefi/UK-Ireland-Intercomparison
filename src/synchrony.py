import pandas as pd
import numpy as np
import itertools
from scipy import stats

def main():
    #Set taxa
    taxa = ["Betu", "Poac"]
    #Import annual metrics master table
    annual_metrics = pd.read_csv("data/processed/yearly_metrics/all_annual_metrics.csv")

    results = {}
    for taxon in taxa:
        #Reformat dataframe to extract APIn per year at each site
        APIn_site_year = site_by_year(annual_metrics, "APIn", taxon)
        #Calculate pairwise correlations
        ##Correlation Matrices
        pairwise_pearson = APIn_site_year.corr(method="pearson", min_periods=5)
        pairwise_spearman = APIn_site_year.corr(method="spearman", min_periods=5)
        #Statistical Report
        results = stats_tests(APIn_site_year, taxon)
        
        #Export results
        pairwise_pearson.to_csv(f"data/processed/analysis/{taxon}_pearson_corrmatrix.csv")
        pairwise_spearman.to_csv(f"data/processed/analysis/{taxon}_spearman_corrmatrix.csv")
        results_df = pd.DataFrame(results)
        results_df.to_csv(f"data/processed/analysis/{taxon}_detailed_stats.csv")


        


#Reshape data to extract APIn per year at each site
def site_by_year(df, metric, taxon):
    #Filter by taxon
    filtered_df = df[df["taxon"] == taxon].copy()
    #Reshape dataframe
    filtered_df = filtered_df.pivot(index="year", columns = "site", values=metric)
    return filtered_df

def stats_tests(df, taxon):
    methods = ["pearson", "spearman"]
    sites = list(df.columns)
    results = []
    for pair in itertools.combinations(sites, 2):
        pair = list(pair)
        API_values = df[pair].dropna()
        n = len(API_values)

        #r = correlation coefficient, p = p-value
        pearson_result = stats.pearsonr(df[pair[0]], df[pair[1]])
        r = pearson_result.statistic
        p = pearson_result.pvalue
        confidence = pearson_result.confidence_interval(confidence_level=0.95)
        ci_low = confidence.low
        ci_high = confidence.high

        results.append({
            "taxon": taxon,
            "site_1": pair[0],
            "site_2": pair[1],
            "method": "pearson",
            "n": n,
            "correlation": r,
            "p_value": p,
            "lower_bound": ci_low,
            "upper_bound": ci_high
        })

        #Spearman test
         #rho = correlation coefficient, p = p-value
        spearman_result = stats.spearmanr(df[pair[0]], df[pair[1]])
        rho = spearman_result.statistic
        p = spearman_result.pvalue
        ci_low = np.nan
        ci_high = np.nan

        results.append({
            "taxon": taxon,
            "site_1": pair[0],
            "site_2": pair[1],
            "method": "spearman",
            "n": n,
            "correlation": rho,
            "p_value": p,
            "lower_bound": ci_low,
            "upper_bound": ci_high
        })

    return results
        
    


if __name__ == "__main__":
    main()