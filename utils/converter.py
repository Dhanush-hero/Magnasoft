import json

def convert_annotations(conversion_type, annotation_text, width, height):
    if conversion_type == "GeoJSON → COCO":
        geojson = json.loads(annotation_text)
        coco = {
            "images": [],
            "annotations": [],
            "categories": [{"id": 1, "name": "object"}]
        }
        image_id = 1
        ann_id = 1
        coco["images"].append({
            "id": image_id,
            "width": width,
            "height": height,
            "file_name": "uploaded_image.jpg"
        })
        for feature in geojson["features"]:
            coords = feature["geometry"]["coordinates"][0]
            x = coords[0][0]
            y = coords[0][1]
            w = abs(coords[2][0] - coords[0][0])
            h = abs(coords[2][1] - coords[0][1])
            coco["annotations"].append({
                "id": ann_id,
                "image_id": image_id,
                "category_id": 1,
                "bbox": [x, y, w, h],
                "area": w * h,
                "iscrowd": 0
            })
            ann_id += 1
        boxes = [[x, y, w, h] for ann in coco["annotations"] for x, y, w, h in [ann["bbox"]]]
        return coco, boxes, "json"

    elif conversion_type == "COCO → YOLO":
        coco = json.loads(annotation_text)
        yolo_lines = []
        boxes = []
        for ann in coco["annotations"]:
            x, y, w, h = ann["bbox"]
            cx = (x + w / 2) / width
            cy = (y + h / 2) / height
            nw = w / width
            nh = h / height
            boxes.append([x, y, w, h])
            yolo_lines.append(f"0 {cx:.6f} {cy:.6f} {nw:.6f} {nh:.6f}")
        return "\n".join(yolo_lines), boxes, "txt"

    elif conversion_type == "YOLO → COCO":
        lines = annotation_text.strip().split("\n")
        coco = {
            "images": [{
                "id": 1,
                "width": width,
                "height": height,
                "file_name": "uploaded_image.jpg"
            }],
            "annotations": [],
            "categories": [{"id": 0, "name": "object"}]
        }
        boxes = []
        for i, line in enumerate(lines, start=1):
            parts = list(map(float, line.strip().split()))
            cx, cy, nw, nh = parts[1], parts[2], parts[3], parts[4]
            w = nw * width
            h = nh * height
            x = (cx * width) - w / 2
            y = (cy * height) - h / 2
            boxes.append([x, y, w, h])
            coco["annotations"].append({
                "id": i,
                "image_id": 1,
                "category_id": 0,
                "bbox": [x, y, w, h],
                "area": w * h,
                "iscrowd": 0
            })
        return coco, boxes, "json"

    else:
        raise ValueError("Unsupported conversion type")
