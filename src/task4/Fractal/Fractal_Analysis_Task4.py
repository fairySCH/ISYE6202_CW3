"""
Fractal Organization Analysis - Task 4 Main Script

Orchestrates the complete fractal factory design analysis for years 2-5.
Designs for year 4 (peak demand), then scales down for earlier years.

Execution Flow:
1. Run Fractal_Design_Task4.py - Equipment requirements analysis
2. Run Fractal_Flow_Matrix_Task4.py - Flow matrix generation
3. Run Fractal_Layout_Generator_Task4.py - Layout optimization
4. Generate summary reports and comparisons

Author: FeMoaSa Design Team
Date: November 2025
"""

import subprocess
import sys
from pathlib import Path

# Configuration
BASE_DIR = Path(__file__).parent
SCRIPTS_DIR = BASE_DIR

def run_script(script_name, description):
    """Run a Python script and check for errors"""
    script_path = SCRIPTS_DIR / script_name

    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run([sys.executable, str(script_path)],
                              capture_output=True, text=True, cwd=BASE_DIR)

        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            # Print last few lines of output for confirmation
            lines = result.stdout.strip().split('\n')
            if lines:
                print("Last output lines:")
                for line in lines[-3:]:
                    if line.strip():
                        print(f"  {line}")
        else:
            print(f"✗ {description} failed with return code {result.returncode}")
            print("Error output:")
            print(result.stderr)
            return False

    except Exception as e:
        print(f"✗ Error running {description}: {e}")
        return False

    return True

def main():
    """Main execution function"""
    print("\n" + "="*80)
    print("FRACTAL ORGANIZATION ANALYSIS - TASK 4")
    print("Multi-Year Factory Design (Years 2-5)")
    print("="*80 + "\n")

    print("Analysis Strategy:")
    print("  1. Design for Year 4 (peak demand) as baseline")
    print("  2. Scale down equipment and space for Years 2-3")
    print("  3. Generate flow matrices and layouts for all years")
    print("  4. Compare scaling efficiency across configurations")
    print()

    # Step 1: Equipment Requirements Analysis
    success = run_script("Fractal_Design_Task4.py",
                        "Equipment Requirements Analysis")

    if not success:
        print("\n❌ Equipment analysis failed. Stopping execution.")
        return

    # Step 2: Flow Matrix Generation
    success = run_script("Fractal_Flow_Matrix_Task4.py",
                        "Flow Matrix Generation")

    if not success:
        print("\n❌ Flow matrix generation failed. Stopping execution.")
        return

    # Step 3: Layout Generation
    success = run_script("Fractal_Layout_Generator_Task4.py",
                        "Layout Optimization")

    if not success:
        print("\n❌ Layout generation failed. Stopping execution.")
        return

    # Success summary
    print("\n" + "="*80)
    print("🎉 ALL FRACTAL ANALYSES COMPLETED SUCCESSFULLY!")
    print("="*80 + "\n")

    print("Generated Results:")
    print("├── Equipment Analysis:")
    print("│   ├── Year2_Fractal_f*_Equipment_Requirements.csv")
    print("│   ├── Year3_Fractal_f*_Equipment_Requirements.csv")
    print("│   ├── Year4_Fractal_f*_Equipment_Requirements.csv")
    print("│   ├── Year5_Fractal_f*_Equipment_Requirements.csv")
    print("│   ├── Fractal_Comparison_All_Years.csv")
    print("│   └── Fractal_Scaling_Analysis.csv")
    print("│")
    print("├── Flow Matrices:")
    print("│   └── year*/f*_centers/")
    print("│       ├── Single_Center_Flow_Matrix.csv")
    print("│       ├── Aggregate_Factory_Flow_Matrix.csv")
    print("│       ├── Flow_Summary.csv")
    print("│       └── Layout_Edges.csv")
    print("│")
    print("└── Layout Designs:")
    print("    └── year*/f*_layout/")
    print("        ├── Process_Locations.csv")
    print("        ├── Flow_Connections.csv")
    print("        ├── Center_Boundaries.csv")
    print("        ├── Layout_Data.json")
    print("        └── Layout_Summary.txt")

    print("\nKey Insights:")
    print("• Year 4 represents peak demand - design factory for this capacity")
    print("• Years 2-3 require ~60-80% of Year 4 equipment")
    print("• Space can be reduced proportionally to demand")
    print("• Fractal centers maintain identical process capabilities")
    print("• Flow patterns remain consistent across years")

    print("\nNext Steps:")
    print("1. Compare fractal designs with functional and part-based approaches")
    print("2. Evaluate cost implications of scaling strategy")
    print("3. Generate visualization plots for presentations")
    print("4. Document final design recommendations")

if __name__ == "__main__":
    main()