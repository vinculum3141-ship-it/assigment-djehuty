# Manual Slide Export Guide

Since automated print-to-PDF has challenges with complex Reveal.js presentations, here's the recommended manual approach using browser zoom and capture.

---

## 🎯 Recommended Approach: Browser Zoom + Screen Capture

This gives you full control over exactly how slides appear in the final PDF.

---

## Method 1: Browser Zoom + Screenshot (Recommended)

### Step 1: Optimize Browser View
```bash
# Open presentation in Chromium
cd /home/ruby/Projects/assigment-djehuty/presentation
chromium-browser index.html

# Press F11 for fullscreen mode (removes browser chrome)
# This gives maximum screen real estate
```

### Step 2: Set Optimal Zoom Level
```bash
# Try these zoom levels to fit content perfectly:
- Ctrl+0 (reset to 100%)
- Ctrl+Minus (zoom out to 90%, 80%, 75%)
- Ctrl+Plus (zoom in if needed)

# Find the zoom level where:
✅ Title visible at top
✅ Bottom content visible
✅ No scrolling needed
✅ Text still readable

# Typical sweet spot: 75-85% zoom
```

### Step 3: Capture Each Slide
```bash
# For each slide:
1. Navigate to slide (arrow keys or click)
2. Adjust zoom if needed (Ctrl+Plus/Minus)
3. Take screenshot:
   - Press PrintScreen (full screen)
   - Or: Shift+PrintScreen (select area)
   - Or: Use Flameshot/Shutter for better control

4. Save as: slide-01.png, slide-02.png, etc.
5. Press → (right arrow) for next slide
6. Repeat
```

### Step 4: Convert to PDF
```bash
# Install ImageMagick if needed
sudo apt install imagemagick

# Convert all screenshots to single PDF (A4 landscape)
cd ~/Pictures/screenshots  # or wherever you saved them

convert slide-*.png \
    -resize 1754x1240 \
    -gravity center \
    -extent 1754x1240 \
    -quality 90 \
    presentation.pdf

# For A4 landscape at 150 DPI:
# Width: 297mm = 1754px at 150 DPI
# Height: 210mm = 1240px at 150 DPI
```

---

## Method 2: Chrome DevTools Device Emulation

More precise control over viewport size.

### Steps:
```bash
1. Open presentation in Chromium
2. Press F12 (open DevTools)
3. Press Ctrl+Shift+M (toggle device toolbar)
4. Set custom dimensions:
   - Width: 1920px (or 1280px for 13" laptop sim)
   - Height: 1080px (or 800px)
   - Device scale: 1.0

5. For each slide:
   - Navigate to slide
   - Press Ctrl+Shift+P
   - Type: "screenshot"
   - Select: "Capture full size screenshot"
   - Saves automatically

6. Repeat for all 16 slides
```

---

## Method 3: Browser Print to Images (Alternative)

Some browsers can print individual pages as images.

### Firefox Approach:
```bash
1. Open in Firefox
2. Ctrl+P (Print)
3. Destination: "Print to File"
4. Format: PDF
5. Print Range: Pages 1-1 (one at a time)
6. Repeat for each slide

# Then split PDF if needed:
pdftk presentation.pdf burst output slide-%02d.pdf
```

---

## Method 4: Use External Tool - Decktape

Decktape is specifically designed for exporting Reveal.js presentations.

### Install:
```bash
# Using npm
npm install -g decktape

# Or use Docker (no installation needed)
```

### Export:
```bash
# Navigate to presentation directory
cd /home/ruby/Projects/assigment-djehuty/presentation

# Export with decktape
decktape reveal index.html slides.pdf \
    --size 1920x1080 \
    --pause 500

# For better quality:
decktape reveal index.html slides.pdf \
    --size 2560x1440 \
    --pause 1000 \
    --load-pause 2000

# Docker version (no installation):
docker run --rm -t -v $(pwd):/slides astefanutti/decktape \
    reveal index.html slides.pdf \
    --size 1920x1080
```

---

## 📋 Recommended Workflow Summary

**Easiest (5 minutes):**
```bash
1. Open presentation in fullscreen (F11)
2. Zoom to 80% (Ctrl+Minus twice)
3. Take 16 screenshots (PrintScreen for each slide)
4. Use ImageMagick convert to create PDF
```

**Most Accurate (10 minutes):**
```bash
1. Open DevTools (F12)
2. Enable device toolbar (Ctrl+Shift+M)
3. Set viewport: 1920x1080
4. Capture full-size screenshot for each slide (Ctrl+Shift+P)
5. Convert to PDF
```

**Most Automated (if it works):**
```bash
npm install -g decktape
decktape reveal index.html slides.pdf --size 1920x1080 --pause 500
```

---

## 🎨 Post-Processing Tips

### If slides need editing:
```bash
# Install GIMP for image editing
sudo apt install gimp

# Batch process with ImageMagick:
# Add borders:
convert slide-*.png -border 20x20 -bordercolor white bordered-%02d.png

# Adjust brightness/contrast:
convert slide-*.png -brightness-contrast 5x10 adjusted-%02d.png

# Crop if needed:
convert slide-*.png -crop 1920x1000+0+40 cropped-%02d.png
```

### Create PDF with specific settings:
```bash
# High quality A4 landscape PDF
convert slide-*.png \
    -page A4 \
    -rotate 90 \
    -gravity center \
    -quality 95 \
    -density 300 \
    presentation-final.pdf

# Compress if file is too large:
gs -sDEVICE=pdfwrite \
   -dCompatibilityLevel=1.4 \
   -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH \
   -sOutputFile=compressed.pdf \
   presentation-final.pdf
```

---

## 📊 Quick Reference: Slide List

You have **16 slides** to capture:

1. Title slide (Faculty-Level Statistics)
2. Problem Statement (Organizations field chaos)
3. Solution Overview
4. Technical Architecture
5. Entity Relationship Diagram
6. Data Model Example
7. **NEW** Working Prototype Dashboard
8. Implementation Timeline
9. Migration Strategy
10. Edge Cases Handling
11. Before/After Comparison
12. Benefits Overview
13. System Strengths
14. Areas for Improvement
15. Success Metrics
16. Summary & Questions

---

## 🚀 Fast Track: 3-Minute Export

```bash
# 1. Open fullscreen
chromium-browser index.html
# Press F11

# 2. Zoom to fit
# Press Ctrl+Minus twice (to 80%)

# 3. Install screenshot tool if needed
sudo apt install flameshot

# 4. Capture all slides
# Press PrintScreen for each of 16 slides
# Flameshot will let you select exact area

# 5. Convert to PDF
cd ~/Pictures
convert screenshot*.png -quality 90 presentation.pdf

# Done! PDF ready in ~/Pictures/presentation.pdf
```

---

## 💡 Tips for Best Results

### For Screen Capture:
- ✅ Use fullscreen mode (F11) - removes browser UI
- ✅ Zoom to fit all content without scrolling
- ✅ Use consistent zoom level for all slides
- ✅ Capture at same time of day (consistent lighting)
- ✅ Use PNG format (lossless, better quality)

### For PDF Creation:
- ✅ Name files in order: slide-01.png, slide-02.png (not slide-1.png)
- ✅ Use consistent resolution for all images
- ✅ Set density to 150-300 DPI for print quality
- ✅ Test with one slide first to verify settings

### File Naming:
```bash
# Good naming (sorts correctly):
slide-01.png, slide-02.png, ..., slide-16.png

# Bad naming (sorts wrong):
slide-1.png, slide-10.png, slide-2.png  # 10 comes before 2!

# Rename if needed:
for i in {1..9}; do mv slide-$i.png slide-0$i.png; done
```

---

## 🆘 Troubleshooting

**Issue: Screenshots too small**
- Solution: Capture at higher resolution, or use DevTools with larger viewport

**Issue: Text blurry in PDF**
- Solution: Use higher quality setting (`-quality 95`) or higher density (`-density 300`)

**Issue: Colors look different in PDF**
- Solution: Use PNG format for screenshots (not JPEG), and convert with `-colorspace RGB`

**Issue: PDF file too large**
- Solution: Compress with ghostscript (see command above)

**Issue: Wrong slide order in PDF**
- Solution: Check file naming (use 01, 02 not 1, 2)

---

## ✅ Verification Checklist

Before finalizing PDF:

- [ ] All 16 slides captured
- [ ] Slides in correct order
- [ ] All text readable
- [ ] No content cut off at edges
- [ ] Consistent zoom/size across slides
- [ ] Colors look good
- [ ] File size reasonable (<10MB)
- [ ] Opens correctly in PDF viewer
- [ ] Suitable for 13" laptop screen

---

Good luck with the manual export! This approach gives you complete control over the final result.
