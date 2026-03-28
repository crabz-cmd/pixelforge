#!/usr/bin/env python3
# ================= OPTIMISATION AUTOMATIQUE DES IMAGES - PIXELFORGE =================

import os
import sys
from pathlib import Path
from datetime import datetime

# Verifier si Pillow est disponible
try:
    from PIL import Image
    from PIL import ImageEnhance
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Configuration
CONFIG = {
    'webp_quality': 82,
    'max_width': 1200,
    'target_sizes': {
        'logo': 50,        # KB
        'large': 100,      # KB
        'medium': 80,      # KB
        'small': 50        # KB
    }
}

# Images a optimiser
IMAGES_TO_OPTIMIZE = [
    {'name': 'logo1.png', 'priority': 'critical', 'target_kb': CONFIG['target_sizes']['logo']},
    {'name': 'spa.png', 'priority': 'high', 'target_kb': CONFIG['target_sizes']['large']},
    {'name': 'resto.png', 'priority': 'high', 'target_kb': CONFIG['target_sizes']['large']},
    {'name': 'osalondeli.png', 'priority': 'high', 'target_kb': CONFIG['target_sizes']['large']},
    {'name': 'mecton-before.png', 'priority': 'high', 'target_kb': CONFIG['target_sizes']['large']},
    {'name': 'plombier.png', 'priority': 'medium', 'target_kb': CONFIG['target_sizes']['medium']},
    {'name': 'mecton.png', 'priority': 'medium', 'target_kb': CONFIG['target_sizes']['medium']},
    {'name': 'mecton-main.png', 'priority': 'medium', 'target_kb': CONFIG['target_sizes']['medium']},
    {'name': 'mecton-shot2.png', 'priority': 'low', 'target_kb': CONFIG['target_sizes']['small']},
    {'name': 'mecton-shot1.png', 'priority': 'low', 'target_kb': CONFIG['target_sizes']['small']},
]

def get_priority_icon(priority):
    """Retourne l'emoji de priorite"""
    icons = {
        'critical': 'CRITICAL',
        'high': 'HIGH',
        'medium': 'MEDIUM',
        'low': 'LOW'
    }
    return icons.get(priority, 'LOW')

def get_file_size_kb(filepath):
    """Retourne la taille en KB"""
    try:
        return os.path.getsize(filepath) / 1024
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0

def optimize_image(input_path, output_path, target_kb, config_key):
    """Optimise une image et la convertit en WebP"""
    try:
        print(f"\nOptimizing {input_path.name}...")

        if not PIL_AVAILABLE:
            print("Pillow not available - Simulation only")
            return False

        # Ouvrir l'image
        with Image.open(input_path) as img:
            # Redimensionner si necessaire
            if img.width > CONFIG['max_width']:
                ratio = CONFIG['max_width'] / img.width
                new_height = int(img.height * ratio)
                img = img.resize((CONFIG['max_width'], new_height), Image.LANCZOS)
                print(f"   Resized: {img.width}px -> {CONFIG['max_width']}px")

            # Convertir en RGB si necessaire (pour WebP)
            if img.mode in ('RGBA', 'P', 'L'):
                img = img.convert('RGB')

            # Sauvegarder en WebP
            img.save(output_path, 'WEBP', quality=CONFIG['webp_quality'], optimize=True)

            # Verifier la taille
            new_size_kb = get_file_size_kb(output_path)

            print(f"   Original size: {target_kb:.0f} KB")
            print(f"   Optimized size: {new_size_kb:.0f} KB")

            if new_size_kb > target_kb:
                print(f"   Warning: Still above target ({target_kb:.0f} KB)")
            else:
                print(f"   Target achieved!")

            return True

    except Exception as e:
        print(f"Error optimizing {input_path.name}: {e}")
        return False

def main():
    print("===========================================")
    print("OPTIMISATION AUTOMATIQUE DES IMAGES - PIXELFORGE")
    print("===========================================")
    print()

    if not PIL_AVAILABLE:
        print("WARNING: Pillow (PIL) not installed")
        print("   Install: pip install Pillow")
        print("   Continuing without real optimization...\n")

    # Repertoire courant
    current_dir = Path(__file__).parent

    print(f"Working directory: {current_dir}")
    print()

    print("===========================================")
    print("PRE-OPTIMISATION REPORT")
    print("===========================================")
    print()

    # Analyser les images actuelles
    results = []
    total_current_size = 0
    total_target_size = 0

    for img_info in IMAGES_TO_OPTIMIZE:
        input_path = current_dir / img_info['name']

        if input_path.exists():
            current_size = get_file_size_kb(input_path)
            total_current_size += current_size

            results.append({
                'name': img_info['name'],
                'current_size_kb': current_size,
                'target_kb': img_info['target_kb'],
                'needs_optimization': current_size > img_info['target_kb'],
                'priority': img_info['priority']
            })

            print(f"{get_priority_icon(img_info['priority'])} {img_info['name']}")
            print(f"   Current size: {current_size:.2f} KB")
            print(f"   Target: <{img_info['target_kb']} KB")
            print(f"   Priority: {img_info['priority']}")
        else:
            print(f"Missing file: {img_info['name']}")

        total_target_size += img_info['target_kb']

    # Resume
    print("\n")
    print("===========================================")
    print("SUMMARY")
    print("===========================================")
    print()

    print(f"Total current size: {total_current_size:.2f} KB")
    print(f"Total target size: {total_target_size:.2f} KB")

    total_target_size_kb = sum(r['target_kb'] for r in results)
    savings = total_current_size - total_target_size_kb
    savings_percent = (savings / total_current_size) * 100 if total_current_size > 0 else 0

    print(f"Potential savings: {savings:.2f} KB ({savings_percent:.1f}%)")
    print()

    # Images qui necessitent une optimisation
    needs_opt = [r for r in results if r['needs_optimization']]
    print(f"Images to optimize: {len(needs_opt)}/{len(results)}")

    if needs_opt:
        print("\nPriorities:")
        print("   CRITICAL: logo1.png (2.1 MB -> <50 KB)")
        print("   HIGH: spa.png, resto.png, osalondeli.png, mecton-before.png")
        print("   MEDIUM: plombier.png, mecton.png, mecton-main.png")
        print("   LOW: mecton-shot2.png, mecton-shot1.png")

        # Optimisation reelle si Pillow disponible
        if PIL_AVAILABLE:
            print("\n===========================================")
            print("STARTING OPTIMISATION")
            print("===========================================")
            print()

            optimized_count = 0
            failed_count = 0

            for img_info in IMAGES_TO_OPTIMIZE:
                input_path = current_dir / img_info['name']
                output_path = current_dir / f"{Path(img_info['name']).stem}.webp"

                if input_path.exists():
                    success = optimize_image(
                        input_path,
                        output_path,
                        img_info['target_kb'],
                        img_info['name']
                    )

                    if success:
                        optimized_count += 1
                    else:
                        failed_count += 1

            print("\n")
            print("===========================================")
            print("OPTIMISATION RESULTS")
            print("===========================================")
            print()

            print(f"Optimized images: {optimized_count}/{len(IMAGES_TO_OPTIMIZE)}")
            if failed_count > 0:
                print(f"Failed images: {failed_count}")

        else:
            print("\n===========================================")
            print("INSTRUCTIONS")
            print("===========================================")
            print()
            print("To optimize images, use one of these tools:")
            print()
            print("   1. https://tinypng.com/ (Recommended - FREE)")
            print("   2. https://squoosh.app/ (WebP support - FREE)")
            print("   3. ImageOptim (Mac) / FileOptimizer (Windows)")
            print()
            print("Steps:")
            print("   1. Drag & drop images on the tool")
            print("   2. Download optimized files")
            print("   3. Rename to .webp")
            print("   4. Save in PixelForge2 directory")
            print("   5. Update index.html with <picture> tags")

    # Generer un rapport
    report_path = current_dir / 'IMAGE_OPTIMIZATION_DETAILED.txt'
    timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

    report_content = f"""
OPTIMISATION DES IMAGES - RAPPORT DETAILE
================================================
Date: {timestamp}
Directory: {current_dir}

TOTALS
--------------------------------------------------
Images analyzed: {len(results)}
Total current size: {total_current_size:.2f} KB
Total target size: {total_target_size_kb:.2f} KB
Potential savings: {savings:.2f} KB ({savings_percent:.1f}%)

DETAILS BY IMAGE
--------------------------------------------------
"""

    for r in results:
        report_content += f"""
{r['name']}
- Current size: {r['current_size_kb']:.2f} KB
- Target: <{r['target_kb']} KB
- Priority: {r['priority']}
- Status: {'Needs optimization' if r['needs_optimization'] else 'OK (optimized)'}
"""

    report_content += """
==================================================
"""

    report_path.write_text(report_content, encoding='utf-8')
    print(f"\nDetailed report saved: {report_path.name}")

    # Instructions finales
    print("\n")
    print("===========================================")
    print("NEXT STEPS")
    print("===========================================")
    print()

    if PIL_AVAILABLE and optimized_count > 0:
        print("Completed steps:")
        print("   1. Images optimized to WebP ✓")
        print("   2. Detailed report generated ✓")
        print("   3. Next steps:")
        print("      a. Update index.html with <picture> tags")
        print("      b. Add descriptive alt texts")
        print("      c. Add loading='lazy' to images")
        print("      d. Test the site")
        print("      e. Verify Lighthouse score")
    else:
        print("To complete:")
        print("   1. Optimize images with TinyPNG or Squoosh")
        print("   2. Convert to WebP")
        print("   3. Save .webp files")
        print("   4. Update index.html")
        print("   5. Test the site")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nCritical error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
