# Presentation Display Troubleshooting Guide

**Issue:** Slides displaying too low in browser and not fitting when printed  
**Status:** Multiple fixes applied - follow steps below

---

## ✅ Changes Applied (Latest: commit f561ff4)

### 1. **Slide Dimensions**
- Set to **1024×768** (standard 4:3 aspect ratio)
- Margin: **0.04** (4% - less wasted space)
- Scale limits: min **0.5**, max **1.5**

### 2. **Positioning**
- `center: false` (no vertical centering)
- Proper HTML/body 100% dimensions
- Let Reveal.js handle natural positioning

### 3. **Print Layout**
- A4 landscape: **297mm × 210mm**
- Margins: **15mm** all around
- Section padding: **20mm** for print
- One slide per page (`page-break-after: always`)

---

## 🔧 Testing Steps

### **Step 1: Hard Refresh Browser**
Old CSS might be cached.

```bash
# Close ALL browser tabs with the presentation
# Then re-open
cd /home/ruby/Projects/assigment-djehuty/presentation
xdg-open index.html
```

**In browser:**
- Press **Ctrl+Shift+R** (hard refresh, clears cache)
- Or **Ctrl+F5**
- Or **F12** → Network tab → Check "Disable cache" → Refresh

### **Step 2: Check Browser Zoom**
Browser zoom might be set too high.

- Press **Ctrl+0** (zero) to reset zoom to 100%
- Current zoom level shown in browser address bar or settings

### **Step 3: Try Fullscreen Mode**
```
Press F11
```
This removes browser chrome and gives presentation full screen.

### **Step 4: Test Print Preview**
```bash
# Open presentation
xdg-open index.html

# Then:
# Ctrl+P
# Select: Landscape
# Check: Print Preview
```

**What you should see:**
- Content should fit on one A4 landscape page
- Margins visible on all sides
- Text not cut off

---

## 🐛 If Still Not Working

### Issue A: "Slides Still Appear Too Low"

**Possible causes:**
1. Browser cache not cleared
2. Browser zoom not at 100%
3. Window too small

**Solutions:**
```bash
# 1. Force clear cache
# Firefox: Ctrl+Shift+Delete → Cached Web Content → Clear
# Chrome: Ctrl+Shift+Delete → Cached images and files → Clear

# 2. Check window size
# Presentation needs at least 1024x768 viewport
# Make browser window larger or go fullscreen (F11)

# 3. Try different browser
firefox /home/ruby/Projects/assigment-djehuty/presentation/index.html
```

### Issue B: "Print Still Doesn't Fit"

**Check print settings:**
```
1. Ctrl+P
2. Destination: Save as PDF (to test first)
3. Layout: LANDSCAPE ✅
4. Paper size: A4
5. Scale: 100% or "Fit to page"
6. Margins: Default
7. Options: Background graphics ON
```

**If content is cut off:**
- Try scale: "Fit to page width" or "Shrink to fit"
- Try custom margins: 15mm or 20mm
- Check "Headers and footers" is OFF

### Issue C: "Content Overflowing"

Some slides might have too much content for the dimensions.

**Quick fix - reduce font sizes:**
```bash
# Edit presentation/index.html
# Find the font size CSS (around line 60-70)
# Reduce:
# h1: from 2.5em to 2.2em
# h2: from 1.8em to 1.6em
```

**Or add this CSS to index.html in <style> section:**
```css
.reveal h1 { font-size: 2.2em !important; }
.reveal h2 { font-size: 1.6em !important; }
.reveal { font-size: 32px !important; }  /* was 36px default */
```

---

## 📊 Diagnostic Commands

### Check current presentation settings:
```bash
# Open browser console (F12)
# Type:
Reveal.getConfig()

# Should show:
# width: 1024
# height: 768
# margin: 0.04
# center: false
```

### Check if CSS is loaded:
```bash
# In browser console:
getComputedStyle(document.querySelector('.reveal')).width
# Should return something like "1024px" scaled to your window

getComputedStyle(document.querySelector('.reveal')).height
# Should return something like "768px" scaled to your window
```

---

## 🎯 Alternative: Use PDF Mode

If browser display is still problematic, you can use Reveal.js PDF export mode:

```bash
# Open with PDF query parameter
chromium-browser "file:///home/ruby/Projects/assigment-djehuty/presentation/index.html?print-pdf"

# Then immediately:
# Ctrl+P → Save as PDF → Landscape
```

This renders slides specifically for PDF export.

---

## 💡 Recommended Browser Settings

### Firefox
- Settings → General → Language and Appearance
- Zoom: 100%
- Default zoom: 100%

### Chrome/Chromium
- Settings → Appearance
- Page zoom: 100%
- Font size: Medium

### Monitor Resolution
Works best on:
- ✅ 1920×1080 (Full HD)
- ✅ 1366×768 (common laptop)
- ✅ 1280×1024
- ⚠️ <1024×768 (may need scaling)

---

## 🔍 Manual Dimension Adjustment

If automatic sizing doesn't work, you can manually adjust:

### Edit `/home/ruby/Projects/assigment-djehuty/presentation/index.html`

Find around line 1630:
```javascript
Reveal.initialize({
    width: 1024,    // Change this
    height: 768,    // Change this
    margin: 0.04,   // Change this
```

**Try these alternative dimensions:**

**Option 1: Smaller (fits more screens)**
```javascript
width: 960,
height: 720,
margin: 0.05,
```

**Option 2: Larger (more space)**
```javascript
width: 1280,
height: 960,
margin: 0.03,
```

**Option 3: Widescreen (16:9)**
```javascript
width: 1280,
height: 720,
margin: 0.04,
```

After changing, save and hard refresh browser (Ctrl+Shift+R).

---

## 📋 Final Checklist

Before presenting, verify:

- [ ] Browser zoom is 100% (Ctrl+0)
- [ ] Browser cache cleared (Ctrl+Shift+R)
- [ ] Window size >= 1024×768 or fullscreen (F11)
- [ ] Slide content visible without scrolling
- [ ] Navigation works (arrow keys)
- [ ] Speaker notes work (press S)
- [ ] Print preview shows one slide per A4 landscape page
- [ ] No content cut off in print preview

---

## 🆘 Last Resort: Fallback Dimensions

If nothing works, use these ultra-safe dimensions:

```javascript
// Edit index.html around line 1630
Reveal.initialize({
    width: 800,
    height: 600,
    margin: 0.1,
    minScale: 0.5,
    maxScale: 1.5,
    center: false,
    // ... rest of config
});
```

800×600 is the "safest" resolution that works on virtually all screens and printers.

---

## 📞 Debug Information to Collect

If you need further help, collect this info:

1. **Browser and version:**
   ```bash
   # Firefox
   firefox --version
   
   # Chrome
   chromium-browser --version
   ```

2. **Screen resolution:**
   ```bash
   xdpyinfo | grep dimensions
   ```

3. **Browser console errors:**
   - Press F12
   - Go to Console tab
   - Copy any red error messages

4. **Current Reveal.js config:**
   - Press F12
   - Type: `Reveal.getConfig()`
   - Copy output

---

## ✅ Expected Final Result

**In Browser:**
- Slides fill screen nicely (not too big, not too small)
- Title appears near top of viewport (not middle/bottom)
- Content readable without zooming
- Navigation smooth

**When Printing:**
- Each slide on one A4 landscape page
- 15mm margins visible all around
- All content fits (nothing cut off)
- Colors preserved
- Professional appearance

---

**Current version:** 1024×768, margin 0.04, center false, commit f561ff4
