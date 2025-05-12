1.Mục tiêu

2.Nội dung
![Hide_and_Seek](https://github.com/user-attachments/assets/bd8bfd79-1169-4ad6-96fe-3223f61399ba)


  2.1 Các thuật toán tìm kiếm không có thông tin (Uninformed Search)

    2.1.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán BFS  (Breadth-First Search)
        _ Các thành phần chính:
          + Khởi tạo:
            . start: Vị trí bắt đầu (vị trí hiện tại của seeker)
            . queue: Hàng đợi lưu trữ các nút cần xét (sử dụng deque để tối ưu)
            . visited: Tập hợp lưu các vị trí đã thăm
          + Vòng lặp chính:
            . Lấy phần tử đầu tiên từ hàng đợi (queue.popleft())
            . Kiểm tra điều kiện đích (khoảng cách < 30 pixel)
          + Mở rộng nút:
            . Xét 4 hướng di chuyển (lên, xuống, trái, phải)
            . Mỗi bước di chuyển 30 pixel (kích thước ô)
          + Kiểm tra điều kiện:
            . Vị trí mới phải trong phạm vi map
            . Chưa được thăm (not in visited)
            . Không va chạm với vật cản (check_collision)
        _ Phân tích solution
          + Ưu điểm:
            . Luôn tìm được lời giải tối ưu (đường đi ngắn nhất)
            . Dễ triển khai và hiểu
            . Phù hợp với map kích thước vừa phải
          + Nhược điểm:
            . Tiêu tốn bộ nhớ do lưu trữ nhiều trạng thái
            . Hiệu suất giảm với map lớn do phải duyệt nhiều nút

  2.2 Các thuật toán tìm kiếm có thông tin (Informed Search)
  
    2.2.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán A*
        _ Các thành phần chính
          + Hàm heuristic:
            . Sử dụng khoảng cách Manhattan (tổng chênh lệch tọa độ x và y)
            . Ước lượng chi phí từ điểm hiện tại đến đích
          + Cấu trúc dữ liệu:
            . open_set: Hàng đợi ưu tiên (min-heap) lưu các nút cần xét, ưu tiên f_score nhỏ nhất
            . came_from: Dictionary lưu vết đường đi (nút cha của mỗi nút)
            . g_score: Dictionary lưu chi phí thực tế từ start đến mỗi nút
            . f_score: Dictionary lưu tổng chi phí ước lượng (g_score + heuristic)
          + Khởi tạo:
            . Bắt đầu từ vị trí hiện tại của seeker
            . g_score[start] = 0 (chi phí từ start đến chính nó là 0)
            . f_score[start] = heuristic(start, goal) (ước lượng ban đầu)
          + Vòng lặp chính:
            . Lấy nút có f_score nhỏ nhất từ open_set (heapq.heappop)
            . Kiểm tra điều kiện đích (khoảng cách < 30 pixel)
          + Mở rộng nút:
            . Xét 4 hướng di chuyển (lên, xuống, trái, phải)
            . Mỗi bước di chuyển 30 pixel
          + Cập nhật chi phí:
            . Tính tentative_g_score (chi phí từ start đến next_pos)
            . Nếu tìm được đường tốt hơn (chi phí thấp hơn), cập nhật các giá trị
        _ Phân tích solution
          + Ưu điểm
            . Hiệu quả hơn BFS nhờ sử dụng heuristic
            . Luôn tìm được lời giải tối ưu (với heuristic admissible)
            . Cân bằng giữa thời gian và chất lượng đường đi
          + Nhược điểm
            . Phức tạp hơn BFS trong cài đặt
            . Phụ thuộc vào chất lượng hàm heuristic
            . Tiêu tốn bộ nhớ để lưu trữ nhiều thông tin
            
  2.3 Các thuật toán tìm kiếm nội bộ
  
    2.3.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán 
    



      


        


  
