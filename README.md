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
   Trạng thái này là điểm bắt đầu cho quá trình tìm k130" /><br/>
      <b>Genetic</b>
    </td>
  </tr>
</table>
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

