"""
Run all layout generators for all years
"""
import subprocess
from pathlib import Path

years = {
    'Year 1 (Task 3)': Path(__file__).parent / "results" / "Task3" / "Part" / "Jatin",
    'Year 2': Path(__file__).parent / "results" / "task4" / "part" / "Jatin" / "Year2",
    'Year 3': Path(__file__).parent / "results" / "task4" / "part" / "Jatin" / "Year3",
    'Year 4': Path(__file__).parent / "results" / "task4" / "part" / "Jatin" / "Year4",
    'Year 5': Path(__file__).parent / "results" / "task4" / "part" / "Jatin" / "Year5",
}

print("Regenerating all layout visualizations...")
print("=" * 70)

for year_name, year_path in years.items():
    script = year_path / "optimized_layout_generator.py"
    if script.exists():
        print(f"\n{year_name}:")
        result = subprocess.run(
            ['python', str(script)],
            cwd=str(year_path),
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(f"  ✓ Layout generated successfully")
        else:
            print(f"  ✗ Error generating layout:")
            print(f"     {result.stderr[:200]}")
    else:
        print(f"\n{year_name}: Script not found at {script}")

print("\n" + "=" * 70)
print("All layouts regenerated!")
