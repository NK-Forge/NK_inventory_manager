#!/usr/bin/env python3
"""
Smart Inventory Management & Analysis Tool
Portfolio Sample - Demonstrates Python automation for small businesses

Features:
- Processes inventory CSV files
- Generates reorder alerts for low stock
- Creates visual reports and analytics
- Exports cleaned data and summaries
- Handles multiple product categories

Target Business Value: $800-1500 automation projects
"""

import pandas as pd
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore
from datetime import datetime
import numpy as np
import os

class InventoryManager:
    def __init__(self):
        self.df = None
        self.low_stock_threshold = 20
        self.reorder_days = 30
        
    def load_inventory_data(self, csv_file):
        """Load and validate inventory data from CSV file"""
        try:
            self.df = pd.read_csv(csv_file)
            print(f"✅ Loaded {len(self.df)} products from {csv_file}")
            
            # Clean and standardize data
            self.df.columns = self.df.columns.str.strip().str.lower().str.replace(' ', '_')
            
            # Ensure required columns exist
            required_cols = ['product_name', 'current_stock', 'price', 'category']
            missing_cols = [col for col in required_cols if col not in self.df.columns]
            
            if missing_cols:
                print(f"⚠️  Missing columns: {missing_cols}")
                print("Available columns:", list(self.df.columns))
                return False
                
            # Clean data types
            self.df['current_stock'] = pd.to_numeric(self.df['current_stock'], errors='coerce').fillna(0)
            self.df['price'] = pd.to_numeric(self.df['price'], errors='coerce').fillna(0)
            
            # Calculate inventory value
            self.df['inventory_value'] = self.df['current_stock'] * self.df['price']
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def generate_sample_data(self, filename="sample_inventory.csv", num_products=50):
        """Generate realistic sample inventory data for demonstration"""
        np.random.seed(42)  # For consistent demo data
        
        # Create logical product-category pairs
        product_categories = [
            ('Wireless Headphones', 'Electronics'), ('Smartphone Case', 'Electronics'), 
            ('Laptop Stand', 'Electronics'), ('USB Cable', 'Electronics'),
            ('Cotton T-Shirt', 'Clothing'), ('Jeans', 'Clothing'), 
            ('Winter Jacket', 'Clothing'), ('Running Shoes', 'Clothing'),
            ('Garden Tools', 'Home & Garden'), ('Plant Pot', 'Home & Garden'), 
            ('LED Light', 'Home & Garden'), ('Storage Box', 'Home & Garden'),
            ('Basketball', 'Sports'), ('Yoga Mat', 'Sports'), 
            ('Protein Powder', 'Sports'), ('Water Bottle', 'Sports'),
            ('Fiction Novel', 'Books'), ('Cookbook', 'Books'), 
            ('Art Supplies', 'Books'), ('Notebook', 'Books'),
            ('Face Cream', 'Beauty'), ('Shampoo', 'Beauty'), 
            ('Makeup Brush', 'Beauty'), ('Perfume', 'Beauty')
        ]
        
        # Generate sample data with correct category matching
        data = []
        for i in range(num_products):
            # Select a random product-category pair
            product_name, category = product_categories[i % len(product_categories)]
            
            # Add variety to make each product unique but realistic
            if category == 'Electronics':
                product_name = f"{product_name} - {['Black', 'White', 'Silver', 'Blue'][i % 4]}"
            elif category == 'Clothing':
                product_name = f"{product_name} - Size {['S', 'M', 'L', 'XL'][i % 4]}"
            elif category == 'Sports':
                product_name = f"{product_name} - {['Pro', 'Standard', 'Premium', 'Basic'][i % 4]}"
            elif category == 'Beauty':
                if 'Brush' in product_name:
                    product_name = f"{product_name} - {['Small', 'Medium', 'Large', 'Travel'][i % 4]}"
                else:  # For liquids like shampoo, perfume, face cream
                    product_name = f"{product_name} - {['50ml', '100ml', '150ml', '200ml'][i % 4]}"
            elif category == 'Books':
                product_name = f"{product_name} - {['Hardcover', 'Paperback', 'Large Print', 'Deluxe'][i % 4]}"
            else:  # Home & Garden
                product_name = f"{product_name} - {['Small', 'Medium', 'Large', 'Extra Large'][i % 4]}"
            
            current_stock = np.random.randint(0, 200)
            price = round(np.random.uniform(5.99, 299.99), 2)
            supplier = f"Supplier_{np.random.randint(1, 10)}"
            
            data.append({
                'Product Name': product_name,
                'Category': category,
                'Current Stock': current_stock,
                'Price': price,
                'Supplier': supplier,
                'Last Updated': datetime.now().strftime('%Y-%m-%d')
            })
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"📊 Generated sample data: {filename}")
        return filename
    
    def analyze_low_stock(self):
        """Identify products that need reordering"""
        if self.df is None:
            print("❌ No data loaded. Please load inventory data first.")
            return None
            
        low_stock = self.df[self.df['current_stock'] <= self.low_stock_threshold].copy()
        low_stock = low_stock.sort_values('current_stock')
        
        print(f"\n🚨 LOW STOCK ALERT - {len(low_stock)} products need attention:")
        print("="*60)
        
        if len(low_stock) > 0:
            for _, product in low_stock.iterrows():
                urgency = "🔴 CRITICAL" if product['current_stock'] <= 5 else "🟡 LOW"
                print(f"{urgency} {product['product_name']}")
                print(f"   Stock: {product['current_stock']} | Value: ${product['inventory_value']:.2f}")
                print(f"   Category: {product['category']}")
                print("-" * 40)
        else:
            print("✅ All products have adequate stock levels!")
            
        return low_stock
    
    def category_analysis(self):
        """Analyze inventory by category"""
        if self.df is None:
            return None
            
        category_stats = self.df.groupby('category').agg({
            'current_stock': ['sum', 'count', 'mean'],
            'inventory_value': ['sum', 'mean'],
            'price': 'mean'
        }).round(2)
        
        category_stats.columns = ['Total_Stock', 'Product_Count', 'Avg_Stock', 
                                'Total_Value', 'Avg_Value', 'Avg_Price']
        
        print("\n📊 INVENTORY BY CATEGORY:")
        print("="*80)
        print(category_stats.to_string())
        
        return category_stats
    
    def create_visual_reports(self, output_dir="inventory_reports"):
        """Generate visual reports and charts"""
        if self.df is None:
            return False
            
        os.makedirs(output_dir, exist_ok=True)
        
        # Set style for professional charts
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # 1. Stock Levels by Category
        plt.figure(figsize=(12, 6))
        category_stock = self.df.groupby('category')['current_stock'].sum()
        plt.subplot(1, 2, 1)
        category_stock.plot(kind='bar', color='skyblue')
        plt.title('Total Stock by Category', fontsize=14, fontweight='bold')
        plt.xlabel('Category')
        plt.ylabel('Total Stock')
        plt.xticks(rotation=45)
        
        # 2. Inventory Value Distribution
        plt.subplot(1, 2, 2)
        category_value = self.df.groupby('category')['inventory_value'].sum()
        plt.pie(category_value.values, labels=category_value.index, autopct='%1.1f%%')
        plt.title('Inventory Value Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(f'{output_dir}/category_analysis.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # 3. Low Stock Alert Chart
        low_stock = self.df[self.df['current_stock'] <= self.low_stock_threshold]
        if len(low_stock) > 0:
            plt.figure(figsize=(10, 6))
            low_stock_sorted = low_stock.sort_values('current_stock').head(10)
            plt.barh(range(len(low_stock_sorted)), low_stock_sorted['current_stock'], 
                    color='red', alpha=0.7)
            plt.yticks(range(len(low_stock_sorted)), 
                      [name[:30] + '...' if len(name) > 30 else name 
                       for name in low_stock_sorted['product_name']])
            plt.xlabel('Current Stock')
            plt.title('Top 10 Products Needing Restock', fontsize=14, fontweight='bold')
            plt.axvline(x=self.low_stock_threshold, color='orange', linestyle='--', 
                       label=f'Reorder Threshold ({self.low_stock_threshold})')
            plt.legend()
            plt.tight_layout()
            plt.savefig(f'{output_dir}/low_stock_alert.png', dpi=300, bbox_inches='tight')
            plt.close()
        
        print(f"📈 Visual reports saved to '{output_dir}/' directory")
        return True
    
    def generate_reorder_report(self, output_file="reorder_report.csv"):
        """Generate CSV report of items to reorder"""
        if self.df is None:
            return False
            
        low_stock = self.df[self.df['current_stock'] <= self.low_stock_threshold].copy()
        
        # Calculate suggested reorder quantities
        low_stock['suggested_reorder'] = np.maximum(50 - low_stock['current_stock'], 20)
        low_stock['estimated_cost'] = low_stock['suggested_reorder'] * low_stock['price']
        
        # Select and rename columns for the report
        reorder_report = low_stock[['product_name', 'category', 'current_stock', 
                                  'suggested_reorder', 'price', 'estimated_cost']].copy()
        
        reorder_report.columns = ['Product', 'Category', 'Current_Stock', 
                                'Suggested_Reorder', 'Unit_Price', 'Estimated_Cost']
        
        # Add totals row
        totals = {
            'Product': 'TOTAL',
            'Category': '',
            'Current_Stock': '',
            'Suggested_Reorder': reorder_report['Suggested_Reorder'].sum(),
            'Unit_Price': '',
            'Estimated_Cost': reorder_report['Estimated_Cost'].sum()
        }
        reorder_report = pd.concat([reorder_report, pd.DataFrame([totals])], ignore_index=True)
        
        reorder_report.to_csv(output_file, index=False)
        print(f"📋 Reorder report saved: {output_file}")
        print(f"💰 Total estimated reorder cost: ${totals['Estimated_Cost']:.2f}")
        
        return reorder_report
    
    def run_full_analysis(self, csv_file=None):
        """Run complete inventory analysis workflow - demonstrates full business solution"""
        print("🚀 SMART INVENTORY ANALYSIS STARTING...")
        print("="*50)
        
        # Load data (or generate sample if no file provided)
        if csv_file is None:
            csv_file = self.generate_sample_data()
            
        if not self.load_inventory_data(csv_file):
            return False
        
        # Run all analyses and actually use the results
        print(f"\n📦 Total Products: {len(self.df)}")
        print(f"💰 Total Inventory Value: ${self.df['inventory_value'].sum():.2f}")
        
        # Analyze low stock and use the results
        low_stock_items = self.analyze_low_stock()
        critical_items = low_stock_items[low_stock_items['current_stock'] <= 5]
        print(f"🔴 Critical stock items (≤5 units): {len(critical_items)}")
        
        # Category analysis and use the results  
        category_stats = self.category_analysis()
        highest_value_category = category_stats['Total_Value'].idxmax()
        lowest_stock_category = category_stats['Total_Stock'].idxmin()
        print(f"💎 Highest value category: {highest_value_category}")
        print(f"⚠️  Lowest stock category: {lowest_stock_category}")
        
        # Generate reports and use the data
        self.create_visual_reports()
        reorder_report = self.generate_reorder_report()
        
        # Extract insights from reorder report
        if len(reorder_report) > 1:  # Has data beyond totals row
            total_items_to_reorder = len(reorder_report) - 1
            total_reorder_cost = reorder_report.iloc[-1]['Estimated_Cost']
            avg_reorder_cost = reorder_report[:-1]['Estimated_Cost'].mean()  # Exclude totals row
            
            print("\n💰 REORDER ANALYSIS:")
            print(f"Items needing reorder: {total_items_to_reorder}")
            print(f"Total reorder investment: ${total_reorder_cost:.2f}")
            print(f"Average cost per item: ${avg_reorder_cost:.2f}")
        
        print("\n✅ ANALYSIS COMPLETE!")
        print("Files generated:")
        print("  📊 Visual reports: inventory_reports/")
        print("  📋 Reorder report: reorder_report.csv")
        print("  📈 Sample data: sample_inventory.csv")
        
        return True

    def run_demo_workflow(self, csv_file=None):
        """Alternative demo showing individual method capabilities"""
        if csv_file is None:
            csv_file = self.generate_sample_data(num_products=75)
        return self.load_inventory_data(csv_file)


def main():
    """Main function to demonstrate the inventory management tool"""
    print("🏪 SMART INVENTORY MANAGEMENT TOOL")
    print("Portfolio Sample by [Your Name]")
    print("="*50)
    
    # Initialize the inventory manager
    manager = InventoryManager()
    
    print("Choose demo mode:")
    print("1. Full Business Analysis (recommended)")
    print("2. Individual Feature Demo")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "2":
        print("\nRunning Individual Feature Demo...\n")
        success = manager.run_demo_workflow()
        if not success:
            print("❌ Failed to load data")
            return
            
        # Run individual demos here
        print("\n📦 INVENTORY OVERVIEW:")
        print(f"Total Products: {len(manager.df)}")
        print(f"Total Inventory Value: ${manager.df['inventory_value'].sum():.2f}")
        print(f"Average Product Value: ${manager.df['inventory_value'].mean():.2f}")
        
        # Individual feature demonstrations
        low_stock_items = manager.analyze_low_stock()
        print(f"Found {len(low_stock_items)} items below threshold")
        
        category_stats = manager.category_analysis()
        top_category = category_stats['Total_Value'].idxmax()
        print(f"Highest value category: {top_category}")
        
        print("\n📊 Generating visual reports...")
        manager.create_visual_reports()
        
        print("📋 Creating reorder report...")
        reorder_report = manager.generate_reorder_report()
        
        # Use the reorder report data
        if len(reorder_report) > 1:  # Has data beyond totals row
            items_to_reorder = len(reorder_report) - 1
            total_cost = reorder_report.iloc[-1]['Estimated_Cost']
            print(f"Reorder report: {items_to_reorder} items need restocking")
            print(f"Total reorder cost: ${total_cost:.2f}")
        else:
            print("No items currently need reordering")
        
        print("\n✅ Individual feature demo complete!")
        
    else:  # Default to option 1
        if choice not in ["1", ""]:
            print(f"Invalid choice '{choice}', defaulting to Full Business Analysis...")
        print("\nRunning Full Business Analysis...\n")
        
        success = manager.run_full_analysis()
        
        if success:
            print("\n💡 BUSINESS VALUE DEMONSTRATED:")
            print("✅ Complete inventory workflow automation")
            print("✅ Actionable insights and recommendations") 
            print("✅ Professional reporting and visualizations")
            print("✅ Cost analysis and budgeting tools")
            print("✅ Category performance tracking")
            print("\n🎯 Perfect for: Retail stores, warehouses, e-commerce businesses")
            print("💼 Custom implementations available for your specific business needs")


if __name__ == "__main__":
    main()