"""
Fractal Layout Generator for Year 5, f=4 Centers
=================================================

This module generates optimal parent block layouts for fractal factory design.

Key Features:
1. Parent Block Design: Creates optimal layouts for each process (A-M)
2. Flow-Based Placement: Uses flow matrix to position blocks optimally
3. Visualization: Generates scaled, annotated layout diagrams
4. CSV Export: Outputs parent block specifications

Author: Adarsh
Date: November 11, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle, FancyBboxPatch
import math
import os
from typing import Dict, List, Tuple, Optional
import seaborn as sns


class FractalLayoutGenerator:
    """
    Generates fractal factory layouts with optimal parent block design
    and flow-based spatial arrangement.
    """
    
    def __init__(self, equipment_file: str, flow_matrix_file: str, output_dir: str):
        """
        Initialize the layout generator.
        
        Args:
            equipment_file: Path to equipment requirements CSV
            flow_matrix_file: Path to flow matrix CSV
            output_dir: Directory for output files
        """
        self.equipment_df = pd.read_csv(equipment_file)
        self.flow_matrix_df = pd.read_csv(flow_matrix_file, index_col=0)
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Area specifications with sharing rules
        self.area_specs = {
            'A': {'Width_ft': 14, 'Depth_ft': 14, 'Shareable_Sides': ['front', 'left', 'right'], 
                  'Shared_Allowance_ft': 2, 'Group': 'ABCD', 'Color': '#8B4789'},
            'B': {'Width_ft': 14, 'Depth_ft': 14, 'Shareable_Sides': ['front', 'left', 'right'], 
                  'Shared_Allowance_ft': 2, 'Group': 'ABCD', 'Color': '#9B59B6'},
            'C': {'Width_ft': 14, 'Depth_ft': 14, 'Shareable_Sides': ['front', 'left', 'right'], 
                  'Shared_Allowance_ft': 2, 'Group': 'ABCD', 'Color': '#E91E63'},
            'D': {'Width_ft': 14, 'Depth_ft': 14, 'Shareable_Sides': ['front', 'left', 'right'], 
                  'Shared_Allowance_ft': 2, 'Group': 'ABCD', 'Color': '#D3D3D3'},
            'E': {'Width_ft': 22, 'Depth_ft': 15, 'Shareable_Sides': [], 
                  'Shared_Allowance_ft': 0, 'Group': 'EFG', 'Color': '#FFB6C1'},
            'F': {'Width_ft': 22, 'Depth_ft': 15, 'Shareable_Sides': [], 
                  'Shared_Allowance_ft': 0, 'Group': 'EFG', 'Color': '#FF0000'},
            'G': {'Width_ft': 22, 'Depth_ft': 15, 'Shareable_Sides': [], 
                  'Shared_Allowance_ft': 0, 'Group': 'EFG', 'Color': '#228B22'},
            'H': {'Width_ft': 14, 'Depth_ft': 36, 'Shareable_Sides': [], 
                  'Shared_Allowance_ft': 0, 'Group': 'HIJ', 'Color': '#D2B48C'},
            'I': {'Width_ft': 14, 'Depth_ft': 36, 'Shareable_Sides': [], 
                  'Shared_Allowance_ft': 0, 'Group': 'HIJ', 'Color': '#000000'},
            'J': {'Width_ft': 14, 'Depth_ft': 36, 'Shareable_Sides': [], 
                  'Shared_Allowance_ft': 0, 'Group': 'HIJ', 'Color': '#0000FF'},
            'K': {'Width_ft': 14, 'Depth_ft': 7, 'Shareable_Sides': ['left', 'right'], 
                  'Shared_Allowance_ft': 1, 'Group': 'KLM', 'Color': '#8B4513'},
            'L': {'Width_ft': 14, 'Depth_ft': 7, 'Shareable_Sides': ['left', 'right'], 
                  'Shared_Allowance_ft': 1, 'Group': 'KLM', 'Color': '#90EE90'},
            'M': {'Width_ft': 14, 'Depth_ft': 7, 'Shareable_Sides': ['left', 'right'], 
                  'Shared_Allowance_ft': 1, 'Group': 'KLM', 'Color': '#87CEEB'},
        }
        
        self.parent_blocks = {}
        self.placement = {}
        
    def calculate_parent_block_layout(self, process: str, num_equipment: int) -> Dict:
        """
        Calculate optimal parent block layout for given number of equipment.
        
        Critical Analysis Steps:
        1. Find all possible rectangular grids (including N+1 for better geometry)
        2. Calculate effective dimensions considering shareable space
        3. Score based on aspect ratio (prefer square) and space efficiency
        4. Consider process flow characteristics (high flow = more compact)
        
        Args:
            process: Process letter (A-M)
            num_equipment: Number of equipment units needed
            
        Returns:
            Dictionary with layout specifications
        """
        spec = self.area_specs[process]
        width = spec['Width_ft']
        depth = spec['Depth_ft']
        shareable = spec['Shareable_Sides']
        shared_allowance = spec['Shared_Allowance_ft']
        
        # Find all possible grid layouts
        layouts = self._find_optimal_grid(num_equipment)
        
        # Select best layout based on multiple criteria
        best_layout = self._select_best_layout(
            layouts, width, depth, shareable, shared_allowance, num_equipment
        )
        
        # Add metadata
        best_layout['process'] = process
        best_layout['num_equipment'] = num_equipment
        best_layout['machine_width'] = width
        best_layout['machine_depth'] = depth
        best_layout['group'] = spec['Group']
        best_layout['color'] = spec['Color']
        
        return best_layout
    
    def _find_optimal_grid(self, n: int) -> List[Tuple]:
        """
        Find all possible rectangular grids for n equipment.
        
        Strategy:
        - Perfect squares preferred (e.g., 16 = 4×4)
        - Near-squares considered (e.g., 15 = 3×5 or 4×4)
        - Allow N+1 spaces for better geometry (e.g., 17 -> 3x6 = 18)
        - Limit waste to max 3 spaces
        
        Returns:
            List of (rows, cols, total_spaces) tuples
        """
        layouts = []
        
        # Check perfect square
        sqrt_n = int(math.sqrt(n))
        if sqrt_n * sqrt_n == n:
            layouts.append((sqrt_n, sqrt_n, n))
        
        # Check all factor pairs for exact fit
        for rows in range(1, n + 1):
            if n % rows == 0:
                cols = n // rows
                layouts.append((rows, cols, n))
        
        # Allow up to 3 extra spaces for better geometry
        for extra in range(1, 4):
            total = n + extra
            for rows in range(1, total + 1):
                if total % rows == 0:
                    cols = total // rows
                    layouts.append((rows, cols, total))
        
        # Remove duplicates
        layouts = list(set(layouts))
        
        return layouts
    
    def _select_best_layout(self, layouts: List[Tuple], width: float, depth: float, 
                           shareable: List[str], shared_allowance: float, 
                           num_equipment: int) -> Dict:
        """
        Select best layout using multi-criteria scoring.
        
        Scoring Criteria:
        1. Aspect Ratio (40%): Prefer square-ish layouts (ratio close to 1.0)
        2. Space Efficiency (30%): Minimize wasted spaces
        3. Perimeter (20%): Minimize perimeter for material handling
        4. Utilization (10%): Maximize equipment utilization
        
        CRITICAL FIX: KLM processes share on LEFT/RIGHT which is along the DEPTH (length),
        not the width. Width=14ft, Depth=7ft. Sharing happens along the 7ft dimension.
        
        Args:
            layouts: List of possible (rows, cols, total_spaces) configurations
            width, depth: Individual machine dimensions
            shareable: List of shareable sides
            shared_allowance: Shared space in feet
            num_equipment: Actual equipment needed
            
        Returns:
            Best layout configuration dictionary
        """
        best_score = float('inf')
        best_layout = None
        
        for layout in layouts:
            rows, cols, total_spaces = layout
            
            # Calculate effective dimensions with sharing
            # CRITICAL: For KLM (width=14, depth=7), left/right sharing is along DEPTH dimension
            # When machines are placed in rows, left/right sharing reduces DEPTH
            # When machines are placed in cols, left/right sharing reduces WIDTH
            
            # Determine which dimension gets sharing reduction
            if 'left' in shareable and 'right' in shareable:
                # Left/right sharing occurs along the depth dimension when arranged in rows
                effective_depth = depth * cols - shared_allowance * (cols - 1)
                effective_width = width * rows
            elif 'front' in shareable and len(shareable) >= 3:  # front sharing for ABCD
                effective_width = width * cols - shared_allowance * (cols - 1)
                effective_depth = depth * rows - shared_allowance * (rows - 1)
            else:
                effective_width = width * cols
                effective_depth = depth * rows
            
            # Calculate metrics
            aspect_ratio = max(effective_width, effective_depth) / min(effective_width, effective_depth)
            wasted_spaces = total_spaces - num_equipment
            perimeter = 2 * (effective_width + effective_depth)
            utilization = num_equipment / total_spaces
            
            # Multi-criteria score (lower is better)
            aspect_score = abs(aspect_ratio - 1.0) * 40  # Penalty for non-square
            waste_score = wasted_spaces * 30  # Penalty for wasted space
            perimeter_score = perimeter / 100 * 20  # Normalized perimeter penalty
            util_score = (1 - utilization) * 10  # Penalty for low utilization
            
            total_score = aspect_score + waste_score + perimeter_score + util_score
            
            if total_score < best_score:
                best_score = total_score
                best_layout = {
                    'rows': rows,
                    'cols': cols,
                    'total_spaces': total_spaces,
                    'width_ft': round(effective_width, 2),
                    'depth_ft': round(effective_depth, 2),
                    'area_sqft': round(effective_width * effective_depth, 2),
                    'aspect_ratio': round(aspect_ratio, 3),
                    'wasted_spaces': wasted_spaces,
                    'utilization': round(utilization, 4),
                    'perimeter_ft': round(perimeter, 2),
                    'score': round(total_score, 2)
                }
        
        return best_layout
    
    def generate_all_parent_blocks(self) -> Dict:
        """
        Generate parent blocks for all processes.
        
        Returns:
            Dictionary mapping process to layout specification
        """
        equipment_data = self.equipment_df[self.equipment_df['Process'] != 'TOTAL']
        
        print("\n" + "="*100)
        print("GENERATING PARENT BLOCK LAYOUTS - Year 5, f=4 Centers")
        print("="*100)
        
        for _, row in equipment_data.iterrows():
            process = row['Process']
            equipment_per_center = int(row['Equipment_per_Center'])
            
            layout = self.calculate_parent_block_layout(process, equipment_per_center)
            self.parent_blocks[process] = layout
            
            print(f"\nProcess {process}: {equipment_per_center} equipment -> "
                  f"{layout['rows']}×{layout['cols']} grid "
                  f"({layout['width_ft']}' × {layout['depth_ft']}') "
                  f"[Waste: {layout['wasted_spaces']}, AR: {layout['aspect_ratio']:.2f}]")
        
        return self.parent_blocks
    
    def export_parent_blocks_csv(self) -> str:
        """
        Export parent block specifications to CSV.
        
        Returns:
            Path to exported CSV file
        """
        output_file = os.path.join(self.output_dir, "Parent_Block_Specifications.csv")
        
        # Convert to DataFrame
        data = []
        for process in sorted(self.parent_blocks.keys()):
            layout = self.parent_blocks[process]
            data.append({
                'Process': process,
                'Group': layout['group'],
                'Equipment_Count': layout['num_equipment'],
                'Layout_Grid': f"{layout['rows']}×{layout['cols']}",
                'Total_Spaces': layout['total_spaces'],
                'Wasted_Spaces': layout['wasted_spaces'],
                'Machine_Width_ft': layout['machine_width'],
                'Machine_Depth_ft': layout['machine_depth'],
                'Block_Width_ft': layout['width_ft'],
                'Block_Depth_ft': layout['depth_ft'],
                'Block_Area_sqft': layout['area_sqft'],
                'Aspect_Ratio': layout['aspect_ratio'],
                'Utilization': layout['utilization'],
                'Perimeter_ft': layout['perimeter_ft'],
                'Optimization_Score': layout['score']
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        
        print(f"\n✓ Parent block specifications exported to: {output_file}")
        return output_file
    
    def visualize_individual_parent_blocks(self):
        """
        Create detailed visualizations of each parent block with scale.
        Shows individual machine positions within each block.
        
        IMPROVED: Creates 4 separate group files (ABCD, EFG, HIJ, KLM) instead of one combined file
        to improve readability and prevent child blocks from appearing cut off.
        """
        print("\n" + "="*100)
        print("GENERATING INDIVIDUAL PARENT BLOCK VISUALIZATIONS")
        print("="*100)
        
        # Define process groups
        process_groups = {
            'ABCD': ['A', 'B', 'C', 'D'],
            'EFG': ['E', 'F', 'G'],
            'HIJ': ['H', 'I', 'J'],
            'KLM': ['K', 'L', 'M']
        }
        
        # Create one combined view per group
        for group_name, processes in process_groups.items():
            # Filter to only processes that exist
            processes = [p for p in processes if p in self.parent_blocks]
            if not processes:
                continue
            
            # Determine grid layout for this group
            n_processes = len(processes)
            if n_processes <= 2:
                n_cols = 2
            else:
                n_cols = 2
            n_rows = (n_processes + n_cols - 1) // n_cols
            
            # Create figure - larger for better readability
            fig = plt.figure(figsize=(20, 10 * n_rows), facecolor='white')
            
            for idx, process in enumerate(processes, 1):
                layout = self.parent_blocks[process]
                
                ax = plt.subplot(n_rows, n_cols, idx)
                self._draw_single_parent_block(ax, process, layout)
            
            # Add overall title for this group
            fig.suptitle(f'Parent Block Layouts - Group {group_name}\n'
                        f'Year 5, f=4 Centers',
                        fontsize=22, fontweight='bold', y=0.995)
            
            plt.tight_layout(rect=[0, 0, 1, 0.985])
            output_file = os.path.join(self.output_dir, f"Parent_Blocks_Group_{group_name}.png")
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"✓ Group {group_name} parent blocks saved to: Parent_Blocks_Group_{group_name}.png")
        
        # ALSO CREATE INDIVIDUAL PNG FOR EACH PROCESS
        print("\n  Creating individual PNG files for each process...")
        all_processes = sorted(self.parent_blocks.keys())
        for process in all_processes:
            layout = self.parent_blocks[process]
            
            fig, ax = plt.subplots(figsize=(12, 10))
            self._draw_single_parent_block(ax, process, layout, standalone=True)
            
            plt.tight_layout()
            individual_file = os.path.join(self.output_dir, f"Parent_Block_{process}.png")
            plt.savefig(individual_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"    ✓ Process {process} saved to: Parent_Block_{process}.png")
            layout = self.parent_blocks[process]
            
            fig, ax = plt.subplots(figsize=(10, 8))
            self._draw_single_parent_block(ax, process, layout, standalone=True)
            
            plt.tight_layout()
            individual_file = os.path.join(self.output_dir, f"Parent_Block_{process}.png")
            plt.savefig(individual_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            print(f"    ✓ Process {process} saved to: Parent_Block_{process}.png")
    
    def _draw_single_parent_block(self, ax, process: str, layout: Dict, standalone: bool = False):
        """
        Draw a single parent block with all its machines.
        
        Args:
            ax: Matplotlib axis
            process: Process letter
            layout: Layout dictionary
            standalone: If True, enhance for standalone image
        """
        # Draw individual machines in grid
        rows = layout['rows']
        cols = layout['cols']
        machine_w = layout['machine_width']
        machine_d = layout['machine_depth']
        
        # Calculate spacing (consider sharing) - MUST MATCH PARENT BLOCK CALCULATION
        # CRITICAL UNDERSTANDING:
        # - Parent calc: effective_width = width * rows, effective_depth = depth * cols
        # - rows controls WIDTH (X-axis), cols controls DEPTH (Y-axis)
        # - When iterating: r varies rows (affects X), c varies cols (affects Y)
        # - Machine dimensions: machine_w (width) in X, machine_d (depth) in Y
        
        spec = self.area_specs[process]
        
        if 'left' in spec['Shareable_Sides'] and 'right' in spec['Shareable_Sides']:
            # KLM case: left/right sharing is along DEPTH dimension
            # effective_depth = depth * cols - shared_allowance * (cols - 1)
            # This means sharing happens between columns (in Y direction)
            # r iterates rows → affects X position, spacing = full width
            # c iterates cols → affects Y position, spacing = depth - sharing
            width_spacing = machine_w  # Full width, no sharing (14ft)
            depth_spacing = machine_d - spec['Shared_Allowance_ft']  # Depth with sharing (7-1=6ft)
        elif 'front' in spec['Shareable_Sides']:
            # ABCD case: sharing on front, left, right reduces both dimensions
            width_spacing = machine_w - spec['Shared_Allowance_ft']
            depth_spacing = machine_d - spec['Shared_Allowance_ft']
        else:
            width_spacing = machine_w
            depth_spacing = machine_d
        
        # Draw machines
        machine_count = 0
        for r in range(rows):
            for c in range(cols):
                if machine_count < layout['num_equipment']:
                    # r controls X (width), c controls Y (depth)
                    x = r * width_spacing
                    y = c * depth_spacing
                    
                    rect = Rectangle((x, y), machine_w, machine_d,
                                   linewidth=2.5, edgecolor='black',
                                   facecolor=layout['color'], alpha=0.85)
                    ax.add_patch(rect)
                    
                    # Add machine number
                    ax.text(x + machine_w/2, y + machine_d/2, 
                           f"{machine_count+1}",
                           ha='center', va='center', fontsize=11 if standalone else 10,
                           fontweight='bold', color='white',
                           bbox=dict(boxstyle='circle', facecolor='black', alpha=0.8, pad=0.35))
                    
                    machine_count += 1
                else:
                    # Wasted space - show with different style
                    # r controls X (width), c controls Y (depth)
                    x = r * width_spacing
                    y = c * depth_spacing
                    rect = Rectangle((x, y), machine_w, machine_d,
                                   linewidth=1.5, edgecolor='gray',
                                   facecolor='lightgray', alpha=0.4,
                                   linestyle='--')
                    ax.add_patch(rect)
                    ax.text(x + machine_w/2, y + machine_d/2, "×",
                           ha='center', va='center', fontsize=14 if standalone else 12,
                           color='gray', fontweight='bold')
        
        # Set proper axis limits with adequate padding - START FROM ORIGIN
        padding = 30 if standalone else 20
        ax.set_xlim(-5, layout['width_ft'] + padding)
        ax.set_ylim(-5, layout['depth_ft'] + padding)
        ax.set_aspect('equal')
        
        # Add grid and labels
        ax.grid(True, alpha=0.25, linestyle=':', linewidth=0.8, color='gray')
        ax.set_xlabel('Width (feet)', fontsize=13 if standalone else 11, fontweight='bold')
        ax.set_ylabel('Depth (feet)', fontsize=13 if standalone else 11, fontweight='bold')
        ax.tick_params(labelsize=10 if standalone else 9)
        
        # Title with key information
        if standalone:
            title = (f"Process {process} - Parent Block Layout\n"
                    f"Group: {layout['group']} | Equipment: {layout['num_equipment']} units\n"
                    f"Grid: {layout['rows']}×{layout['cols']} = {layout['total_spaces']} spaces "
                    f"(Utilization: {layout['utilization']:.1%})\n"
                    f"Dimensions: {layout['width_ft']}'W × {layout['depth_ft']}'D = "
                    f"{layout['area_sqft']:,} sq ft | Aspect Ratio: {layout['aspect_ratio']:.2f}")
            fontsize = 12
        else:
            title = (f"Process {process} ({layout['group']})\n"
                    f"{layout['num_equipment']} equip | {layout['rows']}×{layout['cols']} grid\n"
                    f"{layout['width_ft']}'W × {layout['depth_ft']}'D = "
                    f"{layout['area_sqft']:,} sq ft")
            fontsize = 10
        
        ax.set_title(title, fontsize=fontsize, fontweight='bold', pad=12)
        
        # Professional dimension annotations - POSITIONED WELL OUTSIDE BLOCKS
        # Width annotation (top of block)
        width_y = layout['depth_ft'] + 18
        ax.annotate('', xy=(0, width_y), xytext=(layout['width_ft'], width_y),
                   arrowprops=dict(arrowstyle='<->', color='#2E8B57', lw=2.5,
                                 shrinkA=0, shrinkB=0))
        ax.text(layout['width_ft']/2, width_y + 5, f"{layout['width_ft']:.0f} ft",
               ha='center', va='bottom', fontsize=12 if standalone else 10,
               color='#2E8B57', fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                        edgecolor='#2E8B57', linewidth=2))

        # Depth annotation (right of block)
        depth_x = layout['width_ft'] + 18
        ax.annotate('', xy=(depth_x, 0), xytext=(depth_x, layout['depth_ft']),
                   arrowprops=dict(arrowstyle='<->', color='#2E8B57', lw=2.5,
                                 shrinkA=0, shrinkB=0))
        ax.text(depth_x + 5, layout['depth_ft']/2, f"{layout['depth_ft']:.0f} ft",
               ha='left', va='center', fontsize=12 if standalone else 10,
               color='#2E8B57', fontweight='bold', rotation=90,
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                        edgecolor='#2E8B57', linewidth=2))
        
        # Add sharing info if applicable
        if spec['Shareable_Sides']:
            sharing_text = f"Shareable: {', '.join(spec['Shareable_Sides'])} ({spec['Shared_Allowance_ft']}')"
            ax.text(0.02, 0.98, sharing_text,
                   transform=ax.transAxes,
                   fontsize=10 if standalone else 8,
                   verticalalignment='top',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='yellow', alpha=0.7,
                            edgecolor='orange', linewidth=1.5))
    
    def calculate_flow_scores(self) -> Dict:
        """
        Calculate flow intensity scores for each process.
        Used to prioritize central placement for high-flow processes.
        
        Returns:
            Dictionary mapping process to total flow score
        """
        flow_scores = {}
        
        for process in self.parent_blocks.keys():
            # Total outgoing + incoming flow
            outgoing = self.flow_matrix_df.loc[process].sum()
            incoming = self.flow_matrix_df[process].sum()
            total_flow = outgoing + incoming
            
            flow_scores[process] = total_flow
        
        return flow_scores
    
    def optimize_placement(self) -> Dict:
        """
        Optimize spatial placement of parent blocks using flow-based heuristic.
        
        IMPROVED ALGORITHM for more compact, square layouts:
        1. Start with highest-flow process near center
        2. Place connected high-flow processes nearby
        3. Use compactness penalty to encourage square layouts
        4. Minimize total flow×distance while maintaining compactness
        
        Returns:
            Dictionary mapping process to (x, y, rotation) placement
        """
        print("\n" + "="*100)
        print("OPTIMIZING SPATIAL PLACEMENT BASED ON FLOW MATRIX")
        print("="*100)
        
        flow_scores = self.calculate_flow_scores()
        
        # Sort processes by flow (highest first)
        sorted_processes = sorted(flow_scores.items(), key=lambda x: x[1], reverse=True)
        
        print("\nFlow Intensity Ranking:")
        for i, (proc, flow) in enumerate(sorted_processes, 1):
            print(f"  {i}. Process {proc}: {flow:,.0f} units")
        
        # Initialize placement
        placement = {}
        placed = set()
        
        # Start with highest flow process at origin
        first_process = sorted_processes[0][0]
        first_layout = self.parent_blocks[first_process]
        placement[first_process] = {
            'x': 0,
            'y': 0,
            'rotation': 0,
            'width': first_layout['width_ft'],
            'depth': first_layout['depth_ft']
        }
        placed.add(first_process)
        
        print(f"\nStarting placement with Process {first_process} (highest flow) at origin")
        
        # Placement strategy: greedy based on flow connectivity with compactness preference
        while len(placed) < len(self.parent_blocks):
            best_score = -float('inf')
            best_placement = None
            best_process = None
            
            # Try placing each unplaced process
            for process in self.parent_blocks.keys():
                if process in placed:
                    continue
                
                # Find best position adjacent to already-placed processes
                for placed_proc in placed:
                    # Try multiple positions around placed process (including diagonal)
                    positions = self._get_adjacent_positions_compact(placed_proc, placement, process)
                    
                    for pos in positions:
                        # Calculate score: flow connection / distance - compactness penalty
                        score = self._calculate_placement_score_with_compactness(
                            process, pos, placement, placed
                        )
                        
                        if score > best_score:
                            best_score = score
                            best_placement = pos
                            best_process = process
            
            if best_process:
                placement[best_process] = best_placement
                placed.add(best_process)
                print(f"  Placed Process {best_process} at ({best_placement['x']:.1f}, "
                      f"{best_placement['y']:.1f}) [Score: {best_score:.2f}]")
        
        self.placement = placement
        return placement
    
    def _get_adjacent_positions_compact(self, placed_process: str, placement: Dict, 
                               new_process: str) -> List[Dict]:
        """
        Get possible adjacent positions for a new process around a placed one.
        IMPROVED: Includes diagonal positions for more compact layouts.
        
        Returns list of position dictionaries with x, y, rotation, width, depth
        """
        placed_info = placement[placed_process]
        new_layout = self.parent_blocks[new_process]
        
        positions = []
        gap = 10  # 10 feet gap between blocks for material handling
        
        # Right of placed block
        positions.append({
            'x': placed_info['x'] + placed_info['width'] + gap,
            'y': placed_info['y'],
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Left of placed block
        positions.append({
            'x': placed_info['x'] - new_layout['width_ft'] - gap,
            'y': placed_info['y'],
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Above placed block
        positions.append({
            'x': placed_info['x'],
            'y': placed_info['y'] + placed_info['depth'] + gap,
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Below placed block
        positions.append({
            'x': placed_info['x'],
            'y': placed_info['y'] - new_layout['depth_ft'] - gap,
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # DIAGONAL POSITIONS for more compact layout
        # Top-right
        positions.append({
            'x': placed_info['x'] + placed_info['width'] + gap,
            'y': placed_info['y'] + placed_info['depth'] + gap,
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Top-left
        positions.append({
            'x': placed_info['x'] - new_layout['width_ft'] - gap,
            'y': placed_info['y'] + placed_info['depth'] + gap,
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Bottom-right
        positions.append({
            'x': placed_info['x'] + placed_info['width'] + gap,
            'y': placed_info['y'] - new_layout['depth_ft'] - gap,
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Bottom-left
        positions.append({
            'x': placed_info['x'] - new_layout['width_ft'] - gap,
            'y': placed_info['y'] - new_layout['depth_ft'] - gap,
            'rotation': 0,
            'width': new_layout['width_ft'],
            'depth': new_layout['depth_ft']
        })
        
        # Filter out overlapping positions
        valid_positions = []
        for pos in positions:
            if not self._check_overlap(pos, placement):
                valid_positions.append(pos)
        
        return valid_positions
        
        # Filter out overlapping positions
        valid_positions = []
        for pos in positions:
            if not self._check_overlap(pos, placement):
                valid_positions.append(pos)
        
        return valid_positions
    
    def _check_overlap(self, new_pos: Dict, placement: Dict) -> bool:
        """Check if new position overlaps with any existing placement."""
        gap = 10  # Minimum gap
        
        for proc, pos in placement.items():
            # Check rectangle overlap with gap
            if not (new_pos['x'] + new_pos['width'] + gap <= pos['x'] or
                   new_pos['x'] >= pos['x'] + pos['width'] + gap or
                   new_pos['y'] + new_pos['depth'] + gap <= pos['y'] or
                   new_pos['y'] >= pos['y'] + pos['depth'] + gap):
                return True
        
        return False
    
    def _calculate_placement_score_with_compactness(self, process: str, position: Dict, 
                                  placement: Dict, placed: set) -> float:
        """
        Calculate placement score based on flow intensity, distance, AND compactness.
        
        Score = Σ(flow_ij / distance_ij) - compactness_penalty
        
        Compactness penalty encourages square layouts by penalizing extreme aspect ratios.
        """
        score = 0.0
        
        # Calculate centroid of new position
        new_x = position['x'] + position['width'] / 2
        new_y = position['y'] + position['depth'] / 2
        
        # Flow-based score
        for placed_proc in placed:
            # Get flow between processes (bidirectional)
            try:
                flow_to = float(self.flow_matrix_df.loc[process, placed_proc])
                flow_from = float(self.flow_matrix_df.loc[placed_proc, process])
                total_flow = flow_to + flow_from
            except (ValueError, TypeError):
                total_flow = 0
            
            if total_flow > 0:
                # Calculate distance between centroids
                placed_x = placement[placed_proc]['x'] + placement[placed_proc]['width'] / 2
                placed_y = placement[placed_proc]['y'] + placement[placed_proc]['depth'] / 2
                
                distance = math.sqrt((new_x - placed_x)**2 + (new_y - placed_y)**2)
                
                # Avoid division by zero
                if distance < 1:
                    distance = 1
                
                score += total_flow / distance
        
        # COMPACTNESS PENALTY: Calculate bounding box aspect ratio
        # Get current bounding box with this new position
        all_x = [pos['x'] for pos in placement.values()] + [position['x']]
        all_y = [pos['y'] for pos in placement.values()] + [position['y']]
        all_x_max = [pos['x'] + pos['width'] for pos in placement.values()] + [position['x'] + position['width']]
        all_y_max = [pos['y'] + pos['depth'] for pos in placement.values()] + [position['y'] + position['depth']]
        
        layout_width = max(all_x_max) - min(all_x)
        layout_height = max(all_y_max) - min(all_y)
        
        # Calculate aspect ratio (deviation from square)
        if layout_height > 0:
            aspect_ratio = layout_width / layout_height
            if aspect_ratio < 1:
                aspect_ratio = 1 / aspect_ratio
            
            # Penalty increases quadratically with deviation from square (AR=1)
            # Ideal AR is between 0.8 and 1.25 (square-ish)
            compactness_penalty = (aspect_ratio - 1.0) ** 2 * 50
            score -= compactness_penalty
        
        return score
    
    def visualize_final_layout(self):
        """
        Create CLEAN and INFORMATIVE final layout visualization with:
        - Scaled blocks with clear dimensions
        - Color coding by process group
        - Professional appearance
        - Comprehensive legend and information
        - STARTS FROM ORIGIN (0, 0)
        """
        print("\n" + "="*100)
        print("GENERATING CLEAN FINAL FRACTAL LAYOUT VISUALIZATION")
        print("="*100)
        
        fig, ax = plt.subplots(figsize=(32, 26), facecolor='white')
        ax.set_facecolor('#F8F9FA')  # Very light gray background

        # Calculate layout bounds to ensure all blocks are visible
        min_x = min(p['x'] for p in self.placement.values())
        max_x = max(p['x'] + p['width'] for p in self.placement.values())
        min_y = min(p['y'] for p in self.placement.values())
        max_y = max(p['y'] + p['depth'] for p in self.placement.values())

        # START FROM ORIGIN: Shift all coordinates so layout starts at (0,0)
        x_offset = -min_x
        y_offset = -min_y

        # Calculate final dimensions after offset
        final_max_x = max_x + x_offset
        final_max_y = max_y + y_offset

        # Add generous padding
        padding = 80
        ax.set_xlim(-10, final_max_x + padding)
        ax.set_ylim(-10, final_max_y + padding)

        # Add generous padding
        padding = 80
        ax.set_xlim(-10, final_max_x + padding)
        ax.set_ylim(-10, final_max_y + padding)
        
        # Draw each parent block with clean styling using ORIGIN-BASED coordinates
        for process, original_pos in self.placement.items():
            layout = self.parent_blocks[process]
            
            # Apply offset for origin-based display
            pos_x = original_pos['x'] + x_offset
            pos_y = original_pos['y'] + y_offset
            
            # Create clean rectangle for parent block
            rect = Rectangle(
                (pos_x, pos_y), original_pos['width'], original_pos['depth'],
                linewidth=3, 
                edgecolor='black',
                facecolor=layout['color'], 
                alpha=0.80,
                zorder=2
            )
            ax.add_patch(rect)
            
            # Add process label - CLEAN and READABLE
            center_x = pos_x + original_pos['width'] / 2
            center_y = pos_y + original_pos['depth'] / 2
            
            # Main process label
            ax.text(center_x, center_y + 8, f"Process {process}",
                   ha='center', va='center', 
                   fontsize=18, fontweight='bold',
                   color='white',
                   bbox=dict(boxstyle='round,pad=0.6', facecolor='black', 
                            edgecolor='white', linewidth=2, alpha=0.95),
                   zorder=3)
            
            # Equipment count and group
            ax.text(center_x, center_y - 8, 
                   f"{layout['num_equipment']} Equipment | Group {layout['group']}",
                   ha='center', va='center', 
                   fontsize=13, fontweight='bold',
                   color='white',
                   zorder=3)
            
            # Grid layout
            ax.text(center_x, center_y - 18, 
                   f"Grid: {layout['rows']} × {layout['cols']}",
                   ha='center', va='center', 
                   fontsize=11,
                   color='white',
                   zorder=3)
            
            # Dimensions - POSITIONED WELL OUTSIDE blocks to avoid interference
            dim_offset = 15
            
            # Width annotation (top of block)
            ax.annotate('', 
                       xy=(pos_x, pos_y + original_pos['depth'] + dim_offset), 
                       xytext=(pos_x + original_pos['width'], pos_y + original_pos['depth'] + dim_offset),
                       arrowprops=dict(arrowstyle='<->', color='#2E8B57', lw=3))
            ax.text(center_x, pos_y + original_pos['depth'] + dim_offset + 6, 
                   f"{original_pos['width']:.0f} ft",
                   ha='center', va='bottom', fontsize=11, 
                   color='#2E8B57', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.95,
                            edgecolor='#2E8B57', linewidth=2))
            
            # Depth annotation (right of block)
            ax.annotate('', 
                       xy=(pos_x + original_pos['width'] + dim_offset, pos_y), 
                       xytext=(pos_x + original_pos['width'] + dim_offset, pos_y + original_pos['depth']),
                       arrowprops=dict(arrowstyle='<->', color='#2E8B57', lw=3))
            ax.text(pos_x + original_pos['width'] + dim_offset + 6, center_y, 
                   f"{original_pos['depth']:.0f} ft",
                   ha='left', va='center', fontsize=11, 
                   color='#2E8B57', fontweight='bold', rotation=90,
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='white', alpha=0.95,
                            edgecolor='#2E8B57', linewidth=2))
        
        # Set axis properties
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.2, linestyle='-', linewidth=0.5, color='gray')
        ax.set_xlabel('X Position (feet)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y Position (feet)', fontsize=14, fontweight='bold')
        ax.set_title('Fractal Factory Layout - Year 5, f=4 Centers\n'
                    'Optimized Parent Block Placement (Flow-Based)',
                    fontsize=20, fontweight='bold', pad=25)
        
        # Add comprehensive legend
        self._add_clean_legend(ax)
        
        # Add scale bar
        self._add_clean_scale_bar(ax)
        
        # Add statistics box
        self._add_clean_statistics_box(ax)
        
        plt.tight_layout()
        output_file = os.path.join(self.output_dir, "Final_Fractal_Layout_Clean.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✓ Clean final fractal layout saved to: {output_file}")
    
    def _draw_flow_connections(self, ax):
        """Draw flow connections between processes."""
        # Get all flows and sort
        flows = []
        for i in self.flow_matrix_df.index:
            for j in self.flow_matrix_df.columns:
                try:
                    flow_val = self.flow_matrix_df.loc[i, j]
                    flow = float(flow_val)
                    if flow > 0 and i in self.placement and j in self.placement:
                        flows.append((i, j, flow))
                except (ValueError, TypeError):
                    continue
        
        flows.sort(key=lambda x: x[2], reverse=True)
        top_flows = flows[:20]  # Show top 20 flows
        
        max_flow = max(f[2] for f in top_flows) if top_flows else 1
        
        for from_proc, to_proc, flow in top_flows:
            from_pos = self.placement[from_proc]
            to_pos = self.placement[to_proc]
            
            # Calculate centroids
            from_x = from_pos['x'] + from_pos['width'] / 2
            from_y = from_pos['y'] + from_pos['depth'] / 2
            to_x = to_pos['x'] + to_pos['width'] / 2
            to_y = to_pos['y'] + to_pos['depth'] / 2
            
            # Line width proportional to flow
            linewidth = 0.5 + (flow / max_flow) * 3
            alpha = 0.3 + (flow / max_flow) * 0.4
            
            ax.annotate('',
                       xy=(to_x, to_y),
                       xytext=(from_x, from_y),
                       arrowprops=dict(arrowstyle='->', 
                                     color='orange',
                                     lw=linewidth,
                                     alpha=alpha),
                       zorder=1)
    
    def _add_legend(self, ax):
        """Add legend showing process groups."""
        from matplotlib.patches import Patch
        
        legend_elements = []
        groups_added = set()
        
        for process in sorted(self.parent_blocks.keys()):
            layout = self.parent_blocks[process]
            group = layout['group']
            
            if group not in groups_added:
                legend_elements.append(
                    Patch(facecolor=layout['color'], edgecolor='black',
                         label=f"Group {group}")
                )
                groups_added.add(group)
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 fontsize=11, framealpha=0.9)
    
    def _add_clean_legend(self, ax):
        """Add clean, comprehensive legend showing all processes grouped."""
        from matplotlib.patches import Patch
        
        legend_elements = []
        
        # Group by process group
        groups = {}
        for process in sorted(self.parent_blocks.keys()):
            layout = self.parent_blocks[process]
            group = layout['group']
            if group not in groups:
                groups[group] = []
            groups[group].append((process, layout['color']))
        
        # Create legend entries
        for group in sorted(groups.keys()):
            # Add group header
            legend_elements.append(Patch(facecolor='none', edgecolor='none', 
                                        label=f'═══ {group} ═══'))
            # Add processes in group
            for process, color in groups[group]:
                legend_elements.append(Patch(facecolor=color, edgecolor='black',
                                            linewidth=1.5,
                                            label=f'  Process {process}'))
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 fontsize=10, framealpha=0.95, 
                 fancybox=True, shadow=True,
                 title='Process Groups', title_fontsize=12)
    
    def _add_scale_bar(self, ax):
        """Add scale bar to layout."""
        # Get axis limits
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Scale bar in bottom right
        scale_length = 100  # 100 feet
        x_start = xlim[1] - scale_length - 50
        y_pos = ylim[0] + 30
        
        ax.plot([x_start, x_start + scale_length], 
               [y_pos, y_pos], 
               'k-', linewidth=4)
        ax.text(x_start + scale_length/2, y_pos - 10, 
               f'{scale_length} feet',
               ha='center', fontsize=12, fontweight='bold')
    
    def _add_clean_scale_bar(self, ax):
        """Add professional scale bar to layout."""
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Scale bar in bottom right with professional styling
        scale_length = 100  # 100 feet
        margin = 60
        x_start = xlim[1] - scale_length - margin
        y_pos = ylim[0] + 40
        
        # Draw scale bar with ticks
        ax.plot([x_start, x_start + scale_length], 
               [y_pos, y_pos], 
               'k-', linewidth=5, solid_capstyle='butt')
        
        # Add tick marks
        for i in range(5):
            x_tick = x_start + i * (scale_length / 4)
            ax.plot([x_tick, x_tick], [y_pos - 3, y_pos + 3],
                   'k-', linewidth=3)
        
        # Add labels
        ax.text(x_start + scale_length/2, y_pos - 15, 
               f'Scale: {scale_length} feet',
               ha='center', fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                        edgecolor='black', linewidth=2))
    
    def _add_statistics_box(self, ax):
        """Add statistics box to layout."""
        total_area = sum(layout['area_sqft'] for layout in self.parent_blocks.values())
        total_equipment = sum(layout['num_equipment'] for layout in self.parent_blocks.values())
        avg_utilization = np.mean([layout['utilization'] for layout in self.parent_blocks.values()])
        
        stats_text = (f"Total Equipment: {total_equipment}\n"
                     f"Total Area: {total_area:,.0f} sq ft\n"
                     f"Avg Utilization: {avg_utilization:.1%}")
        
        ax.text(0.02, 0.98, stats_text,
               transform=ax.transAxes,
               fontsize=11,
               verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    def _add_clean_statistics_box(self, ax):
        """Add comprehensive statistics box to layout."""
        total_area = sum(layout['area_sqft'] for layout in self.parent_blocks.values())
        total_equipment = sum(layout['num_equipment'] for layout in self.parent_blocks.values())
        avg_utilization = np.mean([layout['utilization'] for layout in self.parent_blocks.values()])
        total_spaces = sum(layout['total_spaces'] for layout in self.parent_blocks.values())
        
        stats_text = (f"FACTORY STATISTICS\n"
                     f"{'─'*25}\n"
                     f"Total Equipment: {total_equipment}\n"
                     f"Total Spaces: {total_spaces}\n"
                     f"Total Block Area: {total_area:,.0f} sq ft\n"
                     f"Avg Utilization: {avg_utilization:.1%}\n"
                     f"Process Count: {len(self.parent_blocks)}")
        
        ax.text(0.02, 0.98, stats_text,
               transform=ax.transAxes,
               fontsize=11,
               verticalalignment='top',
               fontfamily='monospace',
               bbox=dict(boxstyle='round,pad=0.8', facecolor='lightyellow', 
                        edgecolor='black', linewidth=2, alpha=0.95))
    
    def visualize_detailed_fractal_with_child_blocks(self):
        """
        Create DETAILED fractal layout showing each parent block 
        with all child machine blocks inside.
        
        This is the complete fractal visualization showing the hierarchy.
        STARTS FROM ORIGIN (0, 0)
        """
        print("\n" + "="*100)
        print("GENERATING DETAILED FRACTAL LAYOUT WITH CHILD BLOCKS")
        print("="*100)
        
        fig, ax = plt.subplots(figsize=(36, 30), facecolor='white')
        ax.set_facecolor('#F8F9FA')  # Very light gray background
        
        # Calculate layout bounds to ensure all blocks are visible
        min_x = min(p['x'] for p in self.placement.values())
        max_x = max(p['x'] + p['width'] for p in self.placement.values())
        min_y = min(p['y'] for p in self.placement.values())
        max_y = max(p['y'] + p['depth'] for p in self.placement.values())
        
        # START FROM ORIGIN: Shift all coordinates
        x_offset = -min_x
        y_offset = -min_y
        
        # Calculate final dimensions after offset
        final_max_x = max_x + x_offset
        final_max_y = max_y + y_offset
        
        # Add generous padding around the entire layout
        padding = 80
        ax.set_xlim(-10, final_max_x + padding)
        ax.set_ylim(-10, final_max_y + padding)
        
        # Draw each parent block with ALL child machines inside
        for process, original_pos in self.placement.items():
            layout = self.parent_blocks[process]
            spec = self.area_specs[process]
            
            # Apply offset for origin-based display
            pos_x = original_pos['x'] + x_offset
            pos_y = original_pos['y'] + y_offset
            
            # Draw parent block boundary
            parent_rect = Rectangle(
                (pos_x, pos_y), original_pos['width'], original_pos['depth'],
                linewidth=4.5, 
                edgecolor='black',
                facecolor='none',  # Transparent fill
                linestyle='-',
                zorder=1
            )
            ax.add_patch(parent_rect)
            
            # Add parent block label at the top
            center_x = pos_x + original_pos['width'] / 2
            ax.text(center_x, pos_y + original_pos['depth'] + 8, 
                   f"PROCESS {process}",
                   ha='center', va='bottom', 
                   fontsize=16, fontweight='bold',
                   color='black',
                   bbox=dict(boxstyle='round,pad=0.7', facecolor=layout['color'], 
                            edgecolor='black', linewidth=2.5, alpha=0.95),
                   zorder=5)
            
            # Draw individual child machine blocks inside parent
            rows = layout['rows']
            cols = layout['cols']
            machine_w = layout['machine_width']
            machine_d = layout['machine_depth']
            
            # Calculate spacing - MUST MATCH PARENT BLOCK CALCULATION
            # CRITICAL: rows controls WIDTH (X), cols controls DEPTH (Y)
            # r iterates rows → X position, c iterates cols → Y position
            if 'left' in spec['Shareable_Sides'] and 'right' in spec['Shareable_Sides']:
                # KLM case: left/right sharing along depth dimension
                # effective_depth = depth * cols - shared_allowance * (cols - 1)
                width_spacing = machine_w  # Full width, no sharing
                depth_spacing = machine_d - spec['Shared_Allowance_ft']  # Depth with sharing
            elif 'front' in spec['Shareable_Sides']:
                # ABCD case: sharing on both dimensions
                width_spacing = machine_w - spec['Shared_Allowance_ft']
                depth_spacing = machine_d - spec['Shared_Allowance_ft']
            else:
                width_spacing = machine_w
                depth_spacing = machine_d
            
            # Draw each child machine
            machine_count = 0
            for r in range(rows):
                for c in range(cols):
                    # r controls X (width), c controls Y (depth)
                    machine_x = pos_x + r * width_spacing
                    machine_y = pos_y + c * depth_spacing
                    
                    if machine_count < layout['num_equipment']:
                        # Active machine - filled
                        machine_rect = Rectangle(
                            (machine_x, machine_y), machine_w, machine_d,
                            linewidth=1.8, 
                            edgecolor='black',
                            facecolor=layout['color'], 
                            alpha=0.75,
                            zorder=2
                        )
                        ax.add_patch(machine_rect)
                        
                        # Add machine number
                        ax.text(machine_x + machine_w/2, machine_y + machine_d/2, 
                               f"{machine_count+1}",
                               ha='center', va='center', 
                               fontsize=9, fontweight='bold',
                               color='white',
                               bbox=dict(boxstyle='circle,pad=0.25', 
                                       facecolor='black', alpha=0.85),
                               zorder=3)
                        
                        machine_count += 1
                    else:
                        # Unused space - hatched
                        machine_rect = Rectangle(
                            (machine_x, machine_y), machine_w, machine_d,
                            linewidth=1.2, 
                            edgecolor='gray',
                            facecolor='white', 
                            alpha=0.4,
                            hatch='///',
                            linestyle='--',
                            zorder=2
                        )
                        ax.add_patch(machine_rect)
            
            # Add info box for each parent block
            info_text = (f"{layout['num_equipment']} machines\n"
                        f"{layout['rows']}×{layout['cols']} grid\n"
                        f"{layout['width_ft']}'×{layout['depth_ft']}'")
            ax.text(pos_x + 8, pos_y + 8, info_text,
                   ha='left', va='bottom', 
                   fontsize=10,
                   color='black',
                   bbox=dict(boxstyle='round,pad=0.5', 
                            facecolor='white', 
                            edgecolor='gray', 
                            linewidth=1.5, 
                            alpha=0.90),
                   zorder=4)
        
        # Set axis properties
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.20, linestyle='-', linewidth=0.7, color='gray')
        ax.set_xlabel('X Position (feet)', fontsize=18, fontweight='bold')
        ax.set_ylabel('Y Position (feet)', fontsize=18, fontweight='bold')
        ax.set_title('Detailed Fractal Factory Layout - Year 5, f=4 Centers\n'
                    'Complete View: Parent Blocks with All Child Machine Blocks Inside',
                    fontsize=24, fontweight='bold', pad=35)
        ax.tick_params(labelsize=14)
        
        # Add comprehensive legend
        self._add_detailed_legend(ax)
        
        # Add scale bar
        self._add_clean_scale_bar(ax)
        
        # Add statistics
        self._add_clean_statistics_box(ax)
        
        plt.tight_layout()
        output_file = os.path.join(self.output_dir, "Detailed_Fractal_Layout_With_Child_Blocks.png")
        plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
        plt.close()
        
        print(f"✓ Detailed fractal layout with child blocks saved to: {output_file}")
    
    def _add_detailed_legend(self, ax):
        """Add detailed legend for child blocks visualization."""
        from matplotlib.patches import Patch, Rectangle as LegendRect
        
        legend_elements = []
        
        # Add explanation of symbols
        legend_elements.append(Patch(facecolor='none', edgecolor='none', 
                                    label='═══ LEGEND ═══'))
        legend_elements.append(Rectangle((0, 0), 1, 1, 
                                        facecolor='gray', edgecolor='black',
                                        label='■ Active Machine'))
        legend_elements.append(Rectangle((0, 0), 1, 1, 
                                        facecolor='white', edgecolor='gray',
                                        hatch='///', linestyle='--',
                                        label='▨ Unused Space'))
        legend_elements.append(Rectangle((0, 0), 1, 1, 
                                        facecolor='none', edgecolor='black',
                                        linewidth=3,
                                        label='□ Parent Block'))
        
        # Add process groups
        legend_elements.append(Patch(facecolor='none', edgecolor='none', 
                                    label='\n═══ PROCESSES ═══'))
        
        groups = {}
        for process in sorted(self.parent_blocks.keys()):
            layout = self.parent_blocks[process]
            group = layout['group']
            if group not in groups:
                groups[group] = []
            groups[group].append((process, layout['color']))
        
        for group in sorted(groups.keys()):
            for process, color in groups[group]:
                legend_elements.append(Patch(facecolor=color, edgecolor='black',
                                            linewidth=1,
                                            label=f'  {process} ({group})'))
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 fontsize=9, framealpha=0.95, 
                 fancybox=True, shadow=True,
                 title='Legend & Process Map', title_fontsize=11)
    
    def calculate_layout_metrics(self) -> Dict:
        """
        Calculate comprehensive layout performance metrics.
        
        Returns:
            Dictionary of metrics
        """
        print("\n" + "="*100)
        print("CALCULATING LAYOUT PERFORMANCE METRICS")
        print("="*100)
        
        # Total flow × distance
        total_flow_distance = 0
        
        for i in self.placement.keys():
            for j in self.placement.keys():
                if i != j:
                    try:
                        flow_val = self.flow_matrix_df.loc[i, j]
                        flow = float(flow_val)
                        if flow > 0:
                            # Calculate distance
                            i_x = self.placement[i]['x'] + self.placement[i]['width'] / 2
                            i_y = self.placement[i]['y'] + self.placement[i]['depth'] / 2
                            j_x = self.placement[j]['x'] + self.placement[j]['width'] / 2
                            j_y = self.placement[j]['y'] + self.placement[j]['depth'] / 2
                            
                            distance = math.sqrt((i_x - j_x)**2 + (i_y - j_y)**2)
                            total_flow_distance += flow * distance
                    except (ValueError, TypeError):
                        pass
                    except:
                        continue
        
        # Layout bounds
        min_x = min(p['x'] for p in self.placement.values())
        max_x = max(p['x'] + p['width'] for p in self.placement.values())
        min_y = min(p['y'] for p in self.placement.values())
        max_y = max(p['y'] + p['depth'] for p in self.placement.values())
        
        layout_width = max_x - min_x
        layout_height = max_y - min_y
        total_footprint = layout_width * layout_height
        
        total_block_area = sum(layout['area_sqft'] for layout in self.parent_blocks.values())
        space_utilization = total_block_area / total_footprint
        
        metrics = {
            'total_flow_distance': total_flow_distance,
            'layout_width_ft': layout_width,
            'layout_height_ft': layout_height,
            'total_footprint_sqft': total_footprint,
            'total_block_area_sqft': total_block_area,
            'space_utilization': space_utilization,
            'layout_aspect_ratio': max(layout_width, layout_height) / min(layout_width, layout_height)
        }
        
        print(f"\n  Total Flow × Distance: {total_flow_distance:,.0f} unit-feet")
        print(f"  Layout Dimensions: {layout_width:.1f}' × {layout_height:.1f}'")
        print(f"  Total Footprint: {total_footprint:,.0f} sq ft")
        print(f"  Block Area: {total_block_area:,.0f} sq ft")
        print(f"  Space Utilization: {space_utilization:.1%}")
        print(f"  Layout Aspect Ratio: {metrics['layout_aspect_ratio']:.2f}")
        
        return metrics
    
    def export_placement_csv(self):
        """Export placement coordinates to CSV."""
        output_file = os.path.join(self.output_dir, "Block_Placement_Coordinates.csv")
        
        data = []
        for process in sorted(self.placement.keys()):
            pos = self.placement[process]
            layout = self.parent_blocks[process]
            
            data.append({
                'Process': process,
                'Group': layout['group'],
                'X_Position_ft': pos['x'],
                'Y_Position_ft': pos['y'],
                'Width_ft': pos['width'],
                'Depth_ft': pos['depth'],
                'Center_X_ft': pos['x'] + pos['width'] / 2,
                'Center_Y_ft': pos['y'] + pos['depth'] / 2,
                'Area_sqft': layout['area_sqft']
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        
        print(f"\n✓ Block placement coordinates exported to: {output_file}")
    
    def export_centroids_origin_based_csv(self):
        """
        Export centroid coordinates with origin-based layout (starting at 0,0).
        This provides the final clean coordinates for the flow-optimized layout.
        """
        # Calculate offsets to shift layout to origin
        min_x = min(p['x'] for p in self.placement.values())
        min_y = min(p['y'] for p in self.placement.values())
        
        x_offset = -min_x
        y_offset = -min_y
        
        output_file = os.path.join(self.output_dir, "Parent_Block_Centroids_Origin_Based.csv")
        
        data = []
        for process in sorted(self.placement.keys()):
            pos = self.placement[process]
            layout = self.parent_blocks[process]
            
            # Calculate origin-based coordinates
            origin_x = pos['x'] + x_offset
            origin_y = pos['y'] + y_offset
            center_x = origin_x + pos['width'] / 2
            center_y = origin_y + pos['depth'] / 2
            
            data.append({
                'Process': process,
                'Group': layout['group'],
                'Equipment_Count': layout['num_equipment'],
                'Grid_Layout': f"{layout['rows']}×{layout['cols']}",
                'Block_Width_ft': pos['width'],
                'Block_Depth_ft': pos['depth'],
                'Block_Area_sqft': layout['area_sqft'],
                'Origin_Based_X_ft': round(origin_x, 2),
                'Origin_Based_Y_ft': round(origin_y, 2),
                'Centroid_X_ft': round(center_x, 2),
                'Centroid_Y_ft': round(center_y, 2)
            })
        
        df = pd.DataFrame(data)
        df.to_csv(output_file, index=False)
        
        print(f"\n✓ Parent block centroids (origin-based) exported to: {output_file}")
        return df
    
    def run_complete_analysis(self):
        """
        Run complete fractal layout analysis pipeline.
        
        Steps:
        1. Generate parent blocks
        2. Export specifications
        3. Visualize individual blocks (combined + separate PNGs)
        4. Optimize placement
        5. Visualize final layout (clean version)
        6. Visualize detailed layout with child blocks
        7. Calculate metrics
        8. Export placement data
        """
        print("\n" + "="*100)
        print("FRACTAL LAYOUT GENERATOR - COMPLETE ANALYSIS PIPELINE")
        print("Year 5, f=4 Centers")
        print("="*100)
        
        # Step 1: Generate parent blocks
        self.generate_all_parent_blocks()
        
        # Step 2: Export specifications
        self.export_parent_blocks_csv()
        
        # Step 3: Visualize individual blocks (combined + individual PNGs)
        self.visualize_individual_parent_blocks()
        
        # Step 4: Optimize placement
        self.optimize_placement()
        
        # Step 5: Export placement
        self.export_placement_csv()
        
        # Step 6: Calculate metrics
        metrics = self.calculate_layout_metrics()
        
        # Step 7: Export centroid coordinates (origin-based)
        self.export_centroids_origin_based_csv()
        
        # Step 8: Visualize clean final layout
        self.visualize_final_layout()
        
        # Step 9: Visualize detailed layout with child blocks
        self.visualize_detailed_fractal_with_child_blocks()
        
        print("\n" + "="*100)
        print("✓ COMPLETE ANALYSIS FINISHED SUCCESSFULLY")
        print("="*100)
        print(f"\nAll outputs saved to: {self.output_dir}")
        print("\nGenerated Files:")
        print("  1. Parent_Block_Specifications.csv - Detailed block specs")
        print("  2. Block_Placement_Coordinates.csv - Spatial coordinates (raw optimization)")
        print("  3. Parent_Block_Centroids_Origin_Based.csv - Centroid coordinates starting at origin")
        print("  4. Parent_Blocks_Group_ABCD.png - Group ABCD overview (processes A, B, C, D)")
        print("  5. Parent_Blocks_Group_EFG.png - Group EFG overview (processes E, F, G)")
        print("  6. Parent_Blocks_Group_HIJ.png - Group HIJ overview (processes H, I, J)")
        print("  7. Parent_Blocks_Group_KLM.png - Group KLM overview (processes K, L, M)")
        print("  8. Parent_Block_[A-M].png - Individual process PNGs (13 files)")
        print("  9. Final_Fractal_Layout_Clean.png - Clean overview layout (origin-based)")
        print(" 10. Detailed_Fractal_Layout_With_Child_Blocks.png - Complete fractal view (origin-based)")
        
        return metrics


def main():
    """Main execution function."""
    # File paths
    base_dir = r"d:\Adarsh GATech Files\6335 Benoit SC1\CW3\ISYE6202_CW3"
    equipment_file = os.path.join(base_dir, "results", "task4", "Fractal", 
                                  "Fractal_Design", "Year5_Fractal_f4_Equipment_Requirements.csv")
    flow_matrix_file = os.path.join(base_dir, "results", "task4", "Fractal", 
                                    "Fractal_Flowmatrix", "year5", "f4_centers",
                                    "Aggregate_Factory_Flow_Matrix.csv")
    output_dir = os.path.join(base_dir, "results", "task4", "Fractal", "Adarsh")
    
    # Create generator
    generator = FractalLayoutGenerator(equipment_file, flow_matrix_file, output_dir)
    
    # Run complete analysis
    metrics = generator.run_complete_analysis()
    
    print("\n" + "="*100)
    print("SUMMARY OF KEY FINDINGS")
    print("="*100)
    
    print("\nParent Block Summary:")
    for process in sorted(generator.parent_blocks.keys()):
        layout = generator.parent_blocks[process]
        print(f"  {process}: {layout['rows']}×{layout['cols']} grid, "
              f"{layout['width_ft']}'×{layout['depth_ft']}', "
              f"{layout['area_sqft']} sq ft, "
              f"Util: {layout['utilization']:.1%}")
    
    print(f"\nLayout Performance:")
    print(f"  Total Flow×Distance: {metrics['total_flow_distance']:,.0f} unit-feet")
    print(f"  Space Utilization: {metrics['space_utilization']:.1%}")
    print(f"  Layout Footprint: {metrics['total_footprint_sqft']:,.0f} sq ft")


if __name__ == "__main__":
    main()
