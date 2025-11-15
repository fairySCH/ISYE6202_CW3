"""
fractal organization analysis - task 4 main script

this script orchestrates the complete fractal factory design analysis for years 2-5.
it designs for year 4 (peak demand), then scales down for earlier years.

execution flow:
1. run fractal_design_task4.py - equipment requirements analysis
2. run fractal_flow_matrix_task4.py - flow matrix generation
3. generate summary reports and comparisons

team: machas^2
date: november 2025
"""

import subprocess
import sys
from pathlib import Path

# configuration
BASE_DIR = Path(__file__).parent
SCRIPTS_DIR = BASE_DIR

def run_script(script_name, description):
    """run a python script and check for errors"""
    script_path = SCRIPTS_DIR / script_name

    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run([sys.executable, str(script_path)],
                              capture_output=True, text=True, cwd=BASE_DIR)

        if result.returncode == 0:
            print(f"✓ {description} completed successfully")
            # print last few lines of output for confirmation
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

    # step 1: equipment requirements analysis
    success = run_script("Fractal_Design_Task4.py",
                        "Equipment Requirements Analysis")

    if not success:
        print("\n❌ Equipment analysis failed. Stopping execution.")
        return

    # step 2: flow matrix generation
    success = run_script("Fractal_Flow_Matrix_Task4.py",
                        "Flow Matrix Generation")

    if not success:
        print("\n❌ Flow matrix generation failed. Stopping execution.")
        return

    # step 3: layout generation
    success = run_script("Fractal_Layout_Generator_Task4.py",
                        "Layout Optimization")

    if not success:
        print("\n❌ Layout generation failed. Stopping execution.")
        return

    # step 4: visualization generation
    success = run_script("Fractal_Visualization_Task4.py",
                        "Layout Visualization")

    if not success:
        print("\n❌ Visualization generation failed. Stopping execution.")
        return

    # step 5: cost analysis
    success = run_script("Fractal_Cost_Analysis_Task4.py",
                        "Cost Analysis")

    if not success:
        print("\n❌ Cost analysis failed. Stopping execution.")
        return

    # success summary
    print("\n" + "="*80)
    print("🎉 ALL FRACTAL ANALYSES COMPLETED SUCCESSFULLY!")
    print("="*80 + "\n")

    print("Generated Results:")
    print("+- Equipment Analysis:")
    print("|   +- Year2_Fractal_f*_Equipment_Requirements.csv")
    print("|   +- Year3_Fractal_f*_Equipment_Requirements.csv")
    print("|   +- Year4_Fractal_f*_Equipment_Requirements.csv")
    print("|   +- Year5_Fractal_f*_Equipment_Requirements.csv")
    print("|   +- Fractal_Comparison_All_Years.csv")
    print("|   +- Fractal_Scaling_Analysis.csv")
    print("|")
    print("+- Flow Matrices:")
    print("|   +- year*/f*_centers/")
    print("|       +- Single_Center_Flow_Matrix.csv")
    print("|       +- Aggregate_Factory_Flow_Matrix.csv")
    print("|       +- Flow_Summary.csv")
    print("|       +- Layout_Edges.csv")
    print("|")
    print("+- Layout Designs:")
    print("|   +- year*/f*_layout/")
    print("|       +- Process_Locations.csv")
    print("|       +- Flow_Connections.csv")
    print("|       +- Center_Boundaries.csv")
    print("|       +- Layout_Data.json")
    print("|       +- Layout_Summary.txt")
    print("|")
    print("+- Visualizations:")
    print("|   +- Year*_Fractal_f*_Layout.png")
    print("|   +- Fractal_Scaling_Comparison.png")
    print("|   +- Fractal_Yearly_Equipment_Comparison.png")
    print("|")
    print("+- Cost Analysis:")
    print("    +- Cost_Analysis/")
    print("    |   +- Fractal_Cost_Analysis_Summary.txt")
    print("    |   +- Fractal_Cost_Summary.csv")
    print("    +- Fractal_Visuals/")
    print("        +- Fractal_Capital_Investment_Comparison.png")
    print("        +- Fractal_Operating_Cost_Comparison.png")
    print("        +- Fractal_Cost_Efficiency_Analysis.png")

    print("\nKey Insights:")
    print("• Year 4 represents peak demand - design factory for this capacity")
    print("• Years 2-3 require ~60-80% of Year 4 equipment")
    print("• Space can be reduced proportionally to demand")
    print("• Fractal centers maintain identical process capabilities")
    print("• Flow patterns remain consistent across years")

    print("\nNext Steps:")
    print("1. Compare fractal designs with functional and part-based approaches")
    print("2. Evaluate cost implications of scaling strategy")
    print("3. Review generated visualizations and cost analysis reports")
    print("4. Document final design recommendations")

if __name__ == "__main__":
    main()