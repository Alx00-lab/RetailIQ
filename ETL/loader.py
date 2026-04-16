from sqlalchemy import create_engine, text 
import pandas as pd

# --- Connection ---
def get_engine(server: str, database: str) -> object:
    conn_str = (
        f"mssql+pyodbc://{server}/{database}"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )
    return create_engine(conn_str, fast_executemany=True)

# --- Prepare Dimensions ---
def prepare_dim_customers(df_customers: pd.DataFrame) -> pd.DataFrame:
    cols = [
        'customer_unique_id', 'customer_id',
        'customer_zip_code_prefix', 'customer_city', 'customer_state'
    ]
    return (
        df_customers[cols]
        .drop_duplicates(subset=['customer_unique_id'])
        .reset_index(drop=True)
    )

# ---

def prepare_dim_products(df_products: pd.DataFrame) -> pd.DataFrame:
    cols = [
        'product_id', 'product_category_name',
        'product_name_lenght', 'product_description_lenght',
        'product_photos_qty', 'product_weight_g',
        'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    return df_products[cols].drop_duplicates(subset=['product_id'])

# --- 
def prepare_dim_date(df_orders: pd.DataFrame) -> pd.DataFrame:
    all_dates = pd.concat([
        df_orders['order_purchase_timestamp'],
        df_orders['order_delivered_customer_date']
    ]).dropna().dt.date

    df_date = pd.DataFrame({'FullDate': pd.to_datetime(all_dates.unique())})
    df_date['DateKey']   = df_date['FullDate'].dt.strftime('%Y%m%d').astype(int)
    df_date['Year']      = df_date['FullDate'].dt.year
    df_date['Month']     = df_date['FullDate'].dt.month
    df_date['MonthName'] = df_date['FullDate'].dt.strftime('%B')
    df_date['Quarter']   = df_date['FullDate'].dt.quarter

    return df_date.drop_duplicates(subset=['DateKey']).sort_values('DateKey')


# --- Loader ---

def load_dimension(df: pd.DataFrame, table_name: str, engine) -> None:
    print(f"\nLoading {table_name}...")
    try:
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            schema="dbo"
        )
        print(f" {len(df)} rows loaded into {table_name}")
    except Exception as e:
        print(f" Failed on {table_name}: {e}")
        raise # Re-raise so the pipeline stops — don't silently continue

# --- ORCHESTRATE ---
def load_all_dimensions(df_main, df_customers, df_products_clean, df_orders_clean, engine):
    dim_customers = prepare_dim_customers(df_customers)
    dim_products  = prepare_dim_products(df_products_clean)
    dim_date      = prepare_dim_date(df_orders_clean)


    # remenber here the ones with FK-safe order
    load_dimension(dim_customers, "dim_customers", engine)
    load_dimension(dim_products,  "dim_products",  engine)
    load_dimension(dim_date,      "dim_date",      engine)

    print("\n All dimensions loaded successfully.")



    