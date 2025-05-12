1.Mục tiêu

2.Nội dung  

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
            
2.3 Thuật toán tìm kiếm nội bộ
  
    2.3.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán Simple hill climbing
        _ Các thành phần chính
          + Hàm Đánh Giá (Heuristic - get_score
            . Khoảng cách Euclidean: √((x2 - x1)² + (y2 - y1)²).
            . Dấu - để đảm bảo vị trí càng gần goal thì điểm càng cao (vì thuật toán tìm max)
          + Hàm Kiểm Tra Đích (is_goal)
            . Mục đích: Kiểm tra xem seeker đã đến đủ gần hider chưa (khoảng cách < 30 pixel).
            . Lý do: Tránh việc phải kiểm tra trùng khớp chính xác vị trí, giúp thuật toán linh hoạt hơn.
          + Danh Sách Láng Giềng (neighbors)
            . Kiểm tra ranh giới map (0 ≤ x ≤ 1230, 180 ≤ y ≤ 640).
            . Kiểm tra va chạm với vật cản (check_collision).
          +  Lựa Chọn Hướng Đi Tốt Nhất (best_neighbor)
            . Chọn vị trí tốt nhất trong các láng giềng (điểm get_score cao nhất).
            . Nếu không cải thiện được vị trí hiện tại → dừng thuật toán (đạt cực đại địa phương).
            . Nếu có cải thiện → di chuyển đến vị trí mới và lặp lại.
          +  Giới Hạn Số Lần Lặp (max_attempts=100)
            . Mục đích: Tránh vòng lặp vô hạn nếu không tìm thấy đường đi.
            . Giá trị mặc định: 100 lần thử.
        _ Phân tích solution
          + Ưu điểm
            . Đơn giản, dễ cài đặt (không cần hàng đợi phức tạp như BFS/A*).
            . Tốn ít bộ nhớ (chỉ lưu đường đi hiện tại, không lưu toàn bộ không gian trạng thái).
            . Nhanh trong môi trường đơn giản (nếu không có nhiều vật cản).
          + Nhược điểm
            . Dễ mắc kẹt ở cực đại địa phương (nếu bị bao quanh bởi vật cản
            . Không đảm bảo tìm được đường đi tối ưu (không như BFS/A*).
            . Phụ thuộc vào hàm heuristic – nếu không tốt, thuật toán có thể đi lệch hướng.
            
2.4 Thuật toán tìm kiếm trong môi trường phức tạp

    2.4.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán Partial observation
        _ Các thành phần chính
          + Tầm Nhìn (Vision Radius)
            . Mục đích: Xác định phạm vi mà seeker có thể nhìn thấy hider.
            . Giải thích: Nếu hider nằm trong vòng bán kính 150px, seeker sẽ biết chính xác vị trí và dùng A* để đuổi bắt.
          + Bộ Nhớ Vị Trí (last_known_pos và belief_map)
            . last_known_pos: Lưu vị trí cuối cùng hider được nhìn thấy.
            . belief_map: Bản đồ niềm tin (belief map) lưu xác suất hider xuất hiện ở các vị trí.
            . Xác suất giảm dần theo thời gian (0.9 là hệ số decay).
            . Nếu hider được phát hiện lại, vị trí đó được ưu tiên (+0.5).
        _ Phân tích solution
          + Ưu điểm
            . Mô phỏng thực tế: Seeker chỉ hành động dựa trên thông tin hạn chế, giống game stealth
            . Khám phá thông minh khi không thấy hider (ưu tiên trung tâm và xa tườn
            . Fallback an toàn (di chuyển ngẫu nhiên nếu bị kẹt).
            . Tiết kiệm tài nguyên: Không duyệt toàn bộ map như BFS/A*.
          + Nhược Điểm
            . Phụ thuộc vào heuristic
            . Nếu belief_map không chính xác, seeker có thể đi sai hướng.
            . Chiến lược khám phá có thể không hiệu quả ở map phức tạp.
            . Không đảm bảo tìm thấy hider nếu hider trốn ở góc khuất

  2.5 Thuật toán tìm kiếm Constraint Satisfaction Problems (CSPs)


    2.5.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán Partial Observation
        _ Các thành phần chính 
          + Tầm Nhìn (Vision Radius)
            . Mục đích: Xác định phạm vi mà seeker có thể nhìn thấy hider.
            . Giải thích: Nếu hider nằm trong vòng bán kính 150px, seeker sẽ biết chính xác vị trí và dùng A* để đuổi bắt.
          + Bộ Nhớ Vị Trí (last_known_pos và belief_map)
            . last_known_pos: Lưu vị trí cuối cùng hider được nhìn thấy.
            . belief_map: Bản đồ niềm tin (belief map) lưu xác suất hider xuất hiện ở các vị trí
          + Cập nhật niềm tin:
            . Xác suất giảm dần theo thời gian (0.9 là hệ số decay).
            . Nếu hider được phát hiện lại, vị trí đó được ưu tiên (+0.5).
          + Chiến Lược Khi Không Thấy Hider
            . Hành động: Dùng A* để di chuyển đến vị trí có xác suất cao nhất trong belief_map
            . Nếu chưa bao giờ thấy hider thì ưu tiên di chuyển đến vùng chưa khám phá, hàm đánh giá (score) cho mỗi hướng
            . Fallback: Di chuyển ngẫu nhiên
              Nếu không có hướng nào khả thi (bị bao vây bởi vật cản), chọn ngẫu nhiên
        _ Phân tích solution
          + Ưu điểm
            . Mô phỏng thực tế: Seeker chỉ hành động dựa trên thông tin hạn chế, giống game stealth
            . A* khi biết vị trí hider.
            . Khám phá thông minh khi không thấy hider (ưu tiên trung tâm và xa tường).
            . Fallback an toàn (di chuyển ngẫu nhiên nếu bị kẹt).
            . Tiết kiệm tài nguyên: Không duyệt toàn bộ map như BFS/A*.
          + Nhược điểm
            . Nếu belief_map không chính xác, seeker có thể đi sai hướng.
            . Chiến lược khám phá có thể không hiệu quả ở map phức tạp.
            . Không đảm bảo tìm thấy hider nếu hider trốn ở góc khuất
            
2.6 Thuật toán tìm kiếm Reinforcement Learning

     2.5.1 Các thành phần chính của bài toán tìm kiếm và solution
      * Thuật toán Q-learning
        _ Các thành phần chính
          + Q-Table
            . Mục đích: Lưu trữ giá trị Q (chất lượng) của từng cặp (trạng thái, hành động)
            . Key: (state, action) - state là vị trí làm tròn của seeker và hider.
            . Value: Giá trị Q ước lượng.
          + Tham số học
            . self.learning_rate = 0.1    # Tốc độ học (alpha)
            . self.discount_factor = 0.9  # Hệ số chiết khấu (gamma)
            . self.exploration_rate = 0.3 # Xác suất khám phá ngẫu nhiên (epsilon)
          + Các phương thức chính
            . Hàm get_state(). Mục đích: Chuẩn hóa trạng thái thành các ô 30x30 để giảm không gian trạng thái.
            . Hàm get_possible_actions(). Mục đích: Liệt kê các hành động hợp lệ (không va chạm, trong biên).
            . Hàm choose_action()
                30% khám phá ngẫu nhiên.
                70% chọn hành động có Q-value cao nhất.
            . Hàm update_q_table()
                Công thức Q-learning: Q(s,a) = Q(s,a) + α * [r + γ * max(Q(s',a')) - Q(s,a)]
            . Hàm get_reward()
                Cộng 100 nếu tìm thấy hider.
                Phạt tỉ lệ với khoảng cách (-distance/100).
        _ Phân tích solution
          + Ưu điểm
            . Học từ kinh nghiệm: Cải thiện hiệu suất theo thời gian.
            . Thích nghi với môi trường động: Nếu hider di chuyển, Q-table tự điều chỉnh
            . Cân bằng khám phá/khai thác: Tránh mắc kẹt ở giải pháp tối ưu cục bộ.
          + Nhược điểm
            . Tốn thời gian huấn luyện ban đầu.
            . Hiệu suất phụ thuộc vào thiết kế phần thưởng.
            . Không đảm bảo tối ưu như A*.n

  3. Hình ảnh gif so sánh các nhóm thuật toán
  ![Hide_and_Seek](https://github.com/user-attachments/assets/bd8bfd79-1169-4ad6-96fe-3223f61399ba)

      
    



      


        


  
