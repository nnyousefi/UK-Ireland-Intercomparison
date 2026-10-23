import pandas as pd
import numpy as np
import itertools
from scipy import stats

def main():
    #Set taxa
    taxa = ["Betu", "Poac"]
    #Metrics
    metrics = ["APIn", "duration", "start_DOY"]
    #Import annual metrics master table
    annual_metrics = pd.read_csv("data/processed/yearly_metrics/all_annual_metrics.csv")
    #Convert start date to start_DOY (day of year)
    annual_metrics["start_date"] = pd.to_datetime(annual_metrics["start_date"], format="%Y-%m-%d")
    #Extract day of year from datetime series
    annual_metrics["start_DOY"] =annual_metrics["start_date"].dt.dayofyear



    results = {}
    for taxon in taxa:
        for metric in metrics:
            #Reformat dataframe to extract APIn per year at each site
            metric_site_year_df = site_by_year(annual_metrics, metric, taxon)
            #Calculate pairwise correlations
            ##Correlation Matrices
            pairwise_pearson = metric_site_year_df.corr(method="pearson", min_periods=5)
            pairwise_spearman = metric_site_year_df.corr(method="spearman", min_periods=5)
            
            #Export Statistical Reports

            #Short Pairwise Correlation Matrix 
            pairwise_pearson.to_csv(f"data/processed/analysis/synchrony/pearson/{taxon}_{metric}_pearson_corrmatrix.csv")
            pairwise_spearman.to_csv(f"data/processed/analysis/synchrony/spearman/{taxon}_{metric}_spearman_corrmatrix.csv")

            #Detailed Pearson
            #Pearson
            pearson_results = pearson_test(metric_site_year_df, taxon)
            pearson_results = pd.DataFrame(pearson_results)
            pearson_results.to_csv(f"data/processed/analysis/synchrony/pearson/{taxon}_{metric}_detailed_pearson.csv")


            spearman_results = spearman_test(metric_site_year_df, taxon)
            spearman_results = pd.DataFrame(spearman_results)
            spearman_results.to_csv(f"data/processed/analysis/synchrony/spearman/{taxon}_{metric}_detailed_spearman.csv")
            


        


#Reshape data to extract APIn per year at each site
def site_by_year(df, metric, taxon):
    #Filter by taxon
    filtered_df = df[df["taxon"] == taxon].copy()
    #Reshape dataframe
    filtered_df = filtered_df.pivot(index="year", columns = "site", values=metric)
    return filtered_df

def pearson_test(df, taxon):
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

    return results

def spearman_test(df, taxon):
    sites = list(df.columns)
    results = []
    for pair in itertools.combinations(sites, 2):
        pair = list(pair)
        API_values = df[pair].dropna()
        n = len(API_values)
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