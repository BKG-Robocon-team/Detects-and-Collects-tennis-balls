# Computer Vision Ball Tracking

## Overview

Repository này chứa một đoạn mã Python để theo dõi bóng bằng cách sử dụng các kỹ thuật thị giác máy tính. Kịch bản xử lý đầu vào video, phát hiện quả bóng màu và theo dõi chuyển động của nó trong khung. Thông tin theo dõi sau đó được sử dụng để xác định vị trí của quả bóng và thực hiện các hành động tương ứng.

 ![image](https://github.com/BKG-Robocon-team/Detects-and-Collects-tennis-balls/blob/main/gif/vd1.gif)


## Requirements

- Python 3
- OpenCV (cv2)
- NumPy

## Installation

Bạn có thể cài đặt các gói Python cần thiết bằng lệnh sau:

```bash
pip install opencv-python numpy
```
## Configuration

Thay đoạn code sau bằng code mới
```
    _, frame = cap.read()
```
bằng 
```
    _, frame = 0, cv2.imread(image_path)
```
Sau đó, điều chỉnh thanh trượt trong các cửa sổ GUI để điều chỉnh các tham số ngưỡng màu sắc. Các cửa sổ có tên là:

* HueComp
* SatComp
* ValComp
  
## Next Step

Cấu hình code vào Raspberry PI và thử nghiệm với Robot thực tế


