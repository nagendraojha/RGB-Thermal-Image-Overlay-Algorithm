\# 🔥 Task 1: RGB–Thermal Image Overlay \& Alignment System



\## 📌 Objective



The goal of this task is to \*\*accurately align thermal images with their corresponding RGB images\*\* and generate \*\*spatially consistent overlaid outputs\*\*, despite the images being captured from \*\*two different cameras\*\* with \*\*inherent misalignment\*\*.



Unlike simple image overlays, this project focuses on \*\*robust geometric alignment\*\*, ensuring that the \*\*RGB image remains unchanged\*\* while the \*\*thermal image is intelligently transformed\*\* to match the RGB frame.



---



\## 🧠 Key Challenges Addressed



\* Thermal and RGB images are captured using \*\*different sensors\*\*

\* Images are \*\*not pixel-aligned by default\*\*

\* Standard resizing is insufficient for accurate alignment

\* Some image pairs lack enough reliable feature points

\* Need a \*\*fallback strategy\*\* when feature-based alignment fails

\* Must process \*\*multiple image pairs automatically\*\*



---



\## 🚀 Solution Overview



This project implements a \*\*hybrid alignment pipeline\*\* combining:



\* \*\*Classical computer vision (SIFT + RANSAC)\*\*

\* \*\*Geometric homography estimation\*\*

\* \*\*Robust fallback scaling and centering\*\*

\* \*\*Automated batch processing\*\*

\* \*\*Strict filename-based pair matching\*\*



The result is an \*\*industry-grade RGB–Thermal alignment system\*\* that works reliably across diverse real-world image conditions.



---



\## 🗂️ Input Image Format



Each image pair follows this strict naming convention:



\* `XXXX\_T.JPG` → Thermal image

\* `XXXX\_Z.JPG` → RGB image



Where:



\* `XXXX` is a \*\*shared identifier\*\*

\* Images may differ slightly in timestamp but share the same index



Example:



```

DJI\_20250530121639\_0003\_T.JPG

DJI\_20250530121641\_0003\_Z.JPG

```



---



\## 🏗️ Project Workflow



\### 1️⃣ Intelligent Pair Detection



\* Parses filenames using regex

\* Matches thermal images with the \*\*closest RGB timestamp\*\*

\* Ensures \*\*one-to-one pairing\*\*

\* Logs pairing details (index, timestamp difference)



---



\### 2️⃣ Feature-Based Alignment (Primary Method)



For each RGB–Thermal pair:



\* Convert images to grayscale

\* Invert thermal image for better feature detection

\* Extract features using \*\*SIFT\*\*

\* Match features using \*\*FLANN matcher\*\*

\* Filter matches using \*\*Lowe’s ratio test\*\*

\* Estimate transformation using \*\*RANSAC-based homography\*\*

\* Validate transformation using determinant checks



If valid → \*\*Warp thermal image to RGB space\*\*



✔ RGB image remains \*\*completely unchanged\*\*



---



\### 3️⃣ Robust Fallback Strategy (Safety Net)



If:



\* Not enough keypoints are found

\* Homography estimation fails

\* Transformation is unstable



Then:



\* Thermal image is \*\*scaled proportionally\*\*

\* Centered on the RGB canvas

\* Aspect ratio preserved

\* Prevents failure or distorted output



This guarantees \*\*100% pipeline stability\*\*



---



\### 4️⃣ Special Handling for Hard Image Pairs



Some real-world image pairs are too noisy or lack features.



For these:



\* The system \*\*automatically forces fallback alignment\*\*

\* Ensures consistent output quality without manual intervention



---



\### 5️⃣ Output Generation



For each image pair, the system generates:



| File          | Description                    |

| ------------- | ------------------------------ |

| `XXXX\_Z.JPG`  | Original RGB image (unchanged) |

| `XXXX\_AT.JPG` | Aligned thermal image          |



All outputs are saved in a structured output directory.



---



\## 📁 Folder Structure



```

Task-1-RGB-Thermal-Overlay/

│

├── input-images/

│   ├── XXXX\_T.JPG

│   ├── XXXX\_Z.JPG

│

├── task1output/

│   ├── XXXX\_Z.JPG

│   ├── XXXX\_AT.JPG

│

├── sample-output/

│

├── task1.py

└── README.md

```



---



\## 🧪 Technologies Used



\* \*\*Python\*\*

\* \*\*OpenCV\*\*

\* \*\*NumPy\*\*

\* \*\*SIFT (Scale-Invariant Feature Transform)\*\*

\* \*\*FLANN Matcher\*\*

\* \*\*RANSAC Homography\*\*

\* \*\*PyTorch \& TorchVision\*\* (architecture-ready for deep extensions)



---



\## 📈 Why This Solution Is Industry-Grade



✔ Handles real-world camera misalignment

✔ Robust against missing or weak features

✔ Automated batch processing

✔ Zero manual tuning required

✔ Clean modular architecture

✔ Easily extendable to deep feature matching

✔ Production-ready logging and validation



---



\## 🧩 Possible Extensions



\* Alpha-blended RGB-Thermal visualization

\* Deep feature alignment using CNN embeddings

\* Automatic quality scoring of alignment

\* Real-time video stream alignment

\* GIS / drone-based thermal analytics integration



---



\## ✅ Final Outcome



This project delivers a \*\*fully automated, fault-tolerant RGB–Thermal alignment system\*\* that goes far beyond basic overlay techniques, making it suitable for \*\*computer vision pipelines, drone analytics, surveillance, thermal inspection, and research applications\*\*.





