import cv2
import numpy as np

# Kernel để sử dụng trong các phép toán morphology
kernel = np.ones((5, 5), np.uint8)

# Uncomment và đặt đường dẫn đến video nếu bạn muốn xử lý video
video_path = "dataset/vd2.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print("Error: Could not open video file.")
    exit()

# Lấy thông tin của video để tạo video output
width = int(cap.get(3))
height = int(cap.get(4))
original_fps = cap.get(5)

# Giảm tốc độ fps xuống còn 10
target_fps = 10
frame_interval = int(original_fps / target_fps)

# Tạo video output
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_video.avi', fourcc, target_fps, (width, height))

# Biến đường dẫn đến hình ảnh mẫu
image_path = "test.jpg"

# Hàm không làm gì
def nothing(x):
    pass

# Tạo các cửa sổ cho việc hiển thị các thành phần của ảnh
cv2.namedWindow('HueComp')
cv2.namedWindow('SatComp')
cv2.namedWindow('ValComp')
cv2.namedWindow('closing')
cv2.namedWindow('tracking')

# Tạo trackbar để điều chỉnh ngưỡng màu sắc
cv2.createTrackbar('hmin', 'HueComp', 29, 179, nothing)
cv2.createTrackbar('hmax', 'HueComp', 69, 179, nothing)

# Tạo trackbar để điều chỉnh ngưỡng độ bão hòa màu
cv2.createTrackbar('smin', 'SatComp', 119, 255, nothing)
cv2.createTrackbar('smax', 'SatComp', 255, 255, nothing)

# Tạo trackbar để điều chỉnh ngưỡng độ giá trị màu
cv2.createTrackbar('vmin', 'ValComp', 87, 255, nothing)
cv2.createTrackbar('vmax', 'ValComp', 255, 255, nothing)

# Khởi tạo biến lưu giữ tâm trước đó
prev_center = None

frame_count = 0

while True:
    buzz = 0
    _, frame = cap.read()

    # Chuyển đổi ảnh sang không gian màu HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hue, sat, val = cv2.split(hsv)

    # Lấy giá trị ngưỡng từ trackbar
    hmn = cv2.getTrackbarPos('hmin', 'HueComp')
    hmx = cv2.getTrackbarPos('hmax', 'HueComp')
    smn = cv2.getTrackbarPos('smin', 'SatComp')
    smx = cv2.getTrackbarPos('smax', 'SatComp')
    vmn = cv2.getTrackbarPos('vmin', 'ValComp')
    vmx = cv2.getTrackbarPos('vmax', 'ValComp')

    # Tạo ảnh nhị phân dựa trên ngưỡng
    hthresh = cv2.inRange(np.array(hue), np.array(hmn), np.array(hmx))
    sthresh = cv2.inRange(np.array(sat), np.array(smn), np.array(smx))
    vthresh = cv2.inRange(np.array(val), np.array(vmn), np.array(vmx))

    # Kết hợp các ảnh nhị phân lại với nhau
    tracking = cv2.bitwise_and(hthresh, cv2.bitwise_and(sthresh, vthresh))

    # Nới rộng các vùng trắng để nối các đối tượng gần nhau
    dilation = cv2.dilate(tracking, kernel, iterations=1)

    # Đóng các lỗ nhỏ trong các vùng trắng
    closing = cv2.morphologyEx(dilation, cv2.MORPH_CLOSE, kernel)

    # Làm mờ ảnh để giảm nhiễu
    closing = cv2.GaussianBlur(closing, (15, 15), 0)

    # Vẽ các đường thẳng để chia thành các khu vực
    cv2.line(frame, (width // 3, 0), (width // 3, height), (255, 0, 0), 2)  # Đường thẳng giữa và bên trái
    cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (255, 0, 0), 2)  # Đường thẳng giữa và bên phải
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 2)  # Đường ngang chia trên và dưới

    # Phát hiện các đối tượng tròn trong ảnh đã được làm mờ
    circles = cv2.HoughCircles(closing, cv2.HOUGH_GRADIENT, 2, 120, param1=120, param2=50, minRadius=10, maxRadius=0)

    countLeft = 0
    countRight = 0
    countCenter = 0
    if circles is not None:
        for i in circles[0, :]:
            if int(round(i[2])):
                cv2.circle(frame, (int(round(i[0])), int(round(i[1]))), int(round(i[2])), (0, 255, 0), 5)
                cv2.circle(frame, (int(round(i[0])), int(round(i[1]))), 2, (0, 255, 0), 10)
                center = (int(round(i[0])), int(round(i[1])))
                # Xác định vị trí của quả bóng và thực hiện các hành động tương ứng
                if center[1] > height // 2:
                    if center[0] < width // 3:
                        countLeft += 1
                    elif center[0] > 2 * width // 3:
                        countRight += 1
                    else:
                        countCenter += 1       
    if countLeft > countRight and countLeft > countCenter:
        action = "Turn Left"
        print("Turn Left")
    elif countRight > countLeft and countRight > countCenter:
        action = "Turn Right"
        print("Turn Right")
    elif countCenter > countLeft and countCenter > countRight:
        action = "Go Ahead"
        print("Go Ahead")
    else:
        action = "Stop"
        print("Stop")

    # Vẽ đường dẫn của đối tượng nếu có
    if prev_center is not None:
        cv2.line(frame, prev_center, center, (255, 255, 255), 2)

    # Lưu tâm hiện tại cho lần lặp tiếp theo
    prev_center = center

    # Vẽ chữ và mũi tên
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame, action, (50, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    arrow_center = (100, 70)
    arrow_length = 50
    if action == "Turn Left":
        cv2.arrowedLine(frame, arrow_center, (arrow_center[0] - arrow_length, arrow_center[1]), (0, 0, 255), 2)
    elif action == "Turn Right":
        cv2.arrowedLine(frame, arrow_center, (arrow_center[0] + arrow_length, arrow_center[1]), (0, 0, 255), 2)
    elif action == "Go Ahead":
        cv2.arrowedLine(frame, arrow_center, (arrow_center[0], arrow_center[1] + arrow_length), (0, 0, 255), 2)

    out.write(frame)  # Ghi frame vào video output

    # Hiển thị các thành phần của ảnh trong các cửa sổ tương ứng
    cv2.imshow('HueComp', hthresh)
    cv2.imshow('SatComp', sthresh)
    cv2.imshow('ValComp', vthresh)
    cv2.imshow('closing', closing)
    cv2.imshow('tracking', frame)

    # Phím thoát ứng dụng
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

# Giải phóng tài nguyên khi kết thúc
cap.release()
out.release()
cv2.destroyAllWindows()
