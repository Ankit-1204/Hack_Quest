import streamlit as st
import pandas as pd
import os
import csv
from PIL import Image

CSV_FILE = "products.csv"
UPLOAD_FOLDER = "uploads"


def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

# Function to add product to CSV file
def add_product_to_csv(product_name, uploaded_image):
    try:
        # Save the uploaded image to the upload folder
        image_path = os.path.join(UPLOAD_FOLDER, uploaded_image.name)
        with open(image_path, "wb") as f:
            f.write(uploaded_image.read())

    
        image_path = image_path.replace("\\", "/")

        # Append product details to CSV
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([product_name, image_path])

        st.success("Product added successfully!")
    except Exception as e:
        st.error(f"Error adding product: {e}")

# Function to remove products from CSV file
def remove_products_from_csv(selected_products):
    try:
        df = pd.read_csv(CSV_FILE)
        df = df[~df['Product'].isin(selected_products)]
        df.to_csv(CSV_FILE, index=False)
        st.success("Selected products removed successfully!")
    except Exception as e:
        st.error(f"Error removing products: {e}")

# Function to check admin login
def admin_login(username, password):
    return username == "User_1203" and password == "x1y2z3"

# Main function
def main():
    st.title("Manage Products")

    # Login section
    st.sidebar.header("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    # Proceed if admin login is successful
    if admin_login(username, password):
        st.success("Login successful!")

        # Create upload folder if it doesn't exist
        create_upload_folder()

        # Input fields
        product_name = st.text_input("Enter Product Name")
        uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

        # Button to add product
        if st.button("Add Product") and product_name and uploaded_image:
    
            add_product_to_csv(product_name, uploaded_image)

        
        st.header("Existing Products")
        df = pd.read_csv(CSV_FILE)
        selected_products = st.multiselect("Select products to remove", df['Product'])
        if st.button("Remove Selected Products") and selected_products:
            # Remove selected products from CSV
            remove_products_from_csv(selected_products)
        
    
        st.write(df)
    else:
        if login_button:
            st.error("Invalid username or password.")

if __name__ == "__main__":
    main()

