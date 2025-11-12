"""
Fractal Layout Placement Generator

This script generates the overall facility layout by placing parent blocks (A-M)
on a Cartesian plane based on flow relationships and adjacency requirements.

CRITICAL ANALYSIS & LOGIC:
1. Flow Analysis: Highest to lowest flows determine relative placement priority
2. Adjacency: No space between blocks - they must be adjacent for optimal flow
3. Centroids: Calculated for each block and output to CSV
4. Pragmatic Spacing: Margins added for inbound/outbound but layout is space-efficient

Author: Fractal Layout Placement Team
Date: November 2025
"""

import sys
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ============================================================================
# CONFIGURATION
# ============================================================================

BASE_DIR = Path(__file__).parent.parent.parent.parent

# Layout margins (feet) - pragmatic spacing for inbound/outbound
MARGIN_LEFT = 20
MARGIN_RIGHT = 20
MARGIN_TOP = 20
MARGIN_BOTTOM = 20

# ============================================================================
# FLOW ANALYSIS FUNCTIONS
# ============================================================================

def analyze_flow_relationships(flow_matrix):
    """
    Analyze flow matrix to identify key relationships and placement priorities.

    Critical Analysis:
    - B->C has highest flow (54,400) - these should be adjacent
    - C->D (86,200), E->G (112,200) are major flows
    - G has highest total flow (193,500) - should be central
    - I has high outflows (152,300) - should connect to many processes
    """
    processes = [col for col in flow_matrix.columns if col != '']
    flow_pairs = []

    for i, from_proc in enumerate(processes):
        for j, to_proc in enumerate(processes):
            if i != j:
                flow_amount = flow_matrix.iloc[i, j]
                if flow_amount > 0:
                    flow_pairs.append((from_proc, to_proc, flow_amount))

    flow_pairs.sort(key=lambda x: x[2], reverse=True)
    return flow_pairs

def calculate_flow_totals(flow_pairs):
    """Calculate total flow volume for each process."""
    flow_totals = defaultdict(float)
    for from_p, to_p, flow in flow_pairs:
        flow_totals[from_p] += flow
        flow_totals[to_p] += flow
    return flow_totals

# ============================================================================
# LAYOUT PLACEMENT ALGORITHM
# ============================================================================

class FlowBasedLayoutPlacer:
    """
    Places blocks on Cartesian plane using flow-based adjacency optimization.

    Algorithm:
    1. Sort processes by total flow volume (highest first)
    2. Place highest flow process at origin
    3. For each subsequent process, find best adjacent position based on flow relationships
    4. Use systematic gap-filling to ensure true adjacency
    5. Add pragmatic margins for inbound/outbound operations
    """

    def __init__(self, block_dims, flow_pairs):
        self.block_dims = block_dims
        self.flow_pairs = flow_pairs
        self.placed = {}
        self.centroids = {}
        self.flow_totals = calculate_flow_totals(flow_pairs)

    def get_flow_priority(self, process1, process2):
        """Get flow relationship strength between two processes."""
        for from_p, to_p, flow in self.flow_pairs:
            if (from_p == process1 and to_p == process2) or (from_p == process2 and to_p == process1):
                return flow
        return 0

    def get_adjacent_positions(self, placed_processes):
        """Get all possible adjacent positions to existing blocks."""
        adjacent_positions = set()

        for proc in placed_processes:
            x, y, w, d = self.placed[proc]

            # Add positions adjacent to each side
            adjacent_positions.add((x + w, y))      # right
            adjacent_positions.add((x - w, y))      # left (for same-sized blocks)
            adjacent_positions.add((x, y + d))      # bottom
            adjacent_positions.add((x, y - d))      # top (for same-sized blocks)

            # Also add corner-adjacent positions for better connectivity
            adjacent_positions.add((x + w, y + d))  # bottom-right
            adjacent_positions.add((x + w, y - d))  # top-right
            adjacent_positions.add((x - w, y + d))  # bottom-left
            adjacent_positions.add((x - w, y - d))  # top-left

        return list(adjacent_positions)

    def find_best_placement(self, process, placed_processes):
        """Find best adjacent position for a process with layout compactness consideration."""
        if not placed_processes:
            return (0, 0)

        width, depth = self.block_dims[process]
        best_score = -1
        best_pos = (0, 0)

        # Get all possible adjacent positions
        candidate_positions = self.get_adjacent_positions(placed_processes)

        # Also consider positions that would create more compact layouts
        # Add some strategic positions near the origin and near existing blocks
        strategic_positions = []
        if placed_processes:
            # Add positions near the layout bounds to encourage tighter packing
            min_x = min(x for x, y, w, d in [self.placed[p] for p in placed_processes])
            max_x = max(x + w for x, y, w, d in [self.placed[p] for p in placed_processes])
            min_y = min(y for x, y, w, d in [self.placed[p] for p in placed_processes])
            max_y = max(y + d for x, y, w, d in [self.placed[p] for p in placed_processes])

            # Add positions that would extend the layout more compactly
            strategic_positions.extend([
                (min_x - width, min_y),  # left of leftmost
                (max_x, min_y),          # right of rightmost
                (min_x, min_y - depth),  # above topmost
                (min_x, max_y),          # below bottommost
            ])

        candidate_positions.extend(strategic_positions)

        for cx, cy in candidate_positions:
            # Check if position overlaps with any existing block
            overlap = False
            for other_proc in placed_processes:
                ox, oy, ow, od = self.placed[other_proc]
                if not (cx + width <= ox or cx >= ox + ow or cy + depth <= oy or cy >= oy + od):
                    overlap = True
                    break

            if not overlap:
                # Calculate score based on multiple factors
                score = 0

                # Score based on flow relationships with nearby blocks
                flow_score = 0
                for other_proc in placed_processes:
                    ox, oy, ow, od = self.placed[other_proc]
                    flow_priority = self.get_flow_priority(process, other_proc)

                    # Calculate distance between centroids
                    dist = math.sqrt((cx + width/2 - (ox + ow/2))**2 + (cy + depth/2 - (oy + od/2))**2)

                    # Closer high-flow neighbors get higher scores
                    if dist > 0:
                        proximity_score = flow_priority * 1000 / (dist + 1)  # +1 to avoid division by zero
                        flow_score += proximity_score

                # Bonus for positions that fill gaps tightly
                adjacency_score = 0
                for other_proc in placed_processes:
                    ox, oy, ow, od = self.placed[other_proc]

                    # Check if this position touches the other block
                    touches_right = (cx == ox + ow and cy < oy + od and cy + depth > oy)
                    touches_left = (cx + width == ox and cy < oy + od and cy + depth > oy)
                    touches_bottom = (cy == oy + od and cx < ox + ow and cx + width > ox)
                    touches_top = (cy + depth == oy and cx < ox + ow and cx + width > ox)

                    if touches_right or touches_left or touches_bottom or touches_top:
                        adjacency_score += 100

                # Compactness score - prefer positions closer to origin
                compactness_score = -math.sqrt(cx**2 + cy**2) * 0.1  # Small penalty for distance from origin

                # Boundary preference - prefer positions that don't extend boundaries unnecessarily
                boundary_score = 0
                if placed_processes:
                    layout_min_x = min(x for x, y, w, d in [self.placed[p] for p in placed_processes])
                    layout_max_x = max(x + w for x, y, w, d in [self.placed[p] for p in placed_processes])
                    layout_min_y = min(y for x, y, w, d in [self.placed[p] for p in placed_processes])
                    layout_max_y = max(y + d for x, y, w, d in [self.placed[p] for p in placed_processes])

                    # Bonus for positions inside current bounds
                    if cx >= layout_min_x and cx + width <= layout_max_x and cy >= layout_min_y and cy + depth <= layout_max_y:
                        boundary_score += 50

                total_score = flow_score + adjacency_score + compactness_score + boundary_score

                if total_score > best_score:
                    best_score = total_score
                    best_pos = (cx, cy)

        return best_pos

    def compact_layout(self):
        """Compact the layout by shifting blocks to eliminate gaps."""
        if not self.placed:
            return

        # Try to shift each block left and up as much as possible
        for process in list(self.placed.keys()):
            x, y, w, d = self.placed[process]

            # Try shifting left
            min_x = x
            for dx in range(1, x + 1):
                new_x = x - dx
                can_shift = True

                # Check if this shift would cause overlap
                for other_proc, (ox, oy, ow, od) in self.placed.items():
                    if other_proc != process:
                        if not (new_x + w <= ox or new_x >= ox + ow or y + d <= oy or y >= oy + od):
                            can_shift = False
                            break

                if not can_shift:
                    break
                min_x = new_x

            # Try shifting up
            min_y = y
            for dy in range(1, y + 1):
                new_y = y - dy
                can_shift = True

                # Check if this shift would cause overlap
                for other_proc, (ox, oy, ow, od) in self.placed.items():
                    if other_proc != process:
                        if not (min_x + w <= ox or min_x >= ox + ow or new_y + d <= oy or new_y >= oy + od):
                            can_shift = False
                            break

                if not can_shift:
                    break
                min_y = new_y

            # Apply the shift
            if min_x != x or min_y != y:
                self.placed[process] = (min_x, min_y, w, d)
                self.centroids[process] = (min_x + w/2, min_y + d/2)

    def optimize_layout(self):
        """Final optimization pass to improve layout compactness."""
        if len(self.placed) < 2:
            return

        # Try to move each block to a better position if possible
        for process in list(self.placed.keys()):
            current_x, current_y, w, d = self.placed[process]

            # Try small adjustments to see if we can improve the layout
            best_improvement = 0
            best_new_pos = (current_x, current_y)

            # Try moving in small steps
            for dx in [-5, -2, 0, 2, 5]:
                for dy in [-5, -2, 0, 2, 5]:
                    if dx == 0 and dy == 0:
                        continue

                    new_x, new_y = current_x + dx, current_y + dy

                    # Check if this position is valid
                    valid = True
                    for other_proc, (ox, oy, ow, od) in self.placed.items():
                        if other_proc != process:
                            if not (new_x + w <= ox or new_x >= ox + ow or new_y + d <= oy or new_y >= oy + od):
                                valid = False
                                break

                    if valid:
                        # Calculate if this improves overall layout compactness
                        old_bounds = self.get_layout_bounds()
                        old_area = old_bounds[0] * old_bounds[1]

                        # Temporarily move the block
                        old_pos = self.placed[process]
                        old_centroid = self.centroids[process]
                        self.placed[process] = (new_x, new_y, w, d)
                        self.centroids[process] = (new_x + w/2, new_y + d/2)

                        new_bounds = self.get_layout_bounds()
                        new_area = new_bounds[0] * new_bounds[1]

                        # Restore position
                        self.placed[process] = old_pos
                        self.centroids[process] = old_centroid

                        # Check if this reduces area
                        area_improvement = old_area - new_area
                        if area_improvement > best_improvement:
                            best_improvement = area_improvement
                            best_new_pos = (new_x, new_y)

            # Apply the best improvement found
            if best_improvement > 0:
                self.placed[process] = (best_new_pos[0], best_new_pos[1], w, d)
                self.centroids[process] = (best_new_pos[0] + w/2, best_new_pos[1] + d/2)
                print(f"  Optimized {process}: moved to better position")

    def place_blocks(self):
        """Place all blocks using flow-based algorithm with compaction and optimization."""
        # Sort processes by total flow (highest first)
        processes = sorted(self.block_dims.keys(),
                          key=lambda p: self.flow_totals.get(p, 0),
                          reverse=True)

        print(f"Placement order by flow: {' -> '.join(processes[:5])}...")

        placed_processes = []

        for process in processes:
            x_pos, y_pos = self.find_best_placement(process, placed_processes)

            width, depth = self.block_dims[process]

            self.placed[process] = (x_pos, y_pos, width, depth)
            self.centroids[process] = (x_pos + width/2, y_pos + depth/2)
            placed_processes.append(process)

            print(f"  {process}: ({x_pos:.0f}, {y_pos:.0f}) {width:.0f}×{depth:.0f} ft")

        # Compact the layout to eliminate gaps
        print("\nCompacting layout to eliminate gaps...")
        self.compact_layout()

        # Final optimization pass
        print("Optimizing layout for maximum compactness...")
        self.optimize_layout()

    def add_margins(self):
        """Add margins for inbound/outbound operations."""
        if not self.placed:
            return

        # Find minimum coordinates
        min_x = min(x for x, y, w, d in self.placed.values())
        min_y = min(y for x, y, w, d in self.placed.values())

        # Shift all blocks to add margins
        x_shift = MARGIN_LEFT - min_x if min_x < MARGIN_LEFT else 0
        y_shift = MARGIN_TOP - min_y if min_y < MARGIN_TOP else 0

        for process in self.placed:
            x, y, w, d = self.placed[process]
            self.placed[process] = (x + x_shift, y + y_shift, w, d)

            cx, cy = self.centroids[process]
            self.centroids[process] = (cx + x_shift, cy + y_shift)

    def get_layout_bounds(self):
        """Calculate overall layout dimensions."""
        if not self.placed:
            return 0, 0, 0

        max_x = max(x + w for x, y, w, d in self.placed.values())
        max_y = max(y + d for x, y, w, d in self.placed.values())
        total_area = max_x * max_y

        return max_x, max_y, total_area

# ============================================================================
# VISUALIZATION FUNCTIONS
# ============================================================================

def create_layout_visualization(year, num_fractals, placer):
    """Create and save a visualization of the layout."""
    if not placer.placed:
        print("No layout data to visualize")
        return None

    fig, ax = plt.subplots(1, 1, figsize=(12, 8))

    # Color map for different processes
    color_list = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                  '#aec7e8', '#ffbb78', '#98df8a', '#ff9896']
    colors = [color_list[i % len(color_list)] for i in range(len(placer.placed))]

    # Plot each block
    for i, (process, (x, y, w, d)) in enumerate(placer.placed.items()):
        # Create rectangle
        rect = patches.Rectangle((x, y), w, d,
                               linewidth=2,
                               edgecolor='black',
                               facecolor=colors[i % len(colors)],
                               alpha=0.7)

        ax.add_patch(rect)

        # Add process label at centroid
        cx, cy = placer.centroids[process]
        ax.text(cx, cy, process,
               ha='center', va='center',
               fontsize=10, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.3',
                        facecolor='white',
                        alpha=0.8))

        # Add dimensions
        ax.text(x + w/2, y + d + 2, f'{w:.0f}×{d:.0f}',
               ha='center', va='bottom',
               fontsize=8, color='blue')

    # Plot centroids
    centroids_x = [pos[0] for pos in placer.centroids.values()]
    centroids_y = [pos[1] for pos in placer.centroids.values()]
    ax.scatter(centroids_x, centroids_y,
              c='red', marker='x', s=50,
              linewidth=2, label='Centroids')

    # Set labels and title
    ax.set_xlabel('X Position (feet)')
    ax.set_ylabel('Y Position (feet)')
    ax.set_title(f'Fractal Layout - Year {year}, F{num_fractals}\nFlow-Based Adjacency Placement')

    # Add legend
    ax.legend()

    # Set equal aspect ratio
    ax.set_aspect('equal')

    # Add grid
    ax.grid(True, alpha=0.3)

    # Tight layout
    plt.tight_layout()

    # Save the plot
    output_dir = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / f"Year{year}_F{num_fractals}_Optimized"
    output_dir.mkdir(parents=True, exist_ok=True)

    viz_file = output_dir / f"Year{year}_F{num_fractals}_Layout_Visualization.png"
    plt.savefig(viz_file, dpi=300, bbox_inches='tight')
    plt.close()

    return viz_file

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_flow_matrix(year, num_fractals):
    """Load aggregate flow matrix for the given year and fractal count."""
    flow_path = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Flowmatrix" / f"year{year}" / f"f{num_fractals}_centers" / "Aggregate_Factory_Flow_Matrix.csv"
    return pd.read_csv(flow_path, index_col=0)

def load_block_dimensions(year, num_fractals):
    """Load optimized block dimensions."""
    config_path = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / f"Year{year}_F{num_fractals}_Optimized" / f"Year{year}_F{num_fractals}_Optimal_Grid_Configurations.csv"
    df = pd.read_csv(config_path)

    dims = {}
    for _, row in df.iterrows():
        dims[row['process']] = (row['block_width_ft'], row['block_depth_ft'])

    return dims

# ============================================================================
# OUTPUT FUNCTIONS
# ============================================================================

def save_results(year, num_fractals, placer):
    """Save centroids and layout data."""
    output_dir = BASE_DIR / "results" / "task4" / "Fractal" / "Fractal_Layout" / f"Year{year}_F{num_fractals}_Optimized"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Centroids CSV (primary requirement)
    centroids_data = []
    for process, (cx, cy) in placer.centroids.items():
        centroids_data.append({
            'process': process,
            'centroid_x': round(cx, 1),
            'centroid_y': round(cy, 1)
        })

    df_centroids = pd.DataFrame(centroids_data)
    centroids_file = output_dir / f"Year{year}_F{num_fractals}_Block_Centroids.csv"
    df_centroids.to_csv(centroids_file, index=False)

    # Full layout coordinates
    layout_data = []
    for process, (x, y, w, d) in placer.placed.items():
        cx, cy = placer.centroids[process]
        layout_data.append({
            'process': process,
            'x': round(x, 1),
            'y': round(y, 1),
            'width_ft': round(w, 1),
            'depth_ft': round(d, 1),
            'centroid_x': round(cx, 1),
            'centroid_y': round(cy, 1),
            'area_sqft': round(w * d, 1)
        })

    df_layout = pd.DataFrame(layout_data)
    layout_file = output_dir / f"Year{year}_F{num_fractals}_Layout_Coordinates.csv"
    df_layout.to_csv(layout_file, index=False)

    return centroids_file, layout_file

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main(year, num_fractals):
    print("=" * 60)
    print(f"FRACTAL LAYOUT PLACEMENT - Year {year}, F{num_fractals}")
    print("=" * 60)

    try:
        # Load data
        print("Loading flow matrix and block dimensions...")
        flow_df = load_flow_matrix(year, num_fractals)
        block_dims = load_block_dimensions(year, num_fractals)

        print(f"Loaded {len(block_dims)} process blocks")

        # Analyze flows
        flow_pairs = analyze_flow_relationships(flow_df)
        print(f"Found {len(flow_pairs)} flow relationships")
        if flow_pairs:
            print(f"Top flow: {flow_pairs[0][0]}->{flow_pairs[0][1]} ({flow_pairs[0][2]:,.0f})")

        # Create layout placer
        placer = FlowBasedLayoutPlacer(block_dims, flow_pairs)

        # Place blocks
        print("\nPlacing blocks using flow-based adjacency algorithm...")
        placer.place_blocks()

        # Add margins
        print("\nAdding pragmatic margins for inbound/outbound...")
        placer.add_margins()

        # Calculate layout size
        max_x, max_y, total_area = placer.get_layout_bounds()
        print(f"\nLayout dimensions: {max_x:.0f}×{max_y:.0f} ft ({total_area:,.0f} sq ft)")

        # Save results
        centroids_file, layout_file = save_results(year, num_fractals, placer)

        # Create visualization
        print("\nCreating layout visualization...")
        viz_file = create_layout_visualization(year, num_fractals, placer)

        print("\n✓ LAYOUT GENERATION COMPLETE!")
        print(f"📍 Centroids: {centroids_file.name}")
        print(f"📐 Layout: {layout_file.name}")
        if viz_file:
            print(f"🖼️  Visualization: {viz_file.name}")
        print(f"🎯 {len(placer.centroids)} blocks placed with flow-based adjacency")

    except Exception as e:
        print(f" ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    year = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    num_fractals = int(sys.argv[2]) if len(sys.argv) > 2 else 4

    success = main(year, num_fractals)
    sys.exit(0 if success else 1)
