#!/usr/bin/env python3
"""
Script to convert SVG icons to PNG for pygbag compatibility.
Run this once to generate PNG versions of icon files.
"""

import pygame
import os
import re
import io

pygame.init()
pygame.display.set_mode((100, 100))  # Need display for convert_alpha

icons_dir = "assets/icons"
svg_files = [f for f in os.listdir(icons_dir) if f.endswith(".svg")]

for svg_file in svg_files:
    svg_path = os.path.join(icons_dir, svg_file)
    png_path = os.path.join(icons_dir, svg_file.replace(".svg", ".png"))

    # Read and modify SVG for proper sizing
    with open(svg_path, "r") as f:
        content = f.read()

    # Set explicit size in SVG
    target_size = 64
    svg_tag_match = re.search(r"<svg[^>]*>", content)
    if svg_tag_match:
        tag_content = svg_tag_match.group(0)

        # Update or add width
        if 'width="' in tag_content:
            tag_content = re.sub(
                r'(?<!-)width="[^"]*"', f'width="{target_size}"', tag_content
            )
        else:
            tag_content = tag_content.replace("<svg", f'<svg width="{target_size}"')

        # Update or add height
        if 'height="' in tag_content:
            tag_content = re.sub(
                r'(?<!-)height="[^"]*"', f'height="{target_size}"', tag_content
            )
        else:
            tag_content = tag_content.replace("<svg", f'<svg height="{target_size}"')

        content = content.replace(svg_tag_match.group(0), tag_content)

    # Load SVG with pygame
    bio = io.BytesIO(content.encode("utf-8"))
    try:
        image = pygame.image.load(bio, "icon.svg").convert_alpha()
        image = pygame.transform.scale(image, (target_size, target_size))
        pygame.image.save(image, png_path)
        print(f"Converted: {svg_file} -> {png_path}")
    except Exception as e:
        print(f"Failed to convert {svg_file}: {e}")

pygame.quit()
print("Done!")
