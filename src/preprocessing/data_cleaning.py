import re, ast, json
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.compose import ColumnTransformer
from pathlib import Path

UNINFORMATIVE_COLUMNS = [
    'listing_url', 'scrape_id', 'host_url', 
    'host_thumbnail_url', 'source', 'picture_url', 'host_picture_url'
]

SPECIAL_IMPUTATIONS_MAPPING = {
    "host_response_time" : "response time not mentioned",
    "host_verifications" : "no verifications"
}

def load_dtype_mapping(p):
    with open(p) as f:
        dtype_mapping = json.load(f)
    return dtype_mapping


def special_imputations(df, mapping):
    return listings_df.fillna(mapping)

def get_imputation_pipeline(mapping): 
    return ColumnTransformer(
                            [
                                ("continuous", SimpleImputer(strategy="mean").set_output(transform = 'pandas'), mapping["continuous"]),
                                ("discrete", SimpleImputer(strategy="most_frequent").set_output(transform = 'pandas'), mapping["discrete"]),
                                ("nominal", SimpleImputer(strategy="most_frequent").set_output(transform = 'pandas'), mapping["nominal"])
                            ], 
                            remainder='passthrough'
                    )

def imputer_fit_transform(preprocessor, df, mapping):
    result_array = preprocessor.fit_transform(df)
    
    columns = (
        mapping["continuous"] +
        mapping["discrete"] +
        mapping["nominal"]
    )
    
    passthrough_cols = [c for c in df.columns if c not in columns]
    columns += passthrough_cols
    
    return pd.DataFrame(result_array, columns=columns, index=df.index)
  
def clean_price(df):
    PATTERN = r"[$,]"
    df = df.copy()
    df["price"] = df["price"].astype(str).str.replace(PATTERN, "", regex=True)
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df.dropna(subset=["price"])
    return df

def clean_text(s):
    if pd.isna(s):
        return ""
    s = str(s)
    s = re.sub(r"<.*?>", " ", s)
    s = re.sub(r"http\S+", " ", s)        
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()

def parse_py_object(df, targets=['amenities']):
    df = df.copy()
    for col in targets:
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else np.nan)
    return df

def parse_percents(df, targets):
    PATTERN = r"\%"
    return df.assign(
                        **{
                            target : pd.to_numeric(df[target].astype(str).str.replace(PATTERN, "", regex=True), errors="coerce")
                            for target in targets
                        }
            )
    
def clean_listings_df(listings_df, uninformative_columns=UNINFORMATIVE_COLUMNS):
    return (
        listings_df
            .pipe(lambda df: df.rename(columns={"id":"listing_id"}))
            .pipe(lambda df: df.drop(uninformative_columns, axis=1))
            .pipe(clean_price)
            .pipe(parse_percents, targets=["host_response_rate","host_acceptance_rate"])
            .pipe(parse_py_object, targets=["amenities"])
            .pipe(lambda df: df.dropna(axis=1, how='all'))
            .pipe(lambda df: df.fillna({"host_response_time" : "response time not mentioned"}))
            .pipe(
                    lambda df: df.assign(
                                        host_verifications=df.apply(
                                                                    lambda x: ["N/A"] 
                                                                    if (
                                                                        pd.isna(x["host_verifications"])
                                                                        or
                                                                        len(x["host_verifications"]) == 0
                                                                    )
                                                                    else x["host_verifications"], 
                                                                    axis=1)
                                        )
            )
    )
    
def preprocess(df, dmap):
    df = clean_listings_df(df) 
    imputation_pipeline = get_imputation_pipeline(dmap)
    processed_df = imputer_fit_transform(imputation_pipeline, df, dmap)
    return processed_df, imputation_pipeline
    
