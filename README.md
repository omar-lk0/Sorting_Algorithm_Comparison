# Experimental Comparison of Sorting Algorithms

This repository contains an experimental analysis of various sorting algorithms, comparing their performance across different data sizes and distributions. This project was developed as part of the **Academic Writing** and **Algorithms & Data Structures 1** curriculum.

## 🚀 Algorithms Implemented
- **Elementary Sorts ($O(n^2)$):** Bubble Sort, Selection Sort, Insertion Sort.
- **Efficient Sorts ($O(n \log n)$):** Merge Sort, Quick Sort, Heap Sort.

## 📊 Experiment Setup
The benchmarking script evaluates the algorithms based on:
- **Input Sizes ($n$):** 50, 500, 5,000, and 50,000.
- **Distributions:** - **Random:** Uniformly distributed integers.
  - **Sorted:** Data already in ascending order.
  - **Reverse:** Data in descending order.
  - **Nearly Sorted:** Sorted data with 2% random swaps.
  - **Flat:** Large lists with very few unique values (high duplicate count).
- **Data Types:** Verified support for Integers, Floats, and Strings.

## 📈 Key Findings
- **Complexity Gap:** The transition from $n=500$ to $n=5,000$ clearly shows the exponential growth of Bubble Sort (~2.6s) vs. the linear-logarithmic growth of Quick Sort (~18ms).
- **Quick Sort Anomaly:** During the $n=50,000$ test, Quick Sort experienced a significant performance drop on "Flat" data distributions (taking ~80s). This highlights the vulnerability of certain partitioning schemes to high-frequency duplicates.
- **Insertion Sort Efficiency:** Insertion Sort outperformed all other algorithms on "Sorted" and "Nearly Sorted" data at small to medium scales.

## 🛠️ How to Run
1. Ensure you have Python 3.x installed.
2. Clone the repository:
   ```bash
   git clone [https://github.com/omar-lk0/Sorting-Algorithm-Comparison.git](https://github.com/omar-lk0/Sorting-Algorithm-Comparison.git)
