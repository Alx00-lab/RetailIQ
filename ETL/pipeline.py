import pandas as pd
import os
from loader import get_engine, load_all_dimensions


# --------------------
# 1. LOAD ------------
# --------------------

def load_data(path):
    return {
        "orders": pd.read_csv(f"{path}/olist_orders_dataset.csv"),
        "order_items": pd.read_csv(f"{path}/olist_order_items_dataset.csv"),
        "products": pd.read_csv(f"{path}/olist_products_dataset.csv"),
        "customers": pd.read_csv(f"{path}/olist_customers_dataset.csv"),
        "category_translation": pd.read_csv(f"{path}/product_category_name_translation.csv")
    }

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_DIR, 'C:\\Users\\Alexander\\Desktop\\RetailIQ\\logic', 'brazilian-ecommerce'))


# -------------
# 2. AUDIT ----
# -------------
def audit_df(df, name):
    print(f"\n{name.upper()}")
    print("-" * 40)
    
    print("Shape:", df.shape)

    nulls = df.isnull().sum()
    print("Nulls:", nulls[nulls > 0] if nulls.sum() else "---No nulls---")

    print("Dtypes:\n", df.dtypes)
    
    print("Duplicates:", df.duplicated().sum())

# ----------------
# 3. Cleaning ----
# ----------------
def clean_products(df_products, df_translation):
    df = df_products.copy()

    # Missing category
    df['product_category_name'] = df['product_category_name'].fillna('Other')

    
    # Joining translation 
    df = df.merge(df_translation, on='product_category_name', how='left')

    # Replacing with English name 
    df['product_category_name'] = df['product_category_name_english'].fillna(df['product_category_name'])

    return df.drop(columns=['product_category_name_english'])


def clean_orders(df_orders):
    df = df_orders.copy()

    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
    
    #Flag missing delivery date
    df['flag_missing_date'] = df['order_delivered_customer_date'].isnull()

    return df

# -------------
# 4. Validation
# -------------

def validate_orders(df):
    invalid_delivered = df[
        (df['order_status'] == 'delivered') &
        (df['order_delivered_customer_date'].isnull())
    ]

    print("Invalid deliverid orders:", len(invalid_delivered))

def validate_prices(df_order_items):
    invalid = df_order_items[df_order_items['price'] <= 0]
    print("Invalid prices:", len(invalid))

# ------------
# 5. Features 
# -------------
def create_features(df_orders, df_order_items):
    df = df_order_items.merge(df_orders, on='order_id', how='inner')

    # Total Value
    df['total_order_value'] = df['price'] + df['freight_value']

    # Delivery time
    df['delivery_days'] = (
        df['order_delivered_customer_date'] - 
        df['order_purchase_timestamp']
    ).dt.days

    # Only valid for delivered
    df.loc[df['order_status'] != 'delivered', 'delivery_days'] = None

    return df

# -------------
# 6. Enrichment
# -------------
def add_customers(df, df_customers):
    return df.merge(
        df_customers[['customer_id', 'customer_unique_id']],
        on='customer_id',
        how='left'
    )


# -------------------
# 7. Running Pipeline
# -------------------

def run_pipeline(path):
    data = load_data(path)

    for name, df in data.items():
        audit_df(df, name)

    df_products = clean_products(data['products'], data['category_translation'])
    df_orders = clean_orders(data['orders'])

    validate_orders(df_orders)
    validate_prices(data['order_items'])

    df_main = create_features(df_orders, data['order_items'])
    df_main = add_customers(df_main, data['customers'])

    audit_df(df_main, "order_items")
    print(df_main.head(10))
    # 
    engine = get_engine(server="AlexanderDNA", database="RetailIQ_db")
    load_all_dimensions(df_main, data['customers'], df_products, df_orders, engine)

    return df_main

df_execute = run_pipeline(DATA_PATH)

