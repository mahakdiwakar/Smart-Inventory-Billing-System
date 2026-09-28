import streamlit as st
import psycopg2
from datetime import datetime, date
import sys
import os

# Add the models directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from Database import conn
from customers import Customer
from products import Product
from sales import Sale
from sales_items import SaleItem

# ============================================================================
# GLOBAL CSS STYLING - MODERN PROFESSIONAL DASHBOARD
# ============================================================================

def apply_global_styling():
    """Apply modern, professional CSS styling to the entire application"""
    st.markdown("""
    <style>
    /* ROOT VARIABLES */
    :root {
        --primary: #4F46E5;
        --secondary: #06B6D4;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --purple: #8B5CF6;
        --bg: #F8FAFC;
        --card: #FFFFFF;
        --text: #0F172A;
        --muted: #64748B;
        --border: #E2E8F0;
        --shadow: 0 4px 12px rgba(15, 23, 42, 0.08);
        --shadow-hover: 0 12px 24px rgba(15, 23, 42, 0.12);
    }

    /* GLOBAL PAGE STYLING */
    body, html, [data-testid="stAppViewContainer"] {
        background-color: var(--bg) !important;
    }

    [data-testid="stAppViewContainer"] {
        background-color: var(--bg);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
        border-right: 1px solid var(--border);
    }

    /* MAIN CONTENT AREA */
    [data-testid="stMainBlockContainer"] {
        background-color: var(--bg);
        padding: 2rem 1rem;
    }

    /* TEXT AND TYPOGRAPHY */
    h1 {
        color: var(--text) !important;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }

    h2 {
        color: var(--text) !important;
        font-weight: 600;
        font-size: 1.875rem;
        margin-bottom: 1.25rem;
        margin-top: 1.5rem;
    }

    h3 {
        color: var(--text) !important;
        font-weight: 600;
        font-size: 1.25rem;
        margin-bottom: 1rem;
    }

    p {
        color: var(--muted);
        line-height: 1.6;
        font-size: 0.95rem;
    }

    /* SIDEBAR STYLING */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        padding: 1.5rem;
    }

    [data-testid="stSidebar"] .css-1d391kg {
        padding-top: 2rem;
    }

    /* SIDEBAR HEADER */
    [data-testid="stSidebar"] h1 {
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
        color: var(--primary);
    }

    [data-testid="stSidebar"] h2 {
        font-size: 1.1rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: var(--text);
        font-weight: 600;
    }

    /* SELECTBOX STYLING */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        background-color: white !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] > div:first-child {
        padding: 10px 12px !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-weight: 500;
    }

    /* RADIO BUTTON STYLING */
    [data-testid="stRadio"] label {
        color: var(--text) !important;
        font-weight: 500;
        margin-right: 1.5rem;
        cursor: pointer;
        transition: color 0.3s ease;
    }

    [data-testid="stRadio"] label:hover {
        color: var(--primary) !important;
    }

    /* TEXT INPUT STYLING */
    input[type="text"],
    input[type="date"],
    input[type="number"],
    textarea {
        border-radius: 8px !important;
        border: 1px solid var(--border) !important;
        padding: 10px 12px !important;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        background-color: white !important;
        color: var(--text) !important;
    }

    input[type="text"]:focus,
    input[type="date"]:focus,
    input[type="number"]:focus,
    textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        outline: none !important;
    }

    textarea {
        font-family: inherit;
        resize: vertical;
        min-height: 100px;
    }

    /* BUTTON STYLING */
    .stButton > button {
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease !important;
        border: none !important;
        cursor: pointer;
        text-transform: none;
    }

    .stButton > button:first-child {
        width: 100%;
        background-color: var(--primary) !important;
        color: white !important;
        box-shadow: 0 2px 8px rgba(79, 70, 229, 0.3);
    }

    .stButton > button:first-child:hover {
        background-color: #4338ca !important;
        box-shadow: 0 8px 16px rgba(79, 70, 229, 0.4) !important;
        transform: translateY(-2px);
    }

    /* SUCCESS BUTTON */
    .success-button {
        background-color: var(--success) !important;
        color: white !important;
    }

    .success-button:hover {
        background-color: #059669 !important;
    }

    /* DANGER BUTTON */
    .danger-button {
        background-color: var(--danger) !important;
        color: white !important;
    }

    .danger-button:hover {
        background-color: #dc2626 !important;
    }

    /* SECONDARY BUTTON */
    .secondary-button {
        background-color: var(--border) !important;
        color: var(--text) !important;
    }

    .secondary-button:hover {
        background-color: #cbd5e1 !important;
    }

    /* METRICS STYLING */
    [data-testid="metric-container"] {
        background-color: var(--card);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }

    [data-testid="metric-container"]:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-2px);
        border-color: var(--primary);
    }

    [data-testid="metric-container"] label {
        color: var(--muted);
        font-weight: 500;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    [data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--text);
        font-size: 2rem;
        font-weight: 700;
    }

    /* INFO/SUCCESS/ERROR/WARNING ALERTS */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        border: 1px solid;
        padding: 1rem;
        margin: 1rem 0;
    }

    [data-testid="stAlert"][kind="info"] {
        background-color: rgba(6, 182, 212, 0.1) !important;
        border-color: #06B6D4 !important;
        color: #0891b2 !important;
    }

    [data-testid="stAlert"][kind="success"] {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border-color: #10B981 !important;
        color: #059669 !important;
    }

    [data-testid="stAlert"][kind="error"] {
        background-color: rgba(239, 68, 68, 0.1) !important;
        border-color: #EF4444 !important;
        color: #dc2626 !important;
    }

    [data-testid="stAlert"][kind="warning"] {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border-color: #F59E0B !important;
        color: #d97706 !important;
    }

    /* FORM STYLING */
    form {
        background-color: var(--card);
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        margin: 1.5rem 0;
    }

    form label {
        color: var(--text) !important;
        font-weight: 600;
        margin-bottom: 0.5rem;
        display: block;
        font-size: 0.95rem;
    }

    /* COLUMNS SPACING */
    [data-testid="column"] {
        padding: 0 0.5rem;
    }

    /* TABLE STYLING */
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1rem 0;
    }

    tbody tr {
        border-bottom: 1px solid var(--border);
        transition: background-color 0.2s ease;
    }

    tbody tr:hover {
        background-color: rgba(79, 70, 229, 0.05);
    }

    td, th {
        padding: 0.75rem;
        text-align: left;
        color: var(--text);
    }

    th {
        background-color: var(--bg);
        font-weight: 600;
        color: var(--text);
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        border-bottom: 2px solid var(--border);
    }

    /* EXPANDER STYLING */
    [data-testid="stExpander"] {
        background-color: var(--card);
        border-radius: 8px;
        border: 1px solid var(--border);
        margin: 0.5rem 0;
    }

    [data-testid="stExpander"] button {
        color: var(--text) !important;
    }

    /* CHART STYLING */
    [data-testid="chartContainer"] {
        background-color: var(--card);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        margin: 1.5rem 0;
    }

    /* SEPARATOR/DIVIDER */
    hr {
        border: none;
        height: 1px;
        background-color: var(--border);
        margin: 2rem 0;
    }

    /* RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        h1 {
            font-size: 1.75rem;
        }

        h2 {
            font-size: 1.25rem;
        }

        form {
            padding: 1.5rem;
        }

        [data-testid="metric-container"] {
            padding: 1rem;
        }
    }

    /* KPI CARD STYLING */
    .kpi-card {
        background: linear-gradient(135deg, var(--card) 0%, #FFFFFF 100%);
        border-radius: 12px;
        padding: 1.75rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 1rem;
    }

    .kpi-card:hover {
        box-shadow: var(--shadow-hover);
        transform: translateY(-4px);
        border-color: var(--primary);
    }

    .kpi-card-icon {
        font-size: 2rem;
        margin-bottom: 0.75rem;
    }

    .kpi-card-label {
        color: var(--muted);
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }

    .kpi-card-value {
        color: var(--text);
        font-size: 2.25rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    .kpi-card-desc {
        color: var(--muted);
        font-size: 0.85rem;
    }

    .kpi-primary { border-left: 4px solid var(--primary); }
    .kpi-secondary { border-left: 4px solid var(--secondary); }
    .kpi-success { border-left: 4px solid var(--success); }
    .kpi-warning { border-left: 4px solid var(--warning); }
    .kpi-danger { border-left: 4px solid var(--danger); }
    .kpi-purple { border-left: 4px solid var(--purple); }

    /* CARD STYLING FOR LISTS */
    .info-card {
        background-color: var(--card);
        border-radius: 10px;
        padding: 1.25rem;
        border: 1px solid var(--border);
        margin: 0.75rem 0;
        transition: all 0.2s ease;
    }

    .info-card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.08);
    }

    .info-card-title {
        color: var(--text);
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.95rem;
    }

    .info-card-text {
        color: var(--muted);
        font-size: 0.85rem;
        margin: 0.25rem 0;
    }

    /* BADGE STYLING */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-success {
        background-color: rgba(16, 185, 129, 0.15);
        color: #059669;
    }

    .badge-warning {
        background-color: rgba(245, 158, 11, 0.15);
        color: #d97706;
    }

    .badge-danger {
        background-color: rgba(239, 68, 68, 0.15);
        color: #dc2626;
    }

    .badge-info {
        background-color: rgba(6, 182, 212, 0.15);
        color: #0891b2;
    }

    /* INVOICE STYLING */
    .invoice-container {
        background-color: var(--card);
        border-radius: 12px;
        padding: 2.5rem;
        border: 1px solid var(--border);
        box-shadow: var(--shadow);
        max-width: 700px;
        margin: 2rem auto;
    }

    .invoice-header {
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 2px solid var(--border);
        padding-bottom: 1.5rem;
    }

    .invoice-header h1 {
        color: var(--primary);
        font-size: 1.5rem;
        margin: 0;
    }

    .invoice-header p {
        color: var(--muted);
        margin: 0.5rem 0 0 0;
        font-size: 0.9rem;
    }

    .invoice-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin: 1.5rem 0;
    }

    .invoice-detail-item {
        margin-bottom: 0.75rem;
    }

    .invoice-detail-label {
        color: var(--muted);
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.25rem;
    }

    .invoice-detail-value {
        color: var(--text);
        font-weight: 600;
        font-size: 1rem;
    }

    .invoice-items {
        margin: 2rem 0;
        border-top: 1px solid var(--border);
        border-bottom: 1px solid var(--border);
        padding: 1rem 0;
    }

    .invoice-item-row {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 1rem;
        padding: 0.75rem 0;
        font-size: 0.9rem;
        color: var(--text);
    }

    .invoice-item-header {
        font-weight: 600;
        color: var(--muted);
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.5px;
        border-bottom: 1px solid var(--border);
        padding-bottom: 0.5rem;
        margin-bottom: 0.5rem;
    }

    .invoice-total {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 2px solid var(--primary);
    }

    .invoice-total-label {
        color: var(--text);
        font-weight: 600;
        font-size: 1.1rem;
        margin-right: 1.5rem;
    }

    .invoice-total-value {
        color: var(--primary);
        font-weight: 700;
        font-size: 2rem;
    }

    /* SECTION DIVIDER */
    .section-divider {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2rem 0 1.5rem 0;
    }

    .section-divider::before,
    .section-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(to right, transparent, var(--border), transparent);
    }

    .section-divider span {
        color: var(--muted);
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# CUSTOM COMPONENT FUNCTIONS
# ============================================================================

def create_kpi_card(label, value, description, icon, color_class="kpi-primary"):
    """Create a professional KPI card"""
    st.markdown(f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-card-icon">{icon}</div>
        <div class="kpi-card-label">{label}</div>
        <div class="kpi-card-value">{value:,}</div>
        <div class="kpi-card-desc">{description}</div>
    </div>
    """, unsafe_allow_html=True)

def create_info_card(title, content):
    """Create an information card"""
    st.markdown(f"""
    <div class="info-card">
        <div class="info-card-title">{title}</div>
        <div class="info-card-text">{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_badge(text, badge_type="info"):
    """Create a styled badge"""
    return f'<span class="badge badge-{badge_type}">{text}</span>'

def section_divider(title):
    """Create a section divider"""
    st.markdown(f"""
    <div class="section-divider">
        <span>{title}</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def initialize_tables():
    """Initialize database tables on first run"""
    try:
        Customer.create_table()
        Product.create_table()
        Sale.create_table()
        SaleItem.create_table()
        
        # Fix sequences for all tables
        cur = conn.cursor()
        cur.execute("SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers))")
        cur.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products))")
        cur.execute("SELECT setval('sales_id_seq', (SELECT MAX(id) FROM sales))")
        cur.execute("SELECT setval('sale_items_id_seq', (SELECT MAX(id) FROM sale_items))")
        conn.commit()
        cur.close()
        
        st.success("✅ Database initialized successfully!")
    except Exception as e:
        st.error(f"❌ Error initializing tables: {e}")

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(page_title="Smart Inventory & Billing System", layout="wide", initial_sidebar_state="expanded")

# Apply global styling
apply_global_styling()

# Initialize tables on first run
if 'tables_initialized' not in st.session_state:
    initialize_tables()
    st.session_state.tables_initialized = True

# ============================================================================
# MAIN TITLE
# ============================================================================

st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h1 style="margin: 0; display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 2.5rem;">🏪</span>
            Smart Inventory & Billing System
        </h1>
        <p style="margin: 0.5rem 0 0 0; color: #64748B; font-size: 1rem;">
            Professional Inventory Management Dashboard
        </p>
    </div>
""", unsafe_allow_html=True)

# ============================================================================
# SIDEBAR NAVIGATION
# ============================================================================

with st.sidebar:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📦</div>
        <h2 style="margin: 0; font-size: 1.3rem; color: #4F46E5;">Smart Inventory</h2>
        <p style="margin: 0.25rem 0 0 0; color: #64748B; font-size: 0.85rem;">Modern Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <style>
    [data-testid="stRadio"] > label:first-child {
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748B;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    menu_option = st.radio(
        "NAVIGATION",
        ["📊 Dashboard", "👥 Customer Management", "📦 Product Management", "💰 Sales Management", "📈 Analytics & Reports"],
        key="main_nav"
    )

# Clean up menu option for logic
menu_option = menu_option.split(" ", 1)[1] if " " in menu_option else menu_option

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

if menu_option == "Dashboard":
    st.markdown("## 📊 Dashboard")
    st.markdown("Welcome to your inventory management system. Here's an overview of your business.")
    st.markdown("---")
    
    try:
        cur = conn.cursor()
        
        # Count customers
        cur.execute('SELECT COUNT(*) FROM customers')
        customer_count = cur.fetchone()[0]
        
        # Count products
        cur.execute('SELECT COUNT(*) FROM products')
        product_count = cur.fetchone()[0]
        
        # Count sales and revenue
        cur.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM sales')
        result = cur.fetchone()
        sales_count = result[0]
        total_revenue = float(result[1])
        
        cur.close()
        
        # Display KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_kpi_card("Total Customers", customer_count, "Customer records", "👥", "kpi-primary")
        
        with col2:
            create_kpi_card("Total Products", product_count, "Product inventory", "📦", "kpi-secondary")
        
        with col3:
            create_kpi_card("Total Sales", sales_count, "Sale transactions", "💳", "kpi-success")
        
        with col4:
            create_kpi_card("Total Revenue", f"${total_revenue:,.2f}", "Total earnings", "💰", "kpi-purple")
        
        # Quick Stats Section
        st.markdown("---")
        st.markdown("### 📈 Quick Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Low stock products
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*) FROM products WHERE quantity < 10')
            low_stock_count = cur.fetchone()[0]
            cur.close()
            
            create_info_card(
                "⚠️ Low Stock Items",
                f"{low_stock_count} product(s) with low inventory"
            )
        
        with col2:
            # Average order value
            cur = conn.cursor()
            cur.execute('SELECT AVG(total_amount) FROM sales')
            avg_order = cur.fetchone()[0]
            cur.close()
            
            create_info_card(
                "📊 Average Order Value",
                f"${avg_order:.2f}" if avg_order else "$0.00"
            )
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.info("💡 **Quick Tips:** Use the navigation menu to manage customers, products, and sales. Monitor low stock items in Analytics & Reports.")
        
    except Exception as e:
        st.error(f"❌ Error loading dashboard: {e}")

# ============================================================================
# CUSTOMER MANAGEMENT PAGE
# ============================================================================

elif menu_option == "Customer Management":
    st.markdown("## 👥 Customer Management")
    st.markdown("Manage your customers efficiently.")
    st.markdown("---")
    
    customer_action = st.radio(
        "Select Action:",
        ["View All Customers", "Add New Customer", "Update Customer", "Delete Customer"],
        horizontal=True,
        key="customer_action"
    )
    
    # View All Customers
    if customer_action == "View All Customers":
        st.markdown("### 👥 All Customers")
        
        try:
            customers = Customer.get_all_customers()
            if customers:
                # Create table manually with better styling
                st.markdown("""
                <style>
                .customer-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1rem 0;
                }
                .customer-table th {
                    background-color: #F8FAFC;
                    padding: 1rem;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #E2E8F0;
                    color: #0F172A;
                    text-transform: uppercase;
                    font-size: 0.85rem;
                    letter-spacing: 0.5px;
                }
                .customer-table td {
                    padding: 1rem;
                    border-bottom: 1px solid #E2E8F0;
                    color: #0F172A;
                }
                .customer-table tbody tr:hover {
                    background-color: rgba(79, 70, 229, 0.05);
                }
                .customer-id {
                    font-weight: 600;
                    color: #4F46E5;
                }
                </style>
                """, unsafe_allow_html=True)
                
                # Build HTML table
                table_html = "<table class='customer-table'><tr><th>ID</th><th>Customer Name</th><th>Contact Information</th></tr>"
                for customer in customers:
                    table_html += f"""
                    <tr>
                        <td><span class='customer-id'>#{customer[0]}</span></td>
                        <td><strong>{customer[1]}</strong></td>
                        <td>{customer[2]}</td>
                    </tr>
                    """
                table_html += "</table>"
                
                st.markdown(table_html, unsafe_allow_html=True)
                st.success(f"✅ Total customers: {len(customers)}")
            else:
                st.info("📭 No customers found. Add your first customer to get started!")
        except Exception as e:
            st.error(f"❌ Error retrieving customers: {e}")
    
    # Add New Customer
    elif customer_action == "Add New Customer":
        st.markdown("### ➕ Add New Customer")
        
        with st.form("add_customer_form", border=False):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("🔤 Customer Name", placeholder="John Doe")
            
            with col2:
                contact = st.text_input("📞 Contact Information", placeholder="john@example.com or +1-234-567-8900")
            
            submitted = st.form_submit_button("✅ Add Customer", use_container_width=True)
            
            if submitted:
                if name and contact:
                    try:
                        Customer.insert_customer(name, contact)
                        
                        # Refresh sequence
                        cur = conn.cursor()
                        cur.execute("SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers))")
                        conn.commit()
                        cur.close()
                        
                        st.success(f"✅ Customer '{name}' added successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error adding customer: {e}")
                else:
                    st.warning("⚠️ Please fill in all fields.")
    
    # Update Customer
    elif customer_action == "Update Customer":
        st.markdown("### ✏️ Update Customer")
        
        try:
            customers = Customer.get_all_customers()
            if customers:
                customer_dict = {f"{customer[1]} (ID: {customer[0]})": customer[0] for customer in customers}
                selected_customer = st.selectbox("Select Customer to Update", list(customer_dict.keys()))
                
                if selected_customer:
                    customer_id = customer_dict[selected_customer]
                    
                    # Get current customer data
                    cur = conn.cursor()
                    cur.execute('SELECT * FROM customers WHERE id = %s', (customer_id,))
                    customer = cur.fetchone()
                    cur.close()
                    
                    if customer:
                        with st.form("update_customer_form", border=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                name = st.text_input("🔤 Customer Name", value=customer[1])
                            
                            with col2:
                                contact = st.text_input("📞 Contact Information", value=customer[2])
                            
                            submitted = st.form_submit_button("💾 Update Customer", use_container_width=True)
                            
                            if submitted:
                                try:
                                    Customer.update_customer(customer_id, name, contact)
                                    st.success(f"✅ Customer '{name}' updated successfully!")
                                except Exception as e:
                                    st.error(f"❌ Error updating customer: {e}")
            else:
                st.info("📭 No customers available to update.")
        except Exception as e:
            st.error(f"❌ Error retrieving customers: {e}")
    
    # Delete Customer
    elif customer_action == "Delete Customer":
        st.markdown("### 🗑️ Delete Customer")
        st.warning("⚠️ Deleting a customer is a permanent action. Please be careful.")
        
        try:
            customers = Customer.get_all_customers()
            if customers:
                customer_options = {f"{customer[1]} (ID: {customer[0]})": customer[0] for customer in customers}
                selected_customer = st.selectbox("Select Customer to Delete", list(customer_options.keys()))
                
                if selected_customer:
                    col1, col2 = st.columns([2, 1])
                    
                    with col2:
                        if st.button("🗑️ Delete Customer", key="delete_customer_btn", use_container_width=True):
                            customer_id = customer_options[selected_customer]
                            try:
                                Customer.delete_customer(customer_id)
                                
                                # Refresh sequence
                                cur = conn.cursor()
                                cur.execute("SELECT setval('customers_id_seq', (SELECT MAX(id) FROM customers))")
                                conn.commit()
                                cur.close()
                                
                                st.success(f"✅ Customer '{selected_customer}' deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error deleting customer: {e}")
            else:
                st.info("📭 No customers available to delete.")
        except Exception as e:
            st.error(f"❌ Error retrieving customers: {e}")

# ============================================================================
# PRODUCT MANAGEMENT PAGE
# ============================================================================

elif menu_option == "Product Management":
    st.markdown("## 📦 Product Management")
    st.markdown("Manage your product inventory.")
    st.markdown("---")
    
    product_action = st.radio(
        "Select Action:",
        ["View All Products", "Add New Product", "Update Product", "Delete Product"],
        horizontal=True,
        key="product_action"
    )
    
    # View All Products
    if product_action == "View All Products":
        st.markdown("### 📦 All Products")
        
        try:
            products = Product.view_products()
            if products:
                st.markdown("""
                <style>
                .product-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1rem 0;
                }
                .product-table th {
                    background-color: #F8FAFC;
                    padding: 1rem;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #E2E8F0;
                    color: #0F172A;
                    text-transform: uppercase;
                    font-size: 0.85rem;
                    letter-spacing: 0.5px;
                }
                .product-table td {
                    padding: 1rem;
                    border-bottom: 1px solid #E2E8F0;
                    color: #0F172A;
                }
                .product-table tbody tr:hover {
                    background-color: rgba(79, 70, 229, 0.05);
                }
                .product-id {
                    font-weight: 600;
                    color: #4F46E5;
                }
                .stock-good { color: #10B981; font-weight: 600; }
                .stock-low { color: #F59E0B; font-weight: 600; }
                .stock-critical { color: #EF4444; font-weight: 600; }
                </style>
                """, unsafe_allow_html=True)
                
                # Build HTML table
                table_html = "<table class='product-table'><tr><th>ID</th><th>Product Name</th><th>Description</th><th>Price</th><th>Stock Level</th></tr>"
                for product in products:
                    qty = int(product[4])
                    if qty >= 10:
                        stock_class = "stock-good"
                        stock_icon = "🟢"
                    elif qty >= 5:
                        stock_class = "stock-low"
                        stock_icon = "🟠"
                    else:
                        stock_class = "stock-critical"
                        stock_icon = "🔴"
                    
                    table_html += f"""
                    <tr>
                        <td><span class='product-id'>#{product[0]}</span></td>
                        <td><strong>{product[1]}</strong></td>
                        <td style="color: #64748B; font-size: 0.9rem;">{product[2]}</td>
                        <td><strong>${product[3]:.2f}</strong></td>
                        <td><span class='{stock_class}'>{stock_icon} {qty} units</span></td>
                    </tr>
                    """
                table_html += "</table>"
                
                st.markdown(table_html, unsafe_allow_html=True)
                st.success(f"✅ Total products: {len(products)}")
            else:
                st.info("📭 No products found. Add your first product to get started!")
        except Exception as e:
            st.error(f"❌ Error retrieving products: {e}")
    
    # Add New Product
    elif product_action == "Add New Product":
        st.markdown("### ➕ Add New Product")
        
        with st.form("add_product_form", border=False):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("📝 Product Name", placeholder="Product name")
            
            with col2:
                price = st.number_input("💵 Price", min_value=0.0, step=0.01, value=0.0)
            
            description = st.text_area("📄 Description", placeholder="Product description", height=80)
            
            quantity = st.number_input("📦 Initial Quantity", min_value=0, step=1, value=0)
            
            submitted = st.form_submit_button("✅ Add Product", use_container_width=True)
            
            if submitted:
                if name and price >= 0 and quantity >= 0:
                    try:
                        Product.insert_product(name, description, price, quantity)
                        
                        # Refresh sequence
                        cur = conn.cursor()
                        cur.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products))")
                        conn.commit()
                        cur.close()
                        
                        st.success(f"✅ Product '{name}' added successfully!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"❌ Error adding product: {e}")
                else:
                    st.warning("⚠️ Please fill in all required fields correctly.")
    
    # Update Product
    elif product_action == "Update Product":
        st.markdown("### ✏️ Update Product")
        
        try:
            products = Product.view_products()
            if products:
                product_dict = {f"{product[1]} (ID: {product[0]})": product[0] for product in products}
                selected_product = st.selectbox("Select Product to Update", list(product_dict.keys()))
                
                if selected_product:
                    product_id = product_dict[selected_product]
                    product = Product.view_product_id(product_id)
                    
                    if product:
                        with st.form("update_product_form", border=False):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                name = st.text_input("📝 Product Name", value=product[1])
                            
                            with col2:
                                price = st.number_input("💵 Price", min_value=0.0, step=0.01, value=float(product[3]))
                            
                            description = st.text_area("📄 Description", value=product[2], height=80)
                            
                            quantity = st.number_input("📦 Quantity", min_value=0, step=1, value=int(product[4]))
                            
                            submitted = st.form_submit_button("💾 Update Product", use_container_width=True)
                            
                            if submitted:
                                try:
                                    Product.update_product(product_id, name, description, price, quantity)
                                    st.success(f"✅ Product '{name}' updated successfully!")
                                except Exception as e:
                                    st.error(f"❌ Error updating product: {e}")
            else:
                st.info("📭 No products available to update.")
        except Exception as e:
            st.error(f"❌ Error retrieving products: {e}")
    
    # Delete Product
    elif product_action == "Delete Product":
        st.markdown("### 🗑️ Delete Product")
        st.warning("⚠️ Deleting a product is a permanent action. Please be careful.")
        
        try:
            products = Product.view_products()
            if products:
                product_options = {f"{product[1]} (ID: {product[0]})": product[0] for product in products}
                selected_product = st.selectbox("Select Product to Delete", list(product_options.keys()))
                
                if selected_product:
                    col1, col2 = st.columns([2, 1])
                    
                    with col2:
                        if st.button("🗑️ Delete Product", key="delete_product_btn", use_container_width=True):
                            product_id = product_options[selected_product]
                            try:
                                Product.delete_product(product_id)
                                
                                # Refresh sequence
                                cur = conn.cursor()
                                cur.execute("SELECT setval('products_id_seq', (SELECT MAX(id) FROM products))")
                                conn.commit()
                                cur.close()
                                
                                st.success(f"✅ Product '{selected_product}' deleted successfully!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error deleting product: {e}")
            else:
                st.info("📭 No products available to delete.")
        except Exception as e:
            st.error(f"❌ Error retrieving products: {e}")

# ============================================================================
# SALES MANAGEMENT PAGE
# ============================================================================

elif menu_option == "Sales Management":
    st.markdown("## 💰 Sales Management")
    st.markdown("Create and manage sales transactions.")
    st.markdown("---")
    
    sales_action = st.radio(
        "Select Action:",
        ["Create New Sale", "View All Sales", "Generate Bill"],
        horizontal=True,
        key="sales_action"
    )
    
    # Create New Sale
    if sales_action == "Create New Sale":
        st.markdown("### ➕ Create New Sale")
        
        try:
            customers = Customer.get_all_customers()
            if customers:
                customer_dict = {f"{customer[1]} (ID: {customer[0]})": customer[0] for customer in customers}
                selected_customer = st.selectbox("👥 Select Customer", list(customer_dict.keys()))
                
                if selected_customer:
                    customer_id = customer_dict[selected_customer]
                    
                    with st.form("create_sale_form", border=False):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            sale_date = st.date_input("📅 Sale Date", date.today())
                        
                        with col2:
                            st.write("")  # Spacer
                        
                        submitted = st.form_submit_button("✅ Create Sale", use_container_width=True)
                        
                        if submitted:
                            try:
                                # Insert sale
                                cur = conn.cursor()
                                cur.execute('''INSERT INTO sales (customer_id, date, total_amount)
                                               VALUES (%s, %s, %s) RETURNING id''',
                                            (customer_id, sale_date, 0.0))
                                sale_id = cur.fetchone()[0]
                                conn.commit()
                                cur.close()
                                
                                # Refresh sequence
                                cur = conn.cursor()
                                cur.execute("SELECT setval('sales_id_seq', (SELECT MAX(id) FROM sales))")
                                conn.commit()
                                cur.close()
                                
                                st.session_state.new_sale_id = sale_id
                                st.session_state.new_sale_customer = selected_customer
                                st.success(f"✅ Sale #{sale_id} created successfully!")
                            except Exception as e:
                                st.error(f"❌ Error creating sale: {e}")
                    
                    # Add items to sale
                    if 'new_sale_id' in st.session_state:
                        section_divider("ADD ITEMS TO SALE")
                        
                        products = Product.view_products()
                        if products:
                            product_dict = {f"{product[1]} (ID: {product[0]})": product[0] for product in products}
                            selected_product = st.selectbox("📦 Select Product", list(product_dict.keys()), key="sale_product_select")
                            
                            if selected_product:
                                product_id = product_dict[selected_product]
                                product_details = Product.view_product_id(product_id)
                                
                                if product_details:
                                    default_price = float(product_details[3])
                                    default_quantity = 1
                                    
                                    with st.form("add_item_form", border=False):
                                        col1, col2 = st.columns(2)
                                        
                                        with col1:
                                            quantity = st.number_input("📊 Quantity", min_value=1, value=default_quantity)
                                        
                                        with col2:
                                            price = st.number_input("💵 Price per Item", min_value=0.0, value=default_price, step=0.01)
                                        
                                        submitted_item = st.form_submit_button("➕ Add Item to Sale", use_container_width=True)
                                        
                                        if submitted_item:
                                            try:
                                                # Add item to sale
                                                cur = conn.cursor()
                                                cur.execute('''INSERT INTO sale_items (sale_id, product_id, quantity, price)
                                                               VALUES (%s, %s, %s, %s)''',
                                                            (st.session_state.new_sale_id, product_id, quantity, price))
                                                conn.commit()
                                                cur.close()
                                                
                                                # Refresh sequence
                                                cur = conn.cursor()
                                                cur.execute("SELECT setval('sale_items_id_seq', (SELECT MAX(id) FROM sale_items))")
                                                conn.commit()
                                                cur.close()
                                                
                                                # Update product quantity
                                                new_quantity = product_details[4] - quantity
                                                Product.update_product(product_id, quantity=new_quantity)
                                                
                                                st.success(f"✅ {product_details[1]} added to sale!")
                                            except Exception as e:
                                                st.error(f"❌ Error adding item: {e}")
                        else:
                            st.info("📭 No products available.")
                        
                        # Show sale items
                        section_divider("CURRENT SALE ITEMS")
                        
                        try:
                            cur = conn.cursor()
                            cur.execute('''SELECT p.name, si.quantity, si.price, (si.quantity * si.price) as total
                                          FROM sale_items si JOIN products p ON si.product_id = p.id
                                          WHERE si.sale_id = %s''', (st.session_state.new_sale_id,))
                            items = cur.fetchall()
                            cur.close()
                            
                            if items:
                                st.markdown("""
                                <style>
                                .sale-item { background: #FFFFFF; padding: 1rem; border-radius: 8px; border-left: 4px solid #4F46E5; margin: 0.5rem 0; }
                                .sale-item-name { font-weight: 600; color: #0F172A; }
                                .sale-item-details { color: #64748B; font-size: 0.9rem; margin-top: 0.25rem; }
                                </style>
                                """, unsafe_allow_html=True)
                                
                                total_amount = 0
                                for item in items:
                                    item_total = float(item[1]) * float(item[2])
                                    total_amount += item_total
                                    st.markdown(f"""
                                    <div class="sale-item">
                                        <div class="sale-item-name">{item[0]}</div>
                                        <div class="sale-item-details">Qty: {int(item[1])} × ${float(item[2]):.2f} = ${float(item[3]):.2f}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                                
                                st.markdown("---")
                                
                                col1, col2, col3 = st.columns([2, 1, 1])
                                with col3:
                                    st.metric("Total", f"${total_amount:.2f}")
                                
                                # Finish sale button
                                if st.button("✅ Finish Sale", use_container_width=True, key="finish_sale"):
                                    try:
                                        cur = conn.cursor()
                                        cur.execute('UPDATE sales SET total_amount = %s WHERE id = %s',
                                                   (total_amount, st.session_state.new_sale_id))
                                        conn.commit()
                                        cur.close()
                                        
                                        st.success(f"✅ Sale completed! Total: ${total_amount:.2f}")
                                        del st.session_state.new_sale_id
                                        if 'new_sale_customer' in st.session_state:
                                            del st.session_state.new_sale_customer
                                        st.balloons()
                                    except Exception as e:
                                        st.error(f"❌ Error finalizing sale: {e}")
                        except Exception as e:
                            st.error(f"❌ Error retrieving sale items: {e}")
            else:
                st.info("📭 No customers available. Please add customers first.")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    # View All Sales
    elif sales_action == "View All Sales":
        st.markdown("### 📋 All Sales")
        
        try:
            cur = conn.cursor()
            cur.execute('''SELECT s.id, c.name, s.date, s.total_amount 
                          FROM sales s JOIN customers c ON s.customer_id = c.id 
                          ORDER BY s.date DESC''')
            sales = cur.fetchall()
            cur.close()
            
            if sales:
                st.markdown("""
                <style>
                .sales-table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 1rem 0;
                }
                .sales-table th {
                    background-color: #F8FAFC;
                    padding: 1rem;
                    text-align: left;
                    font-weight: 600;
                    border-bottom: 2px solid #E2E8F0;
                    color: #0F172A;
                    text-transform: uppercase;
                    font-size: 0.85rem;
                    letter-spacing: 0.5px;
                }
                .sales-table td {
                    padding: 1rem;
                    border-bottom: 1px solid #E2E8F0;
                    color: #0F172A;
                }
                .sales-table tbody tr:hover {
                    background-color: rgba(79, 70, 229, 0.05);
                }
                .sale-id {
                    font-weight: 600;
                    color: #4F46E5;
                }
                .sale-amount {
                    font-weight: 600;
                    color: #10B981;
                }
                </style>
                """, unsafe_allow_html=True)
                
                table_html = "<table class='sales-table'><tr><th>Sale ID</th><th>Customer</th><th>Date</th><th>Total Amount</th></tr>"
                for sale in sales:
                    table_html += f"""
                    <tr>
                        <td><span class='sale-id'>#{sale[0]}</span></td>
                        <td><strong>{sale[1]}</strong></td>
                        <td>{sale[2]}</td>
                        <td><span class='sale-amount'>${float(sale[3]):.2f}</span></td>
                    </tr>
                    """
                table_html += "</table>"
                
                st.markdown(table_html, unsafe_allow_html=True)
                st.success(f"✅ Total sales: {len(sales)}")
            else:
                st.info("📭 No sales found.")
        except Exception as e:
            st.error(f"❌ Error retrieving sales: {e}")
    
    # Generate Bill
    elif sales_action == "Generate Bill":
        st.markdown("### 📄 Generate Bill")
        
        try:
            cur = conn.cursor()
            cur.execute('SELECT id FROM sales ORDER BY id DESC')
            sales = cur.fetchall()
            cur.close()
            
            if sales:
                sale_ids = [str(sale[0]) for sale in sales]
                selected_sale_id = st.selectbox("Select Sale ID", sale_ids, format_func=lambda x: f"Sale #{x}")
                
                if st.button("📄 Generate Bill", use_container_width=True):
                    selected_sale_id = int(selected_sale_id)
                    
                    try:
                        cur = conn.cursor()
                        cur.execute('''SELECT s.id, c.name, s.date, s.total_amount 
                                      FROM sales s JOIN customers c ON s.customer_id = c.id 
                                      WHERE s.id = %s''', (selected_sale_id,))
                        sale = cur.fetchone()
                        
                        if sale:
                            # Get sale items
                            cur.execute('''SELECT p.name, si.quantity, si.price, (si.quantity * si.price) as total
                                          FROM sale_items si JOIN products p ON si.product_id = p.id
                                          WHERE si.sale_id = %s''', (selected_sale_id,))
                            items = cur.fetchall()
                            cur.close()
                            
                            # Render invoice
                            st.markdown(f"""
                            <div class="invoice-container">
                                <div class="invoice-header">
                                    <h1>SMART INVENTORY</h1>
                                    <p>Professional Billing System</p>
                                </div>
                                
                                <div class="invoice-details">
                                    <div>
                                        <div class="invoice-detail-item">
                                            <div class="invoice-detail-label">Sale ID</div>
                                            <div class="invoice-detail-value">#{sale[0]}</div>
                                        </div>
                                        <div class="invoice-detail-item">
                                            <div class="invoice-detail-label">Date</div>
                                            <div class="invoice-detail-value">{sale[2]}</div>
                                        </div>
                                    </div>
                                    <div>
                                        <div class="invoice-detail-item">
                                            <div class="invoice-detail-label">Customer</div>
                                            <div class="invoice-detail-value">{sale[1]}</div>
                                        </div>
                                    </div>
                                </div>
                                
                                <div class="invoice-items">
                                    <div class="invoice-item-header">
                                        <div style="display: grid; grid-template-columns: 2fr 1fr 1fr 1fr; gap: 1rem;">
                                            <div>Product</div>
                                            <div>Qty</div>
                                            <div>Price</div>
                                            <div>Total</div>
                                        </div>
                                    </div>
                            """, unsafe_allow_html=True)
                            
                            if items:
                                for item in items:
                                    st.markdown(f"""
                                        <div class="invoice-item-row">
                                            <div>{item[0]}</div>
                                            <div>{int(item[1])}</div>
                                            <div>${float(item[2]):.2f}</div>
                                            <div><strong>${float(item[3]):.2f}</strong></div>
                                        </div>
                                    """, unsafe_allow_html=True)
                            
                            st.markdown(f"""
                                </div>
                                
                                <div class="invoice-total">
                                    <div class="invoice-total-label">TOTAL AMOUNT</div>
                                    <div class="invoice-total-value">${float(sale[3]):.2f}</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            st.markdown("---")
                            st.success("✅ Bill generated successfully!")
                        else:
                            st.warning("Sale not found.")
                    except Exception as e:
                        st.error(f"❌ Error generating bill: {e}")
            else:
                st.info("📭 No sales available.")
        except Exception as e:
            st.error(f"❌ Error retrieving sales: {e}")

# ============================================================================
# ANALYTICS & REPORTS PAGE
# ============================================================================

elif menu_option == "Analytics & Reports":
    st.markdown("## 📈 Analytics & Reports")
    st.markdown("View detailed reports and analytics.")
    st.markdown("---")
    
    analytics_action = st.radio(
        "Select Report:",
        ["Sales Summary", "Sales by Date Range", "Top Selling Products", "Low Stock Alert", "Customer Purchase History"],
        horizontal=False,
        key="analytics_action"
    )
    
    # Sales Summary
    if analytics_action == "Sales Summary":
        st.markdown("### 📊 Sales Summary")
        
        try:
            cur = conn.cursor()
            cur.execute('SELECT COUNT(*), COALESCE(SUM(total_amount), 0) FROM sales')
            result = cur.fetchone()
            total_sales = result[0] or 0
            total_revenue = float(result[1])
            
            # Display KPI Cards
            col1, col2 = st.columns(2)
            
            with col1:
                create_kpi_card("Total Sales", total_sales, "Sale transactions", "💳", "kpi-secondary")
            
            with col2:
                create_kpi_card("Total Revenue", f"${total_revenue:,.2f}", "Total earnings", "💰", "kpi-success")
            
            # Sales by date
            cur.execute('''SELECT date, SUM(total_amount) as daily_total
                          FROM sales 
                          GROUP BY date 
                          ORDER BY date''')
            sales_data = cur.fetchall()
            cur.close()
            
            if sales_data:
                st.markdown("---")
                st.markdown("### 📈 Daily Sales Trend")
                
                # Prepare data for chart
                dates = [str(row[0]) for row in sales_data]
                amounts = [float(row[1]) for row in sales_data]
                
                import pandas as pd
                chart_data = pd.DataFrame({'Date': dates, 'Sales': amounts})
                st.line_chart(chart_data.set_index('Date'))
            else:
                st.info("📭 No sales data available for chart.")
                
        except Exception as e:
            st.error(f"❌ Error generating sales summary: {e}")
    
    # Sales by Date Range
    elif analytics_action == "Sales by Date Range":
        st.markdown("### 📅 Sales by Date Range")
        
        try:
            col1, col2 = st.columns(2)
            with col1:
                start_date = st.date_input("📅 Start Date", date.today())
            with col2:
                end_date = st.date_input("📅 End Date", date.today())
            
            if st.button("🔍 Get Sales Report", use_container_width=True):
                if start_date <= end_date:
                    cur = conn.cursor()
                    cur.execute('''SELECT s.id, c.name, s.date, s.total_amount 
                                  FROM sales s JOIN customers c ON s.customer_id = c.id 
                                  WHERE s.date BETWEEN %s AND %s
                                  ORDER BY s.date DESC''', (start_date, end_date))
                    sales_data = cur.fetchall()
                    cur.close()
                    
                    if sales_data:
                        # Display totals
                        total_sales_count = len(sales_data)
                        total_amount = sum([float(row[3]) for row in sales_data])
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            create_kpi_card("Total Sales", total_sales_count, "Transactions", "💳", "kpi-primary")
                        
                        with col2:
                            create_kpi_card("Total Revenue", f"${total_amount:,.2f}", f"{start_date} to {end_date}", "💰", "kpi-success")
                        
                        st.markdown("---")
                        st.markdown(f"### Sales from {start_date} to {end_date}")
                        
                        # Display table
                        st.markdown("""
                        <style>
                        .report-table {
                            width: 100%;
                            border-collapse: collapse;
                            margin: 1rem 0;
                        }
                        .report-table th {
                            background-color: #F8FAFC;
                            padding: 1rem;
                            text-align: left;
                            font-weight: 600;
                            border-bottom: 2px solid #E2E8F0;
                            color: #0F172A;
                            text-transform: uppercase;
                            font-size: 0.85rem;
                            letter-spacing: 0.5px;
                        }
                        .report-table td {
                            padding: 1rem;
                            border-bottom: 1px solid #E2E8F0;
                            color: #0F172A;
                        }
                        .report-table tbody tr:hover {
                            background-color: rgba(79, 70, 229, 0.05);
                        }
                        .report-amount {
                            font-weight: 600;
                            color: #10B981;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        table_html = "<table class='report-table'><tr><th>Sale ID</th><th>Customer</th><th>Date</th><th>Amount</th></tr>"
                        for row in sales_data:
                            table_html += f"""
                            <tr>
                                <td><strong>#{row[0]}</strong></td>
                                <td>{row[1]}</td>
                                <td>{row[2]}</td>
                                <td><span class='report-amount'>${float(row[3]):.2f}</span></td>
                            </tr>
                            """
                        table_html += "</table>"
                        
                        st.markdown(table_html, unsafe_allow_html=True)
                    else:
                        st.info("📭 No sales found for the selected date range.")
                else:
                    st.warning("⚠️ End date must be after start date.")
        except Exception as e:
            st.error(f"❌ Error retrieving sales data: {e}")
    
    # Top Selling Products
    elif analytics_action == "Top Selling Products":
        st.markdown("### 🏆 Top Selling Products")
        
        try:
            cur = conn.cursor()
            cur.execute('''SELECT p.name, SUM(si.quantity) as total_quantity
                          FROM sale_items si 
                          JOIN products p ON si.product_id = p.id
                          GROUP BY p.name, p.id
                          ORDER BY total_quantity DESC
                          LIMIT 10''')
            top_products = cur.fetchall()
            cur.close()
            
            if top_products:
                # Prepare chart data
                product_names = [row[0] for row in top_products]
                quantities = [int(row[1]) for row in top_products]
                
                import pandas as pd
                chart_data = pd.DataFrame({'Product': product_names, 'Units Sold': quantities})
                
                st.bar_chart(chart_data.set_index('Product'))
                
                st.markdown("---")
                st.markdown("### 📋 Product Details")
                
                for i, product in enumerate(top_products, 1):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{i}. {product[0]}**")
                    
                    with col2:
                        st.metric("Units Sold", int(product[1]))
            else:
                st.info("📭 No sales data available.")
        except Exception as e:
            st.error(f"❌ Error retrieving top selling products: {e}")
    
    # Low Stock Alert
    elif analytics_action == "Low Stock Alert":
        st.markdown("### ⚠️ Low Stock Alert")
        
        try:
            cur = conn.cursor()
            
            # Get low stock items
            cur.execute('SELECT id, name, quantity FROM products WHERE quantity < 10 ORDER BY quantity ASC')
            low_stock = cur.fetchall()
            
            # Get critical stock items
            critical_stock = [item for item in low_stock if item[2] < 5]
            warning_stock = [item for item in low_stock if 5 <= item[2] < 10]
            
            cur.close()
            
            if low_stock:
                # Critical items
                if critical_stock:
                    st.markdown("### 🔴 Critical Stock (< 5 units)")
                    for item in critical_stock:
                        st.markdown(f"""
                        <div class="info-card" style="border-left: 4px solid #EF4444;">
                            <div class="info-card-title">🔴 {item[1]}</div>
                            <div class="info-card-text"><strong>{item[2]} units</strong> remaining - Urgent reorder needed!</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Warning items
                if warning_stock:
                    st.markdown("### 🟠 Low Stock (5-10 units)")
                    for item in warning_stock:
                        st.markdown(f"""
                        <div class="info-card" style="border-left: 4px solid #F59E0B;">
                            <div class="info-card-title">🟠 {item[1]}</div>
                            <div class="info-card-text"><strong>{item[2]} units</strong> remaining - Consider reordering soon</div>
                        </div>
                        """, unsafe_allow_html=True)
            else:
                st.success("🟢 All products are well-stocked!")
        except Exception as e:
            st.error(f"❌ Error retrieving low stock products: {e}")
    
    # Customer Purchase History
    elif analytics_action == "Customer Purchase History":
        st.markdown("### 📊 Customer Purchase History")
        
        try:
            customers = Customer.get_all_customers()
            if customers:
                customer_dict = {f"{customer[1]}": customer[0] for customer in customers}
                selected_customer = st.selectbox("👥 Select Customer", list(customer_dict.keys()), key="analytics_customer")
                
                if selected_customer:
                    customer_id = customer_dict[selected_customer]
                    cur = conn.cursor()
                    cur.execute('''SELECT s.id, s.date, s.total_amount 
                                  FROM sales s 
                                  WHERE s.customer_id = %s 
                                  ORDER BY s.date DESC''', (customer_id,))
                    customer_sales = cur.fetchall()
                    cur.close()
                    
                    if customer_sales:
                        # Calculate total
                        total_purchases = sum([float(row[2]) for row in customer_sales])
                        
                        st.metric("Total Purchases", f"${total_purchases:.2f}")
                        
                        st.markdown("---")
                        st.markdown(f"### Purchase History for {selected_customer}")
                        
                        # Display table
                        st.markdown("""
                        <style>
                        .history-table {
                            width: 100%;
                            border-collapse: collapse;
                            margin: 1rem 0;
                        }
                        .history-table th {
                            background-color: #F8FAFC;
                            padding: 1rem;
                            text-align: left;
                            font-weight: 600;
                            border-bottom: 2px solid #E2E8F0;
                            color: #0F172A;
                            text-transform: uppercase;
                            font-size: 0.85rem;
                            letter-spacing: 0.5px;
                        }
                        .history-table td {
                            padding: 1rem;
                            border-bottom: 1px solid #E2E8F0;
                            color: #0F172A;
                        }
                        .history-table tbody tr:hover {
                            background-color: rgba(79, 70, 229, 0.05);
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        table_html = "<table class='history-table'><tr><th>Sale ID</th><th>Date</th><th>Amount</th></tr>"
                        for row in customer_sales:
                            table_html += f"""
                            <tr>
                                <td><strong>#{row[0]}</strong></td>
                                <td>{row[1]}</td>
                                <td><strong>${float(row[2]):.2f}</strong></td>
                            </tr>
                            """
                        table_html += "</table>"
                        
                        st.markdown(table_html, unsafe_allow_html=True)
                    else:
                        st.info(f"📭 {selected_customer} has no purchase history.")
            else:
                st.info("📭 No customers available.")
        except Exception as e:
            st.error(f"❌ Error retrieving customer purchase history: {e}")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem 0; color: #64748B; font-size: 0.85rem;">
    <p>💼 Smart Inventory & Billing System | Modern Inventory Management Dashboard</p>
    <p>Built with ❤️ for efficient business operations</p>
</div>
""", unsafe_allow_html=True)