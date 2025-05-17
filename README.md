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
#### **Đặc điểm**
- Không khai thác tri thức chuyên biệt nào của bài toán  
- Không sử dụng hàm heuristic để định hướng tìm kiếm  
- Tổng quát, dễ cài đặt  
- Có thể **kém hiệu quả** trong không gian trạng thái lớn hoặc sâu

### **Giải pháp**
- **Duyệt toàn bộ không gian trạng thái**  
  - Tìm kiếm không có thông tin duyệt tuần tự hoặc theo một chiến lược cụ thể qua tất cả các trạng thái có thể sinh ra từ trạng thái ban đầu.
  - Mỗi **nút** trong quá trình tìm kiếm đại diện cho một **trạng thái**.
  - Thuật toán sẽ **mở rộng từng nút** để sinh ra các trạng thái kế tiếp.
  - Quá trình tiếp tục cho đến khi:
    - Tìm thấy **trạng thái đích**, hoặc  
    - **Cạn kiệt** không gian tìm kiếm mà không có lời giải.

### **Hình ảnh giải thuật**
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

----------------------------------------------------------------------------------------------------------------------------------------

### **2.2. Tìm kiếm có thông tin (Informed Search)**

Trong lĩnh vực **Trí tuệ nhân tạo**, **tìm kiếm có thông tin** (*informed search*) là nhóm các thuật toán sử dụng **thông tin bổ sung (heuristic)** để định hướng việc tìm kiếm trong không gian trạng thái. Thông tin này có thể đến từ **tri thức chuyên biệt về bài toán**, giúp thuật toán ưu tiên mở rộng các trạng thái **“hứa hẹn” hơn** — tức là có khả năng dẫn đến đích nhanh hơn.

### **Đặc điểm**
- Sử dụng **thông tin heuristic** để định hướng quá trình tìm kiếm.
- Tránh duyệt qua các vùng không hứa hẹn, **tăng hiệu quả tìm kiếm**.
- Tốc độ tìm kiếm **nhanh hơn đáng kể** so với các thuật toán không có thông tin.
- Có khả năng tìm được lời giải **tốt hơn** nếu heuristic **chính xác**.

### **Giải pháp**
- Sử dụng **hàm heuristic `h(n)`** để đánh giá độ “hứa hẹn” của mỗi trạng thái.
- Trong **A\***, kết hợp cả **chi phí đã đi qua `g(n)`** và **chi phí ước lượng còn lại `h(n)`**.
- Trạng thái có giá trị **`f(n)` hoặc `h(n)` thấp hơn** sẽ được **ưu tiên mở rộng trước**.
- Mục tiêu là **giảm số lượng trạng thái cần duyệt** và **rút ngắn thời gian tìm kiếm**.

### **Hình ảnh giải thuật**
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Greedy.gif" width="150" /><br/>
      <b>Greedy</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/A.gif" width="150" /><br/>
      <b>A*</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/IDA.gif" width="150" /><br/>
      <b>IDA*</b>
    </td>
  </tr>
</table>

### **Hình ảnh hiệu suất**
<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20172043.png" width="550"/>
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20172056.png" width="550"/>
</p>

<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20172114.png" width="550"/>
</p>

### **Nhận xét**
- **Greedy Best-First Search**: Dù chỉ mất khoảng **0.01 giây**, nhưng trung bình cần tới **60 bước**, cho thấy thuật toán **chỉ tập trung vào bước đi gần nhất**. Điều này có thể dẫn tới **lời giải không tối ưu** hoặc **dài hơn** về tổng thể. Phù hợp khi **tốc độ** là ưu tiên hàng đầu, tuy nhiên có khả năng **lời giải không ngắn** và có thể **đi đường vòng**.
- **A\*** và **IDA\***: Tốn **ít thời gian hơn** và có **số bước trung bình thấp** (khoảng **23 bước**), phản ánh khả năng **tìm lời giải nhanh và tối ưu hơn** của hai thuật toán này. Cho kết quả **tốt hơn** về cả **thời gian thực hiện** và **độ dài đường đi**, là lựa chọn **cân bằng giữa tốc độ và tối ưu hóa**.

----------------------------------------------------------------------------------------------------------------------------------------

### **2.3. Các thuật toán Tìm kiếm cục bộ**
**Tìm kiếm cục bộ (Local Search)** là nhóm các thuật toán **không xây dựng toàn bộ cây tìm kiếm**, mà chỉ quan tâm đến **một hoặc vài trạng thái tại một thời điểm**. Cách tiếp cận này rất hiệu quả trong **không gian trạng thái lớn**, nơi việc lưu trữ toàn bộ cây tìm kiếm là không khả thi.

### **Đặc điểm**
- Bắt đầu từ **một trạng thái ban đầu**.
- Lặp lại việc **di chuyển sang trạng thái lân cận tốt hơn**.
- Kết thúc khi **không thể cải thiện thêm** (rơi vào tối ưu cục bộ).

### **Giải pháp **
- **Tối ưu dần thông qua trạng thái lân cận**:
  - Khởi đầu từ một **trạng thái ngẫu nhiên**.
  - Đánh giá và chọn **trạng thái lân cận tốt hơn** để di chuyển.
  - Nếu **không có lân cận nào tốt hơn** (rơi vào bẫy tối ưu cục bộ), có thể:
    - **Dừng lại**, hoặc
    - Sử dụng các kỹ thuật tránh bẫy như:
      - **Simulated Annealing (làm lạnh mô phỏng)**
      - **Beam Search** (tìm kiếm theo chùm)
      - **Genetic Algorithm** (thuật toán di truyền)

### **Hình ảnh giải thuật**
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Leodoi.gif" width="130" /><br/>
      <b>SHC</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Leodoi.gif" width="130" /><br/>
      <b>S_AHC</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Leodoi.gif" width="130" /><br/>
      <b>Stochastic</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/SA.gif" width="130" /><br/>
      <b>SA </b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Leodoi.gif" width="130" /><br/>
      <b>Beam Search</b>
    </td>
     <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Genetic.gif" width="130" /><br/>
      <b>Genetic</b>
    </td>
  </tr>
</table>

### **Hình ảnh hiệu suất**
<table>
  <tr>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20172946.png" width="550" />
    </td>
    <td width="30"></td>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20173011.png" width="550" />
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20173026.png" width="550" />
    </td>
    <td width="30"></td>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20173037.png" width="550" />
    </td>
  </tr>
  <tr>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20173052.png" width="550" />
    </td>
    <td width="30"></td>
    <td align="center" style="padding: 20px;">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20173109.png" width="550" />
    </td>
  </tr>
</table>

### **Nhận xét**
- **Beam Search**, **SA** nổi bật nhất về hiệu quả với **tỷ lệ thành công cao (66.7%)**, trong khi vẫn xử lý rất nhanh.
- Các thuật toán **GA**, **SHC**, **S_AHC**, **Stochastic** đều có **thời gian xử lý cực nhanh**, trung bình **chưa đến 0.01 giây**.Tuy nhiên, **tỷ lệ thành công của các thuật toán này chỉ dao động từ 40% đến 50%**, do đó phù hợp với các bài toán **ưu tiên tốc độ hơn tối ưu tuyệt đối**.
- Riêng nhóm **Hill Climbing** có tỷ lệ thành công **thấp hơn** so với các thuật toán khác, nhưng vẫn giữ được ưu điểm về **tốc độ**.
  
-----------------------------------------------------------------------------------------------------------------------------------------------------------

### **2.4. Tìm kiếm trong môi trường phức tạp**
### **Đặc điểm**
- Thiếu thông tin đầy đủ về trạng thái hiện tại hoặc trạng thái đích.
- Môi trường có thể thay đổi trong quá trình tìm kiếm (dynamic environment).
- Có thể có nhiều tác nhân (agents) cùng hành động và ảnh hưởng lẫn nhau.
- Các hành động có thể không đảm bảo kết quả chắc chắn (non-deterministic).
- Một số môi trường chỉ cho phép quan sát từng phần (partial observability).

### **Giải pháp**
- Tìm kiếm với thông tin không đầy đủ (Partial-Observation Search)
- Đại diện cho trạng thái bằng các tập hợp có thể xảy ra (belief states).
- Tìm chiến lược thay vì chỉ một chuỗi hành động.
- Cần khả năng thích ứng trong quá trình tìm kiếm và tương tác.

### **Hình ảnh giải thuật**
<table>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/cb3114b090e81c8f2dbde3b28aafafbb05b70444/sensor.gif" width="150" /><br/>
      <b>Sensorless</b>
    </td>
</table>

### **Thuật toán AND-OR Search và Partial không có đường đi**
### **Hình ảnh hiệu suất**
<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20174110.png" width="550"/>
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20174057.png" width="550"/>
</p>

<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20174124.png" width="550"/>
</p>

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### **2.5. Tìm kiếm trong môi trường có ràng buộc (Constraint Satisfaction Problem - CSP)**
### **Đặc điểm***
- Không quan tâm đến thứ tự hành động hay chi phí.
- Tập trung vào việc tìm một (hoặc tất cả) cấu hình thỏa mãn toàn bộ ràng buộc.
- Các bài toán CSP thường có tính tổ hợp rất lớn.

### **Giải pháp**
- Gán giá trị cho biến sao cho thỏa mãn tất cả ràng buộc
- Thường sử dụng thuật toán gán ràng buộc + kiểm tra nhất quán (backtracking + constraint checking).
- Cải tiến với kỹ thuật như:
            - Forward Checking
            - AC-3 (Arc Consistency) – loại trừ giá trị không hợp lệ sớm.

### **Hình ảnh giải thuật**
<table>
  <tr>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Backtracking.gif" width="150" /><br/>
      <b>Backtracking</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/AC.gif" width="150" /><br/>
      <b>AC3</b>
    </td>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/test.gif" width="150" /><br/>
      <b>Testing</b>
    </td>
  </tr>
</table>

### **Hình ảnh hiệu suất**
<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20175314.png" width="550"/>
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20175303.png" width="550"/>
</p>

<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20175328.png" width="550"/>
</p>

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### **2.6. Tìm kiếm học tăng cường (Reinforcement Learning Search)**
### **Đặc điểm**
- Tác nhân học thông qua tương tác với môi trường mà không cần mô hình đầy đủ.
- Phản hồi từ môi trường dưới dạng phần thưởng (reward) thay vì hướng dẫn trực tiếp.
- Hành động ảnh hưởng đến trạng thái tương lai và phần thưởng tích lũy.
- Cân bằng giữa khám phá (exploration) và khai thác (exploitation).
- Phù hợp với các môi trường không xác định, động, hoặc có chuỗi hành động dài.

### **Giải pháp**
- Học chính sách hoặc hàm giá trị để tối ưu phần thưởng
- Sử dụng các thuật toán như:
  - Q-Learning, SARSA – học giá trị hành động.
  - Deep Q-Network (DQN) – mở rộng với mạng nơ-ron.
  - Policy Gradient, Actor-Critic – học trực tiếp chính sách.
  - Dữ liệu học thu được từ quá trình tương tác liên tục với môi trường.
  - Cần có chiến lược khám phá như ε-greedy, Boltzmann, v.v
 
### **Hình ảnh giải thuật**
<table>
    <td align="center">
      <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/q.gif" width="150" /><br/>
      <b>QLearning</b>
    </td>
</table>

### **Hình ảnh hiệu suất**
<p align="center">
  <img src="https://github.com/NguyenThanhTin23/GIT_TEST/raw/20f25ce3670fc24702042d4300ecd9c72e293bb5/Screenshot%202025-05-17%20173615.png" width="550"/>
</p>

### **Nhận xét**
- Hiệu suất Q-Learning khá tốt: tỷ lệ thành công 66.7% và thất bại 33.3%. Thời gian trung bình để đạt thành công là 13.02 giây, có thể cần tối ưu thêm để nâng cao hiệu quả.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

### **3. Kết luận**
- Nắm vững nguyên lý hoạt động và cách áp dụng các thuật toán tìm kiếm trong không gian trạng thái, giúp nâng cao khả năng giải quyết các bài toán phức tạp.
- Giải pháp được xây dựng có khả năng tìm ra chuỗi hành động từ trạng thái ban đầu đến trạng thái đích một cách tối ưu hoặc gần tối ưu.
- Quá trình tìm kiếm được tối ưu nhằm giảm thiểu tài nguyên tính toán và thời gian xử lý, tăng hiệu suất cho chương trình.
- Giao diện trực quan giúp người dùng dễ dàng theo dõi từng bước giải, đồng thời hỗ trợ nhóm kiểm tra và hoàn thiện thuật toán hiệu quả hơn.
- Nhận thức rõ các thách thức khi tìm kiếm trong môi trường có ràng buộc và thông tin không đầy đủ, từ đó hiểu tầm quan trọng của việc thiết kế giải pháp phù hợp cho từng bài toán.
- Kết quả đạt được khẳng định tính khả thi của việc ứng dụng các thuật toán tìm kiếm trong trò chơi 8 puzzle, đồng thời mở rộng tiềm năng áp dụng vào nhiều bài toán thực tế khác trong lĩnh vực trí tuệ nhân tạo.
