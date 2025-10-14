import os
import urllib.request
from urllib.error import URLError, HTTPError

os.makedirs("images", exist_ok=True)

# For shapes and coins we provide multiple candidate URLs (try them in order).
images_candidates = {
    "fruits.jpg": [
        "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/fruits.jpg",
        "https://raw.githubusercontent.com/opencv/opencv/raw/4.x/samples/data/fruits.jpg",
    ],
    "smarties.png": [
        "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/smarties.png",
        "https://raw.githubusercontent.com/opencv/opencv/raw/4.x/samples/data/smarties.png",
    ],
    "sudoku.png": [
        "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/sudoku.png",
        "https://raw.githubusercontent.com/opencv/opencv/raw/4.x/samples/data/sudoku.png",
    ],
    "gradient.png": [
        "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/gradient.png",
        "https://raw.githubusercontent.com/opencv/opencv/raw/4.x/samples/data/gradient.png",
    ],
    # shapes & coins: try multiple known locations, then fall back to a generic placeholder
    "shapes.png": [
        "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/cv/morphology/shapes.png",
        "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/shapes.png",
        # fallback placeholder (simple geometric shapes image)
        "https://upload.wikimedia.org/wikipedia/commons/6/6d/Geometric_shapes.svg"
    ],
    "coins.png": [
        "https://raw.githubusercontent.com/opencv/opencv_extra/master/testdata/cv/segmentation/coins.png",
        "https://raw.githubusercontent.com/opencv/opencv/master/samples/data/coins.png",
        # fallback: public domain coin image (may be larger but usable)
        "https://upload.wikimedia.org/wikipedia/commons/3/37/Coins_2007.jpg"
    ],
}

def try_download(url, path):
    try:
        # Use urlretrieve which raises HTTPError on non-200
        urllib.request.urlretrieve(url, path)
        return True, None
    except HTTPError as he:
        return False, f"HTTP Error {he.code} for {url}"
    except URLError as ue:
        return False, f"URL Error {ue.reason} for {url}"
    except Exception as e:
        return False, f"Other error {e} for {url}"

for name, candidates in images_candidates.items():
    dest = os.path.join("images", name)
    # Skip download if file already exists locally
    if os.path.exists(dest):
        print(f"{name} already exists — skipping download.")
        continue

    downloaded = False
    last_err = None
    for url in candidates:
        print(f"Trying to download {name} from: {url}")
        ok, err = try_download(url, dest)
        if ok:
            print(f"{name} downloaded successfully from: {url}")
            downloaded = True
            break
        else:
            last_err = err
            print(f" -> failed: {err}")

    if not downloaded:
        print(f"Could not download {name}. Last error: {last_err}. File will be skipped.")

print("\nDownload script finished. Check the 'images' folder for available samples.")



