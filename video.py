import cv2

# rtsp link: rtsp://210.99.70.120:1935/live/cctv002.stream
def main():
    # 영상 소스 입력
    source = input("Enter video file path: ")
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print("Error: Cannot open video")
        return

    # 영상 사이즈 입력
    width = int(input("Enter video width: "))
    height = int(input("Enter video height: "))

    # FPS 설정
    if source.startswith("rtsp"):
        fps = 30
    else:
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
    output_fps = int(fps)
    print(f"Using FPS: {output_fps}")

    info_height = 60  # 하단 정보 표시 공간 높이
    draw_rectangle = False  # 사각형 표시 여부
    rect_color = (0, 0, 255)  # 사각형 색상
    capture_cnt = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video")
            break

        # 프레임 리사이즈
        frame = cv2.resize(frame, (width, height))

        # 빈 공간 추가
        output_frame = cv2.copyMakeBorder(frame, 0, info_height, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))

        # 하단 첫 번째 줄: 영상 주소
        cv2.putText(output_frame, f"<Video Path: {source}>", (10, height + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # 하단 두 번째 줄: FPS와 size
        cv2.putText(output_frame, f"FPS: <{output_fps}>, Size: <{width}>x<{height}>", (10, height + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

        # 사각형 표시 여부
        if draw_rectangle:
            cv2.rectangle(output_frame, (50, 50), (width - 50, height - 50), rect_color, 2)

        # 프레임 출력
        cv2.imshow('Video Stream', output_frame)

        # 키 입력 처리
        key = cv2.waitKey(int(1000 / output_fps)) & 0xFF

        # print(f"Key pressed: {chr(key) if key < 128 else key}")  # 입력 키를 콘솔에 출력

        # 누르면 종료
        if key in [ord('q'), ord('Q')]:
            print("Exiting video stream")
            break

        # 누르면 캡쳐
        elif key in [ord('s'), ord('S')]:
            capture_path = "capture_frame_" + str(capture_cnt) + ".jpg"
            capture_frame = output_frame.copy()
            cv2.imwrite(capture_path, capture_frame)
            print(f"Captured frame saved to {capture_path}")
            capture_cnt += 1

        # 누르면 사각형 그리기
        elif key in [ord('w'), ord('W')]:
            draw_rectangle = not draw_rectangle
            print("rectangle")

        # 누르면 fps 1 감소
        elif key == ord('a'):
            if output_fps > 1:
                output_fps -= 1
                print(f"Decreased FPS to {output_fps}")

        # 누르면 fps 1 증가
        elif key == ord('b'): # shift나 caps lock을 통한 대문자 변환을 프로그램이 읽지 못해 b로 변경함
            output_fps += 1
            print(f"Increased FPS to {output_fps}")

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
