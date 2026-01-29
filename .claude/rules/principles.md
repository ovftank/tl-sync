---
paths:
  - "**"
---

# Programming Principles

## Principles (Priority Order)

Khi có xung đột, ưu tiên theo thứ tự:

1. **KISS** - Giữ code đơn giản, dễ hiểu
2. **YAGNI** - Không implement "trong trường hợp cần sau này"
3. **DRY** - Tránh lặp code (nhưng 2-3 dòng lặp lại OK)

### KISS - Keep It Simple, Stupid

- Đơn giản hơn phức tạp
- Đọc hiểu hơn clever
- Code rõ ràng > code ngắn gọn

### YAGNI - You Aren't Gonna Need It

- Chỉ làm những gì được yêu cầu
- Không implement tính năng "có thể cần sau này"
- Tránh premature optimization

### DRY - Don't Repeat Yourself

- 2-3 dòng lặp lại: OK, đừng over-abstract
- 4+ dòng lặp lại: extract function
- Balance giữa reuse và simplicity

### SOLID (khi cần thiết)

- **SRP** - Mỗi module 1 trách nhiệm (ưu tiên nhất)
- **OCP** - Mở rộng, không sửa đổi code hiện có
- **LSP** - Subclass thay thế được superclass
- **ISP** - Interface nhỏ, focused
- **DIP** - Phụ thuộc vào abstraction, không concrete

### Separation of Concerns

- Tách biệt các công việc vào modules khác nhau
- Giảm dependency giữa components
- Mỗi module có trách nhiệm rõ ràng
- Please think step by step about whether there exists a less over-engineered and yet simpler, more elegant, and more robust solution that accords with KISS and DRY principles.
