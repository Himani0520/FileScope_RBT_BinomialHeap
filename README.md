# FileScope: File System Analyzer using Red-Black Tree and Binomial Heap

## Overview

FileScope is a desktop-based file system analysis tool that leverages advanced data structures to efficiently organize, query, and visualize files within a selected directory. The application integrates Red-Black Trees for balanced search operations and Binomial Heaps for efficient priority-based retrieval.

The project demonstrates the practical application of data structures in solving real-world problems, combined with an interactive graphical interface.

---

## Key Features

* Directory scanning and file indexing
* Efficient storage using Red-Black Tree (self-balancing BST)
* Priority-based operations using Binomial Heap
* Visualization of both data structures
* Search functionality based on file names
* Sorting options (size and modification time)
* File detail inspection (name, size, path, timestamp)
* Statistical summary of files (total count, size, largest, smallest)
* Interactive node highlighting in visualization

---

## Technologies Used

* Python
* Tkinter (GUI development)
* Humanize (readable file sizes)

---

## Data Structures Used

### Red-Black Tree

* Maintains balanced structure for efficient operations
* Provides O(log n) insertion and search
* Used for organizing files based on size

### Binomial Heap

* Supports efficient minimum extraction
* Used for identifying smallest files quickly
* Maintains heap-ordered tree structure

---

## Installation and Setup

1. Clone the repository:

```bash
git clone https://github.com/your-username/FileScope_RBT_BinomialHeap.git
cd FileScope_RBT_BinomialHeap
```

2. Install dependencies:

```bash
pip install humanize
```

3. Run the application:

```bash
python DAA_Main.py
```

---

## Usage

1. Launch the application
2. Select a directory
3. View file structure visualization
4. Use sorting and search features
5. Inspect file details via selection
6. Perform operations like:

   * Find largest file
   * Find most recent file
   * Extract smallest file

---

## Screenshots

<img width="1919" height="1028" alt="image" src="https://github.com/user-attachments/assets/80977a03-bbc2-4cdd-bf24-6de0f09d98a1" />
<img width="1909" height="1017" alt="image" src="https://github.com/user-attachments/assets/c1655981-e3de-47e1-9304-bae31588739e" />
<img width="1611" height="573" alt="image" src="https://github.com/user-attachments/assets/d755595f-a172-4342-b730-4cf69621c8ae" />

## Future Enhancements

* Improved visualization layout
* File filtering options
* Export functionality
* Performance optimization for large datasets

---

## Author

Himani Deopura
