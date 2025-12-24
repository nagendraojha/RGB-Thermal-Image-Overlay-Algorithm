# 🔥 RGB–Thermal Image Overlay & Alignment Algorithm

## 📌 Project Overview

This project implements a **robust RGB–Thermal image alignment and overlay pipeline** designed to accurately align thermal imagery with its corresponding RGB counterpart.

Since thermal and RGB images are captured using **different sensors and cameras**, they are **not naturally aligned**. A simple resize or overlay produces incorrect results.
This project solves that problem using **feature-based geometric alignment**, ensuring that the **RGB image remains unchanged** while the **thermal image is precisely transformed** to match the RGB frame.

The solution is **fully automated**, **fault-tolerant**, and capable of processing **multiple image pairs in batch mode**, making it suitable for **real-world computer vision and inspection workflows**.

---

## 🎯 Task Objective

* Align thermal images with their corresponding RGB images
* Handle misalignment caused by different camera sensors
* Process all image pairs automatically from an input directory
* Generate aligned thermal outputs while keeping RGB images unchanged
* Produce clean, reproducible outputs following a fixed folder structure

---

## 🧠 Key Challenges Addressed

* RGB and thermal cameras have **different viewpoints**
* Images are **not pixel-aligned by default**
* Feature detection on thermal images is difficult
* Some image pairs lack reliable correspondences
* Alignment must not distort or modify RGB images

This project handles all these challenges gracefully.

---

## 🗂️ Folder Structure

```
RGB-Thermal-Image-Overlay-Algorithm/
│
├── RGB Thermal Overlay Algorithm Images/
│   └── input-images/
│       ├── XXXX_T.JPG   (Thermal image)
│       ├── XXXX_Z.JPG   (RGB image)
│
├── task1output/
│   ├── XXXX_Z.JPG       (Original RGB image)
│   ├── XXXX_AT.JPG      (Aligned thermal image)
│
├── task1.py
└── README.md
```

---

## 🖼️ Sample Input (Thermal Image)

Below is an example **thermal input image** used by the algorithm:

<p align="center">
  <img src="RGB Thermal Overlay Algorithm Images/input-images/sample_thermal.JPG" width="500">
</p>

*(Thermal image captured from a different sensor and viewpoint)*

---

## 🖼️ Sample Output (Aligned Thermal Image)

After alignment, the thermal image is transformed to match the RGB frame:

<p align="center">
  <img src="task1output/sample_AT.JPG" width="500">
</p>

✔ Thermal content is geometrically aligned
✔ RGB frame remains unchanged
✔ Aspect ratio preserved
✔ No visual distortion

---

## ⚙️ How the Algorithm Works

### 1️⃣ Intelligent Image Pair Matching

* Parses filenames using a strict naming convention
* Matches thermal (`_T.JPG`) and RGB (`_Z.JPG`) images using shared identifiers
* Handles slight timestamp differences automatically

---

### 2️⃣ Feature-Based Alignment (Primary Method)

For each image pair:

* Convert images to grayscale
* Invert thermal image to improve feature detection
* Extract features using **SIFT**
* Match features using **FLANN**
* Filter matches using **Lowe’s ratio test**
* Estimate geometric transformation using **RANSAC homography**
* Validate transformation stability

If successful → thermal image is **warped into RGB space**

---

### 3️⃣ Robust Fallback Strategy

If feature matching fails due to:

* Insufficient keypoints
* Noisy thermal data
* Unstable homography

Then:

* Thermal image is **scaled proportionally**
* Centered on the RGB canvas
* Aspect ratio preserved

This guarantees **100% pipeline reliability**.

---

## 🧪 Technologies Used

* **Python**
* **OpenCV**
* **NumPy**
* **SIFT (Scale-Invariant Feature Transform)**
* **FLANN Matcher**
* **RANSAC Homography**
* **PyTorch / TorchVision** (architecture-ready for deep extensions)

---

## ✅ Why This Project Stands Out

✔ Solves a **real sensor-alignment problem**
✔ Uses **industry-standard vision techniques**
✔ Fully automated batch processing
✔ Robust to edge cases and failures
✔ Clean, modular, production-ready code
✔ Easily extensible to deep learning alignment

---

## 🚀 Potential Applications

* Drone-based thermal inspection
* Power line and infrastructure monitoring
* Surveillance and security systems
* Industrial fault detection
* Smart agriculture and environmental analysis
* Research in multi-modal computer vision

---

## 🧩 Future Enhancements

* Alpha-blended RGB–Thermal visualization
* Deep feature alignment using CNN embeddings
* Automatic alignment quality scoring
* Real-time video stream support
* Integration with GIS / drone pipelines

---

## 🏁 Final Notes

This project goes **far beyond basic image overlay** and demonstrates a **strong understanding of computer vision, geometry, and real-world sensor limitations**.

It is designed to be **readable, reproducible, and ready for real deployment**.

---

### 👤 Author

**Nagendra Kumar Ojha**


