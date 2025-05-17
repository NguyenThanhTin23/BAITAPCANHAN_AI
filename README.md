### **Nguyễn Thành Tin - 23110340**
---------------------------------------------------------------------------------------------------------------------------------------
### **1. Mục tiêu**
• Ứng dụng các thuật toán tìm kiếm trong trí tuệ nhân tạo (AI) để giải bài toán 8-Puzzle — một bài toán kinh điển về tìm kiếm trạng thái.  
• So sánh hiệu quả giữa các thuật toán trong từng nhóm thuật toán  
• Đánh giá và phân tích ưu điểm, nhược điểm, độ phức tạp về thời gian và bộ nhớ của từng thuật toán.  
• Triển khai và minh họa trực quan quá trình giải quyết bài toán bằng thư viện đồ họa (như pygame) để dễ quan sát và phân tích.  
• Làm nền tảng cho các bài toán AI phức tạp hơn trong lĩnh vực giải đố và tự động hóa suy luận trạng thái.

----------------------------------------------------------------------------------------------------------------------------------------
### **2. Nội dung**

### **Các thành phần chính của một bài toán tìm kiếm**
### **- Không gian trạng thái (State Space)**
- Là tập hợp tất cả các cấu hình hợp lệ của bảng 3x3, gồm các số từ 0 đến 8 (0 là ô trống).  
- Mỗi trạng thái là một hoán vị của các số này.  
- Tổng số trạng thái hợp lệ: 9! = 362,880, nhưng chỉ 181,440 trạng thái là giải được (do tính chất hoán vị chẵn/lẻ).

### **- Trạng thái đầu (Initial State)**
- Là trạng thái ban đầu được cung cấp, ví dụ:  
            1 2 3  
            4 0 6  
            7 5 8  
   Trạng thái này là điểm bắt đầu cho quá trình tìm kiếm lời giải.
  
### **- Trạng thái đích (Goal State)**
- Là trạng thái mong muốn đạt được, thường là:
  1 2 3  
  4 5 6  
  7 8 0
  - Trạng thái này có thể thay đổi tùy yêu cầu bài toán, miễn sao hợp lệ.

### **- Tập hành động (Action Set)**
- Tại mỗi trạng thái, ta có thể di chuyển ô trống (0) theo 4 hướng:
    - **Lên** (Up)  
    - **Xuống** (Down)  
    - **Trái** (Left)  
    - **Phải** (Right)  
- Tổng số hành động hợp lệ phụ thuộc vào vị trí của ô trống (0).  
Ví dụ: nếu ô trống ở góc trên trái → chỉ có 2 hành động: phải, xuống.

### **- Hàm chi phí thực tế (Cost Function – g(n))**
- Là tổng số bước đã đi từ trạng thái bắt đầu đến trạng thái hiện tại.  
- Mỗi bước di chuyển được tính với chi phí bằng 1 → `g(n) = số bước đã đi`.  
- Được sử dụng trong các thuật toán như Uniform Cost Search (UCS), A*, v.v.
  
### **- Hàm chi phí ước lượng (Heuristic Function – h(n))**
- Là ước lượng số bước còn lại để đi từ trạng thái hiện tại đến trạng thái đích.  
- Trong bài toán này, `h(n)` được tính là **số ô đang sai vị trí so với trạng thái đích**, không tính ô trống (`0`).  
- Đây là một hàm heuristic đơn giản và hợp lệ (admissible) vì nó **không bao giờ đánh giá vượt quá chi phí thực tế**.  
- Dùng trong các thuật toán như Greedy Best-First Search và A* để định hướng tìm kiếm hiệu quả hơn.

### **2.1. Các thuật toán Tìm kiếm không có thông tin**
Trong lĩnh vực Trí tuệ nhân tạo, **tìm kiếm không có thông tin** (hay còn gọi là **tìm kiếm mù**) là nhóm các thuật toán giải bài toán tìm kiếm trạng thái **mà không sử dụng bất kỳ thông tin nào về khoảng cách tới mục tiêu**.
Thay vào đó, các thuật toán này dựa vào:
- Cấu trúc của **không gian trạng thái**
- Các phép biến đổi trạng thái hợp lệ để lần lượt kiểm tra các khả năng có thể xảy ra.
#### **Đặc điểm:**
- Không khai thác tri thức chuyên biệt nào của bài toán  
- Không sử dụng hàm heuristic để định hướng tìm kiếm  
- Tổng quát, dễ cài đặt  
- Có thể **kém hiệu quả** trong không gian trạng thái lớn hoặc sâu

### **Giải pháp của nhóm thuật toán này:**
- **Duyệt toàn bộ không gian trạng thái**  
  - Tìm kiếm không có thông tin duyệt tuần tự hoặc theo một chiến lược cụ thể qua tất cả các trạng thái có thể sinh ra từ trạng thái ban đầu.
  - Mỗi **nút** trong quá trình tìm kiếm đại diện cho một **trạng thái**.
  - Thuật toán sẽ **mở rộng từng nút** để sinh ra các trạng thái kế tiếp.
  - Quá trình tiếp tục cho đến khi:
    - Tìm thấy **trạng thái đích**, hoặc  
    - **Cạn kiệt** không gian tìm kiếm mà không có lời giải.
### **Hình ảnh giải thuật:**
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/BFS.gif" width="150" /><br/>
      <b>BFS</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/DFS.gif" width="150" /><br/>
      <b>DFS</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/UCS.gif" width="150" /><br/>
      <b>UCS</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/IDS.gif" width="150" /><br/>
      <b>IDS</b>
    </td>
  </tr>
</table>

### **Hình ảnh hiệu suất**
<table>
  <tr>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20171348.png" width="550" />
    </td>
    <td width="30"></td>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20171404.png" width="550" />
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20171423.png" width="550" />
    </td>
    <td width="30"></td>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20171444.png" width="550" />
    </td>
  </tr>
</table>

### **Nhận xét**
- IDS có tốc độ nhanh, tỷ lệ thành công cao, phù hợp cho bài toán 8-Puzzle.
- UCS đạt hiệu quả tốt, tỷ lệ thành công cao nhưng tiêu tốn nhiều thời gian hơn.
- DFS xử lý nhanh nhưng tỷ lệ thất bại cao và dễ mắc kẹt trong vòng lặp vô hạn.
- BFS tốn nhiều thời gian và bộ nhớ, hiệu quả thấp hơn IDS và UCS.
- Tổng thể, IDS là lựa chọn tối ưu để cân bằng giữa tốc độ và độ tin cậy trong bài toán này.



2.2. Các thuật toán Tìm kiếm có thông tin
Trong lĩnh vực Trí tuệ nhân tạo, tìm kiếm có thông tin (informed search) là nhóm các thuật toán sử dụng thông tin bổ sung (heuristic) để định hướng việc tìm kiếm trong không gian trạng thái. Thông tin này có thể đến từ tri thức chuyên biệt về bài toán, giúp thuật toán ưu tiên mở rộng các trạng thái “hứa hẹn” hơn — tức là có khả năng dẫn đến đích nhanh hơn.
Các thuật toán có thông tin có thể hiệu quả hơn đáng kể so với các phương pháp không có thông tin, vì chúng tránh việc khám phá những vùng ít có khả năng chứa lời giải.
Thuật toán tiêu biểu: Greedy Best-First Search, A* (A-star), Recursive Best-First Search (RBFS), v.v.
Giải pháp:
•	Định hướng tìm kiếm nhờ hàm heuristic
• Mỗi trạng thái được đánh giá bởi một hàm heuristic (h(n)) hoặc kết hợp chi phí thực (g(n)) và dự đoán (h(n)) như trong A*.
• Thuật toán ưu tiên mở rộng các trạng thái có giá trị heuristic thấp hơn.
• Nhờ đó, thuật toán giảm số lượng trạng thái cần duyệt và tăng tốc độ tìm kiếm.
________________________________________
2.3. Các thuật toán Tìm kiếm cục bộ
Tìm kiếm cục bộ (local search) là nhóm các thuật toán không xây dựng toàn bộ cây tìm kiếm, mà chỉ quan tâm đến một hoặc vài trạng thái tại một thời điểm. Đây là cách tiếp cận hiệu quả trong các không gian trạng thái rất lớn, nơi việc lưu trữ toàn bộ cây tìm kiếm là không khả thi.
Thuật toán cục bộ bắt đầu từ một trạng thái ban đầu và lặp lại việc di chuyển sang một trạng thái lân cận “tốt hơn”, cho đến khi không thể cải thiện nữa.
Thuật toán tiêu biểu: Hill Climbing, Simulated Annealing, Stochastic Hill Climbing, Local Beam Search, Genetic Algorithm, v.v.
Giải pháp:
•	Tối ưu dần qua trạng thái lân cận
• Khởi đầu từ một trạng thái (thường là ngẫu nhiên).
• Đánh giá các trạng thái lân cận và di chuyển tới trạng thái tốt hơn.
• Nếu không có lân cận nào tốt hơn (tối ưu cục bộ), có thể dừng lại hoặc sử dụng kỹ thuật tránh bẫy như làm lạnh mô phỏng (Simulated Annealing) hoặc đa nghiệm (Beam, Genetic).
• Phù hợp cho các bài toán tối ưu hóa hoặc không gian tìm kiếm liên tục.
2.4. Tìm kiếm trong môi trường phức tạp
Trong nhiều ứng dụng thực tế, việc tìm kiếm không diễn ra trong môi trường đơn giản, tĩnh, có đầy đủ thông tin. Thay vào đó, môi trường có thể mang tính động, không chắc chắn, một phần quan sát được, hoặc có nhiều tác nhân tương tác với nhau. Đây được gọi chung là môi trường phức tạp.
Đặc điểm:
•	Thiếu thông tin đầy đủ về trạng thái hiện tại hoặc trạng thái đích.
•	Môi trường có thể thay đổi trong quá trình tìm kiếm (dynamic environment).
•	Có thể có nhiều tác nhân (agents) cùng hành động và ảnh hưởng lẫn nhau.
•	Các hành động có thể không đảm bảo kết quả chắc chắn (non-deterministic).
•	Một số môi trường chỉ cho phép quan sát từng phần (partial observability).
Giải pháp:
•	Tìm kiếm với thông tin không đầy đủ (Partial-Observation Search)
• Đại diện cho trạng thái bằng các tập hợp có thể xảy ra (belief states).
• Tìm chiến lược thay vì chỉ một chuỗi hành động.
2.5. Tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Problem - CSP)
Thay vì mô hình hóa bài toán theo không gian trạng thái truyền thống (trạng thái – hành động), nhiều bài toán thực tế được biểu diễn dưới dạng các biến với miền giá trị và các ràng buộc logic giữa các biến. Đây là mô hình Constraint Satisfaction Problem (CSP) – một lớp bài toán quan trọng trong AI.
Thành phần của một CSP:
•	Tập biến (Variables): X={X1,X2,...,Xn}X = \{X_1, X_2, ..., X_n\}X={X1,X2,...,Xn}
•	Tập miền giá trị (Domains): Mỗi biến XiX_iXi có miền giá trị DiD_iDi.
•	Tập ràng buộc (Constraints): Xác định các tổ hợp giá trị hợp lệ giữa các biến.
Đặc điểm:
•	Không quan tâm đến thứ tự hành động hay chi phí.
•	Tập trung vào việc tìm một (hoặc tất cả) cấu hình thỏa mãn toàn bộ ràng buộc.
•	Các bài toán CSP thường có tính tổ hợp rất lớn.
Giải pháp:
•	Gán giá trị cho biến sao cho thỏa mãn tất cả ràng buộc
• Thường sử dụng thuật toán gán ràng buộc + kiểm tra nhất quán (backtracking + constraint checking).
• Cải tiến với Forward Checking, AC-3 (Arc Consistency) để loại trừ giá trị không hợp lệ sớm.
3. Kết luận
•	Nắm vững nguyên lý hoạt động và cách áp dụng các thuật toán tìm kiếm trong không gian trạng thái, giúp nâng cao khả năng giải quyết các bài toán phức tạp.
•	Giải pháp được xây dựng có khả năng tìm ra chuỗi hành động từ trạng thái ban đầu đến trạng thái đích một cách tối ưu hoặc gần tối ưu.
•	Quá trình tìm kiếm được tối ưu nhằm giảm thiểu tài nguyên tính toán và thời gian xử lý, tăng hiệu suất cho chương trình.
•	Giao diện trực quan giúp người dùng dễ dàng theo dõi từng bước giải, đồng thời hỗ trợ nhóm kiểm tra và hoàn thiện thuật toán hiệu quả hơn.
•	Nhận thức rõ các thách thức khi tìm kiếm trong môi trường có ràng buộc và thông tin không đầy đủ, từ đó hiểu tầm quan trọng của việc thiết kế giải pháp phù hợp cho từng bài toán.
•	Kết quả đạt được khẳng định tính khả thi của việc ứng dụng các thuật toán tìm kiếm trong trò chơi 8 puzzle, đồng thời mở rộng tiềm năng áp dụng vào nhiều bài toán thực tế khác trong lĩnh vực trí tuệ nhân tạo.

