
# Interactive Graph Algorithms Visualizer  
### เว็บสำหรับเรียนรู้อัลกอริทึมกราฟแบบ Step-by-Step ด้วย Streamlit

โปรเจกต์นี้เป็นเว็บแอปสำหรับ **จำลองและแสดงภาพการทำงานของอัลกอริทึมบนกราฟ** แบบทีละขั้นตอน ใช้เทคโนโลยี  
**Streamlit + NetworkX + streamlit-agraph**  
เหมาะสำหรับใช้สอนหรือใช้เรียนวิชาโครงสร้างข้อมูล (Data Structures) / Discrete Mathematics / Algorithm

---

## ฟีเจอร์หลัก

### 1. ชุดกราฟตัวอย่าง (Testcases) ให้เลือกใช้งานทันที

มีกราฟตัวอย่างหลายรูปแบบ เช่น

- 3x3 Grid  
- Hexagon / Grid  
- Pentagon Star  
- Composite Graph (สี่เหลี่ยม + สี่เหลี่ยมผืนผ้า)  
- กราฟตัวอย่างสำหรับ Dijkstra หลายแบบ  
- กราฟตัวอย่างสำหรับ MST หลายแบบ เช่น House, Bridge, Star, Cross ฯลฯ  

แต่ละ testcase จะกำหนด:
- รายชื่อโหนด (nodes)  
- รายการเส้นเชื่อมพร้อมน้ำหนัก (weighted edges)  
- ตำแหน่งของโหนดบนหน้าจอ (fixed positions) เพื่อให้รูปกราฟดูสวยและอ่านง่าย  

นอกจากนี้ยังมีโหมด **Custom** ให้ผู้ใช้เพิ่มโหนดและเส้นเชื่อมเองได้จาก Sidebar

---

## 2. อัลกอริทึมที่รองรับ

### Depth-First Search (DFS)
- ใช้การเรียกฟังก์ชันแบบ recursive  
- บันทึกลำดับการเยี่ยมโหนด และเส้นที่สำรวจ  
- แสดงโหนดที่ถูกเยี่ยมแล้วเป็นสีเขียว  

### Breadth-First Search (BFS)
- ใช้โครงสร้างข้อมูลคิว (Queue)  
- บันทึกเส้นที่ค้นพบและโหนดที่เข้าคิว / ถูกเยี่ยมแล้ว  
- แสดงลำดับการเดินกราฟอย่างชัดเจน  

### Dijkstra’s Shortest Path
- ใช้ Priority Queue (min-heap) ในการเลือกระยะทางที่น้อยที่สุด  
- บันทึกทุกขั้นตอนการตรวจสอบระยะทางและการอัปเดตค่า Distance  
- แสดงตารางระยะทาง (Distance Table) แบบสด ๆ  
- เมื่อจบแล้วจะไฮไลต์ **Shortest Path** กลับจากปลายทางไปยังจุดเริ่มต้น  
- รองรับกรณีที่ปลายทางไปไม่ถึง (unreachable)  

### Minimum Spanning Tree (MST)

รองรับ 2 แบบ:

#### Kruskal
- เรียงเส้นเชื่อมทุกเส้นตามน้ำหนักจากน้อยไปมาก  
- ใช้โครงสร้าง Union-Find / Disjoint Set ในการเช็ค cycle  
- บันทึกว่าขั้นตอนไหน “เลือกเส้น” เข้าสู่ MST และขั้นตอนไหน “ข้ามเส้น” เพราะทำให้เกิดวงจร  

#### Prim (Implement เองแบบละเอียด)
- เลือกจุดเริ่มต้น (start node) ได้จาก Sidebar  
- ใช้ Priority Queue เก็บ “เส้นเชื่อมที่เป็นตัวเลือก” (candidate edges)  
- เลือกเส้นที่เบาที่สุดจากโหนดที่อยู่ใน MST ไปยังโหนดใหม่  
- บันทึก log ทั้งเส้นที่ “เพิ่มเข้าเป็นตัวเลือก” และเส้นที่ “ถูกเลือกเข้าจริง” ใน MST  

---

## 3. การแสดงผลแบบ Interactive

ส่วนแสดงผลหลัก (Main Area) จะมี:

- โหนดสีต่าง ๆ  
  - สีขาว: ยังไม่ถูกเยี่ยม  
  - สีเขียว: ถูกเยี่ยมแล้ว / อยู่บนเส้นทางที่เลือก  
  - สีส้ม: โหนดที่กำลังถูกประมวลผล (current node)  

- เส้นเชื่อม (Edge)  
  - เส้นปกติ: สีเทา  
  - เส้นบนเส้นทาง หรือเส้นที่เกี่ยวข้องกับขั้นตอนปัจจุบัน: สีเขียว หนา  

- มีตัวนับ Step พร้อมปุ่มควบคุม
  - ◀ Prev Step  
  - Next Step ▶  
  - Instant Skip ⏩ (กระโดดไปขั้นสุดท้ายทันที)  

---

## 4. แผงสถานะ (Status Panel)

ด้านขวาของหน้าเว็บจะแสดง:

- ผลลัพธ์สุดท้ายของอัลกอริทึม  
  - DFS / BFS: ลำดับการเดินกราฟ (Traversal Order)  
  - Dijkstra: Shortest Path + Total Distance  
  - MST: น้ำหนักรวมของ MST และรายชื่อเส้นที่อยู่ใน MST  

- Action ปัจจุบัน (ข้อความอธิบายว่า Step นี้กำลังทำอะไร)  
- กรณี Dijkstra จะมี  
  - ตาราง Distance ของทุกโหนด (แสดงเป็น ∞ ถ้ายังไปไม่ถึง)  
- Legend อธิบายความหมายของสีโหนด  

---

main.py                 # ไฟล์ Streamlit app หลัก
README.md               # ไฟล์อธิบายโปรเจกต์

## ภาพรวมโค้ดในไฟล์นี้


ใน `main.py` ส่วนสำคัญ ๆ ได้แก่:

### 1. TESTCASES
ชุดข้อมูลกราฟตัวอย่าง:
- nodes: รายชื่อโหนด  
- edges: (u, v, weight)  
- pos: ตำแหน่ง (x, y) ของแต่ละโหนด  

### 2. คลาส GraphAlgorithms

รวบรวมอัลกอริทึมทั้งหมด:

- `get_dfs_steps(start_node)`  
- `get_bfs_steps(start_node)`  
- `get_dijkstra_steps(start, end)`  
- `get_mst_steps(algo="kruskal", start_node=None)`  

ฟังก์ชันเหล่านี้จะ **ไม่เพียงแค่คำนวณผลลัพธ์** แต่ยัง:
- คืนค่า `steps` (list ของ Step) ที่ใช้สำหรับ visualization แต่ละก้าวของอัลกอริทึม
- แต่ละ step จะบอกประเภท เช่น `"node"`, `"edge"`, `"current"`, `"check_edge"`, `"update"`, `"add_edge"`, `"finished"` พร้อมข้อความ log ประกอบ

### 3. ฟังก์ชัน `convert_to_agraph(...)`

แปลงกราฟจาก NetworkX เป็นโครงสร้างที่ใช้กับ `streamlit-agraph`:

- สร้าง `Node(...)` พร้อมสี ตำแหน่ง ขนาด และ label  
- สร้าง `Edge(...)` พร้อม label น้ำหนัก สี และความหนา  
- ใช้ชุด `highlight_nodes` และ `highlight_edges` เพื่อกำหนดว่าตัวไหนต้องเน้นสี  

### 4. ฟังก์ชัน `main()` (ตัวเว็บจริงของ Streamlit)

ประกอบด้วย:

- `st.sidebar` สำหรับ:
  - เลือก testcase  
  - ปุ่ม Reset / Load Graph  
  - ฟอร์มเพิ่ม Node / Edge  
  - เลือกอัลกอริทึม  
  - เลือก Start Node / End Node  
  - ปุ่ม Initialize Algorithm  

- การสร้างอ็อบเจกต์ NetworkX Graph จาก `st.session_state["graph_data"]`  

- การจัดการ `session_state`:
  - `graph_data`: โหนด, เส้น, และตำแหน่ง  
  - `algo_steps`: รายการ steps ของอัลกอริทึม  
  - `step_idx`: index ของ step ปัจจุบัน  
  - `final_result`: ข้อความสรุปผลสุดท้าย  

- ส่วนแสดงผล:
  - ปุ่มเปลี่ยน step  
  - กราฟ interactive ด้วย `agraph(...)`  
  - Status Panel + Distance Table  

---

## วิธีติดตั้งและใช้งาน

### 1. ติดตั้ง Python และไลบรารีที่จำเป็น

แนะนำ Python 3.9 ขึ้นไป

```bash
pip install streamlit networkx pandas streamlit-agraph
```

### 2. รันแอป

สมมติว่าไฟล์นี้ชื่อ `main.py`

```bash
streamlit run main.py
```

เปิดเว็บเบราว์เซอร์ที่ลิงก์ที่ Streamlit แสดง (เช่น http://localhost:8501)

## วิธีใช้งานในหน้าเว็บ

1. ไปที่ Sidebar:
    - เลือกกราฟจากเมนู **Load Testcase** หรือเลือก "Custom" เพื่อสร้างเอง
    - กดปุ่ม **Reset / Load Graph** เพื่อโหลดกราฟ
2. ถ้าต้องการแก้กราฟเอง:
    - ใช้ส่วน "Edit Graph (Add Node/Edge)"
    - ใส่ชื่อโหนดใหม่แล้วกด Add Node
    - ใส่ From / To / Weight แล้วกด Add Edge
3. เลือกอัลกอริทึมจากเมนู:
    - DFS
    - BFS
    - Dijkstra
    - MST (Kruskal)
    - MST (Prim)
4. เลือกจุดเริ่มต้น (Start Node) และปลายทาง (End Node) หากอัลกอริทึมต้องใช้
5. กด **Initialize Algorithm**
6. ใช้ปุ่ม:
    - ◀ Prev Step
    - Next Step ▶
    - Instant Skip ⏩
        
        เพื่อไล่ดูการทำงานทีละขั้นหรือข้ามไปดูผลลัพธ์เลย
        

---

## จุดเด่นของโปรเจกต์นี้

- เน้นการเรียนรู้ “ทีละขั้นตอน” (Step-by-step) ไม่ใช่แค่เห็นผลลัพธ์สุดท้าย
- โค้ดอ่านง่าย แยกส่วนชัดเจน เหมาะสำหรับใช้เป็นตัวอย่างประกอบการสอนในห้องเรียน
- ผู้ใช้สามารถทดลองเปลี่ยนกราฟเองได้ ทำให้เข้าใจพฤติกรรมของอัลกอริทึมในกรณีต่าง ๆ
- รองรับทั้ง DFS, BFS, Dijkstra และ MST (Kruskal + Prim) ในระบบเดียว

---