"""
Fractal Organization - Master Execution Script

Runs complete fractal organization analysis in proper sequence:
1. Equipment requirements calculation
2. Flow matrix generation
3. Layout generation
4. Comprehensive comparison analysis

This is your ONE-STOP script for all fractal analysis.

Author: FeMoaSa Design Team
Date: November 2025
"""

import sys
from pathlib import Path

BASE_DIR = Path(r"d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3")
SRC_DIR = BASE_DIR / "src"

# Add src directory to path
sys.path.insert(0, str(SRC_DIR))


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*80)
    print(title.center(80))
    print("="*80 + "\n")


def run_step(step_name, module_name):
    """Run a single analysis step"""
    print_header(f"STEP: {step_name}")
    
    try:
        module = __import__(module_name)
        if hasattr(module, 'main'):
            module.main()
        else:
            print(f"Warning: {module_name} has no main() function")
        
        print(f"\n✓ {step_name} completed successfully")
        return True
        
    except Exception as e:
        print(f"\n✗ Error in {step_name}: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Execute complete fractal analysis pipeline"""
    
    print_header("FRACTAL ORGANIZATION DESIGN - COMPLETE ANALYSIS")
    
    print("This script will execute the following steps:")
    print("  1. Calculate equipment requirements (fractal_design_main.py)")
    print("  2. Generate flow matrices (fractal_flow_matrix.py)")
    print("  3. Create factory layouts (fractal_layout_generator.py)")
    print("  4. Perform comparative analysis (fractal_comparison_analysis.py)")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    steps = [
        ("Equipment Requirements Calculation", "fractal_design_main"),
        ("Flow Matrix Generation", "fractal_flow_matrix"),
        ("Layout Generation", "fractal_layout_generator"),
        ("Comprehensive Comparison Analysis", "fractal_comparison_analysis")
    ]
    
    results = []
    
    for step_name, module_name in steps:
        success = run_step(step_name, module_name)
        results.append((step_name, success))
        
        if not success:
            print(f"\n⚠ Warning: {step_name} failed. Continue anyway? (y/n)")
            response = input().strip().lower()
            if response != 'y':
                print("\nExecution stopped by user.")
                break
    
    # Print summary
    print_header("EXECUTION SUMMARY")
    
    print("Analysis Steps Completed:\n")
    for step_name, success in results:
        status = "✓ SUCCESS" if success else "✗ FAILED"
        print(f"  {status:12} - {step_name}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n{successful}/{total} steps completed successfully")
    
    if successful == total:
        print_header("ALL ANALYSIS COMPLETE - FILES GENERATED")
        print("""
Equipment Requirements:
  - Fractal_f2_Equipment_Requirements.csv
  - Fractal_f3_Equipment_Requirements.csv
  - Fractal_f4_Equipment_Requirements.csv
  - Fractal_f5_Equipment_Requirements.csv
  - Fractal_Comparison_All_Scenarios.csv

Flow Matrices (in fractal_flow_matrices/):
  - f2_centers/Single_Center_Flow_Matrix.csv
  - f2_centers/Aggregate_Factory_Flow_Matrix.csv
  - (same for f3, f4, f5)

Layouts (in fractal_layouts/):
  - f2_layout/Process_Locations.csv
  - f2_layout/Flow_Connections.csv
  - f2_layout/Center_Boundaries.csv
  - (same for f3, f4)

Comparison & Recommendations:
  - Organization_Design_Comparison.csv
  - Fractal_Recommendation_Report.txt
  - Fractal_Radar_Chart_Data.csv

NEXT STEPS:
1. Review Fractal_Recommendation_Report.txt for design guidance
2. Use Process_Locations.csv and Flow_Connections.csv to draw layout
3. Import Center_Boundaries.csv to show fractal center zones
4. Use comparison data for presentation/documentation
        """)
    else:
        print("\n⚠ Some steps failed. Check error messages above.")
    
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExecution cancelled by user.")
    except Exception as e:
        print(f"\n\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
