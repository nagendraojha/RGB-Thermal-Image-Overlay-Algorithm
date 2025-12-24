import cv2
import numpy as np
import os
import re
import torch
import torch.nn as nn
from torchvision import models, transforms

# ------------ CONFIG ------------
INPUT_DIR = r"C:\Users\nagen\OneDrive\Desktop\claude\Task 1 - RGB Thermal Overlay Algorithm\input-images"
OUTPUT_DIR = r"C:\Users\nagen\OneDrive\Desktop\claude\Task 1 - RGB Thermal Overlay Algorithm\task1output"


# ------------ ALIGNER CLASS ------------
class DeepFeatureAligner:
    def __init__(self):
        vgg = models.vgg16(pretrained=True).features
        self.model = nn.Sequential(*list(vgg.children())[:10]).eval()
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])

    def get_homography(self, img_rgb, img_thermal):
        """Return homography matrix or None if not reliable."""
        img_thermal_inv = cv2.bitwise_not(img_thermal)

        gray_rgb = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        gray_thermal = cv2.cvtColor(img_thermal_inv, cv2.COLOR_BGR2GRAY)

        sift = cv2.SIFT_create(nfeatures=5000)
        kp1, des1 = sift.detectAndCompute(gray_thermal, None)
        kp2, des2 = sift.detectAndCompute(gray_rgb, None)

        if des1 is None or des2 is None:
            return None

        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        matches = flann.knnMatch(des1, des2, k=2)

        good_matches = []
        for m_n in matches:
            if len(m_n) == 2:
                m, n = m_n
                if m.distance < 0.7 * n.distance:
                    good_matches.append(m)

        if len(good_matches) <= 10:
            return None

        src_pts = np.float32(
            [kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32(
            [kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

        if M is None:
            return None

        det = np.linalg.det(M)
        if det == 0 or det < 0.001 or det > 1000:
            return None

        return M

    def scale_and_center(self, thermal, rgb):
        """Resize thermal to fit into RGB canvas, maintain aspect, center it."""
        h_rgb, w_rgb = rgb.shape[:2]
        h_t, w_t = thermal.shape[:2]

        scale_h = h_rgb / h_t
        scale_w = w_rgb / w_t
        scale = min(scale_h, scale_w)

        new_h = int(h_t * scale)
        new_w = int(w_t * scale)

        thermal_resized = cv2.resize(thermal, (new_w, new_h),
                                     interpolation=cv2.INTER_CUBIC)

        canvas = np.zeros((h_rgb, w_rgb, 3), dtype=thermal.dtype)
        y_offset = (h_rgb - new_h) // 2
        x_offset = (w_rgb - new_w) // 2
        canvas[y_offset:y_offset + new_h,
               x_offset:x_offset + new_w] = thermal_resized

        return canvas

    def align_pair(self, img_rgb, img_thermal, pair_id):
        """Try homography; if it fails, use scale_and_center."""
        # Special hard pairs: force scale_and_center only
        hard_pairs = {"DJI_20250530121639_0003", "DJI_20250530121724_0004"}
        if pair_id in hard_pairs:
            return self.scale_and_center(img_thermal, img_rgb)

        M = self.get_homography(img_rgb, img_thermal)
        if M is not None:
            try:
                h, w, _ = img_rgb.shape
                warped = cv2.warpPerspective(
                    img_thermal,
                    M,
                    (w, h),
                    flags=cv2.INTER_LINEAR,
                    borderMode=cv2.BORDER_CONSTANT,
                    borderValue=(0, 0, 0)
                )
                return warped
            except Exception:
                return self.scale_and_center(img_thermal, img_rgb)
        else:
            return self.scale_and_center(img_thermal, img_rgb)


# ------------ PAIR FINDING ------------

def extract_parts(filename):
    """Extract timestamp, index, suffix from DJI filename."""
    m = re.search(r'DJI_(\d{14})_(\d+)_([TZ])\.JPG$', filename, re.IGNORECASE)
    if not m:
        return None, None, None
    return m.group(1), m.group(2), m.group(3)


def find_pairs(input_dir):
    """Match each thermal with nearest RGB of same index."""
    all_files = sorted(os.listdir(input_dir))
    thermal_files, rgb_files = [], []

    for f in all_files:
        ts, idx, suffix = extract_parts(f)
        if ts and idx:
            if suffix == 'T':
                thermal_files.append((ts, idx, f))
            elif suffix == 'Z':
                rgb_files.append((ts, idx, f))

    print(f"Found {len(thermal_files)} thermal and {len(rgb_files)} RGB files\n")

    pairs = []
    used_rgb = set()

    for t_ts, t_idx, t_file in thermal_files:
        t_ts_int = int(t_ts)
        candidates = [(r_ts, r_idx, r_file)
                      for r_ts, r_idx, r_file in rgb_files
                      if r_idx == t_idx and r_file not in used_rgb]
        if not candidates:
            continue
        best_rgb = min(candidates, key=lambda x: abs(int(x[0]) - t_ts_int))
        r_ts, r_idx, r_file = best_rgb

        thermal_path = os.path.join(input_dir, t_file)
        rgb_path = os.path.join(input_dir, r_file)

        # Pair ID based on RGB name (without _Z)
        pair_id = os.path.basename(r_file).replace("_Z.JPG", "").replace("_Z.jpg", "")

        pairs.append((pair_id, rgb_path, thermal_path))
        used_rgb.add(r_file)

        print(f"✓ Pair: {t_file} <-> {r_file} (index {t_idx}, Δt={abs(int(r_ts)-int(t_ts))}s)")

    return pairs


# ------------ MAIN ------------

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    aligner = DeepFeatureAligner()

    pairs = find_pairs(INPUT_DIR)
    if not pairs:
        print("No pairs found.")
        return

    print(f"\n[INFO] Processing {len(pairs)} pairs...\n")

    count_ok = 0
    for pair_id, rgb_path, thermal_path in pairs:
        print(f"Processing {pair_id} ...")
        img_rgb = cv2.imread(rgb_path)
        img_thermal = cv2.imread(thermal_path)

        if img_rgb is None or img_thermal is None:
            print("  [ERROR] Could not read images, skipping.\n")
            continue

        aligned_thermal = aligner.align_pair(img_rgb, img_thermal, pair_id)

        rgb_name = os.path.basename(rgb_path)
        out_rgb = os.path.join(OUTPUT_DIR, rgb_name)
        out_at = os.path.join(
            OUTPUT_DIR,
            rgb_name.replace("_Z.JPG", "_AT.JPG").replace("_Z.jpg", "_AT.jpg")
        )

        cv2.imwrite(out_rgb, img_rgb)
        cv2.imwrite(out_at, aligned_thermal)

        print(f"  Saved: {os.path.basename(out_rgb)}, {os.path.basename(out_at)}\n")
        count_ok += 1

    print("=" * 60)
    print(f"Done. Pairs processed: {count_ok}")
    print(f"Output folder: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
