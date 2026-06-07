# Jigmo CJK Mega Dataset Generator

## Overview

**Jigmo CJK Mega Dataset Generator** is a high-performance synthetic dataset creation framework designed to generate massive character recognition datasets covering the complete set of modern and historical Chinese, Japanese, and Korean (CJK) ideographs.

The generator automatically discovers supported glyphs from the Jigmo font family and creates train/test datasets with realistic visual variations suitable for OCR, handwriting recognition research, character classification, multilingual AI systems, and large-scale computer vision experiments.

The system is capable of processing more than **100,000 Unicode character targets** across all currently defined CJK Unified Ideograph blocks while utilizing multi-core CPU parallelism for maximum throughput.

---

# Features

### Complete CJK Coverage

Supports all currently assigned CJK Unified Ideograph blocks including:

* CJK Unified Ideographs
* CJK Unified Ideographs Extension A
* Extension B
* Extension C
* Extension D
* Extension E
* Extension F
* Extension G
* Extension H
* Extension I
* Extension J

Total Unicode coverage exceeds **100,000 potential character classes**.

---

### Synthetic Data Augmentation Pipeline

Every generated image undergoes randomized transformations to improve model generalization.

Implemented variance types:

| Variance Type       | Description                       |
| ------------------- | --------------------------------- |
| Font Size Variation | Multiple rendering scales         |
| Rotation            | Random angular distortion         |
| Translation         | Random positional jitter          |
| Stroke Weight       | Simulated bold and thin rendering |
| Blur                | Gaussian blur simulation          |

These transformations help create robust datasets suitable for deep learning models.

---

### Intelligent Glyph Detection

Before generating a class, the system verifies whether the target glyph exists within the available Jigmo font collection.

Unsupported Unicode characters are automatically skipped.

This prevents creation of empty or invalid classes.

---

### Multi-Font Rendering

The generator can operate using multiple Jigmo font slices simultaneously.

Supported font files:

* Jigmo.ttf
* Jigmo2.ttf
* Jigmo3.ttf

The rendering engine automatically selects the first font capable of displaying the requested character.

---

### Parallel Processing Engine

The dataset generation pipeline utilizes process-based parallel execution.

Benefits include:

* Full CPU utilization
* Reduced generation time
* Efficient scaling on multi-core systems
* Balanced workload distribution

---

### Automatic Dataset Splitting

Generated samples are organized into:

```text
dataset/
├── train/
└── test/
```

Each character class receives:

* Training images
* Testing images

This structure is immediately compatible with popular deep learning frameworks.

---

# Dataset Structure

Generated folders follow Unicode codepoint naming conventions.

Example:

```text
train/
└── U_04E00/
    ├── train_0.png
    ├── train_1.png
    ├── ...
```

```text
test/
└── U_04E00/
    ├── test_0.png
    ├── test_1.png
    ├── ...
```

Where:

* `U_04E00` corresponds to Unicode codepoint U+4E00.
* Each folder represents a single character class.

---

# Image Specifications

| Property      | Value     |
| ------------- | --------- |
| Image Size    | 64 × 64   |
| Color Mode    | Grayscale |
| Background    | White     |
| Foreground    | Black     |
| Output Format | PNG       |

---

# Augmentation Strategy

## Font Size Variation

Characters are rendered at multiple scales to simulate differing writing and printing conditions.

---

## Stroke Weight Variation

Morphological operations are applied to create:

* Bold variants
* Thin variants
* Standard variants

This approximates real-world font diversity.

---

## Rotation

Characters are randomly rotated to improve robustness against scanning misalignment and imperfect document positioning.

---

## Translation

Random horizontal and vertical offsets simulate imperfect centering.

---

## Blur

Occasional Gaussian blur simulates:

* Low-quality scans
* Motion artifacts
* Optical degradation

---

# Expected Scale

For a fully supported Unicode range:

| Metric            | Approximate Value |
| ----------------- | ----------------- |
| Character Classes | 100,000+          |
| Images per Class  | 20                |
| Total Images      | 2,000,000+        |

Actual totals depend on glyph availability within the installed Jigmo font collection.

---

# Research Applications

This dataset generator is suitable for:

* Optical Character Recognition (OCR)
* Character Classification
* Historical Text Digitization
* East Asian Language Processing
* Vision Transformers
* CNN-Based Character Recognition
* Few-Shot Character Learning
* Large Vocabulary Recognition
* Synthetic Dataset Research
* Multilingual AI Systems

---

# Performance Design

Several optimizations are implemented:

### Font Caching

Fonts are cached in memory to minimize repeated disk access.

### Parallel Workers

Independent character classes are processed concurrently.

### Large-Canvas Rendering

Characters are initially rendered on oversized canvases to prevent clipping during augmentation.

### Chunked Scheduling

Task batching reduces inter-process communication overhead.

---

# Output Summary

Upon completion the generator reports:

* Number of valid character classes
* Number of generated images
* Dataset location

Example output:

```text
Finished!

Dataset ready.

Total Character Classes: XXXXX

Total Images Generated: XXXXXXX
```

---

# Requirements

The project relies on:

* Python 3.x
* Pillow (PIL)
* Concurrent Futures
* Jigmo Font Collection

---

# Intended Use

This project is designed for researchers, students, OCR engineers, computer vision practitioners, and language technology developers who require extremely large-scale synthetic datasets for CJK character recognition.

---

# License

Please verify the licensing terms of the Jigmo font family before redistributing generated datasets.

The generated dataset may inherit restrictions depending on the source fonts used during rendering.

---

# Acknowledgements

* Unicode Consortium for the CJK standard
* Jigmo font developers
* Open-source Python ecosystem
* Computer Vision and OCR research community

---

## Project Goal

To provide a scalable, reproducible, and massively parallel framework for generating synthetic datasets covering the entire spectrum of Unicode CJK ideographs for next-generation OCR and multilingual AI research.
