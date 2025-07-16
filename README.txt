## 📦 C950 - WGUPS Truck Routing Program

This project was developed as part of the **Western Governors University (WGU) C950 - Data Structures and Algorithms** course. It simulates a real-world delivery scenario for the **Western Governors University Parcel Service (WGUPS)**, optimizing package delivery routes using a **Greedy Algorithm** and a custom-built **hash table**.

---

## 🚀 Project Overview

- Calculates the most efficient delivery routes for two trucks delivering packages.
- Ensures all packages are delivered **on time** and total mileage stays **under 140 miles**.
- Uses a **self-adjusting algorithm** and data structures to support fast lookups and dynamic routing.

---

## 🧠 Key Features

- Custom **Hash Table** implementation for efficient package lookup.
- **Greedy Algorithm** for route optimization (similar to nearest neighbor in TSP).
- Handles special package constraints like:
  - Delayed availability
  - Wrong address (corrected mid-delivery)
  - Truck-specific or grouped delivery

---

## 📂 File Structure

```

Salesman-Algorithm\_Project/
├── main.py                 # Main driver script
├── truck.py                # Truck class and routing logic
├── hash\_table.py           # Custom hash table implementation
├── package.py              # Package class
├── distance\_data.py        # Distance matrix and address list
└── README.md               # This file

````

---

## ⚙️ Technologies

- Python 3.x
- Standard Library only (no external dependencies)
- Time and datetime libraries used for scheduling

---

## ✅ How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/YourUsername/C950-Truck-Route.git
   cd C950-Truck-Route
````

2. Run the main script:

   ```bash
   python main.py
   ```

---

## 📖 Learning Outcomes

* Implemented complex data structures from scratch
* Solved a logistics-based optimization problem
* Strengthened Python skills and algorithm design
* Applied greedy algorithms to a real-world simulation

---

## 📜 License

This project is for educational use only, as part of the WGU curriculum.

---

## 🙋‍♂️ Author

**Robert Swallow**
Bachelor of Science – Computer Science (WGU)
[GitHub](https://github.com/RobertSwallow) • [LinkedIn](https://linkedin.com/in/robertswallow) • [swallow.brandon91@gmail.com](mailto:swallow.brandon91@gmail.com)

```
