"""
Complete setup script - runs all setup steps
"""
import os
import subprocess
import sys

def run_script(script_path, description):
    """Run a Python script and report results"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}\n")
    
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=False, 
                              text=True)
        if result.returncode == 0:
            print(f"\n✅ {description} completed successfully!")
            return True
        else:
            print(f"\n❌ {description} failed!")
            return False
    except Exception as e:
        print(f"\n❌ Error running {description}: {e}")
        return False

def main():
    print("🏦 BankSight Complete Setup")
    print("="*60)
    
    # Check if scripts directory exists
    if not os.path.exists('scripts'):
        print("❌ 'scripts' folder not found!")
        print("Please make sure you're in the correct directory.")
        return
    
    # Step 1: Data Preparation
    if not run_script('scripts/1_data_preparation.py', 'Data Generation'):
        print("\n⚠️ Setup stopped due to error in data generation")
        return
    
    # Step 2: Database Setup
    if not run_script('scripts/2_database_setup.py', 'Database Setup'):
        print("\n⚠️ Setup stopped due to error in database setup")
        return
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETE!")
    print("="*60)
    print("\nYou can now run the app with:")
    print("  streamlit run app.py")
    print("="*60)

if __name__ == "__main__":
    main()
