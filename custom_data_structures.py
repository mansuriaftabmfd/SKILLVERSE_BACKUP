"""
Custom Data Structures Implementation from Scratch
Author: SkillVerse Team
Purpose: Demonstrate data structure concepts by implementing them from scratch

This module contains custom implementations of common data structures:
1. CustomList (Dynamic Array)
2. CustomDict (Hash Table)
3. CustomSet (Hash Set)
4. CustomQueue (FIFO Queue)
5. CustomStack (LIFO Stack)
6. LinkedList (Singly Linked List)
7. DoublyLinkedList
8. BinarySearchTree
9. MinHeap / MaxHeap
10. Graph (Adjacency List)

PRODUCTION IMPLEMENTATIONS (Used in SkillVerse):
11. HashMap - For caching featured services (O(1) lookup)
12. Queue - For FIFO order processing (O(1) enqueue/dequeue)
13. Trie - For search autocomplete (O(k) where k = word length)
14. MaxHeap - For sorting top-rated services (O(log n) operations)

All implementations maintain the same interface as Python's built-in types
so they can be used as drop-in replacements without changing application logic.
"""


# ============================================================================
# 1. CUSTOM LIST (Dynamic Array Implementation)
# ============================================================================

class CustomList:
    """
    Custom implementation of Python's list using dynamic array
    
    Time Complexity:
    - Access: O(1)
    - Append: O(1) amortized
    - Insert: O(n)
    - Delete: O(n)
    - Search: O(n)
    
    Space Complexity: O(n)
    """
    
    def __init__(self, initial_capacity=10):
        """Initialize with default capacity"""
        self._capacity = initial_capacity
        self._size = 0
        self._data = [None] * self._capacity
    
    def __len__(self):
        """Return number of elements"""
        return self._size
    
    def __getitem__(self, index):
        """Get item at index"""
        if not -self._size <= index < self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        return self._data[index]
    
    def __setitem__(self, index, value):
        """Set item at index"""
        if not -self._size <= index < self._size:
            raise IndexError("Index out of range")
        if index < 0:
            index += self._size
        self._data[index] = value
    
    def append(self, value):
        """Add element to end - O(1) amortized"""
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        self._data[self._size] = value
        self._size += 1
    
    def insert(self, index, value):
        """Insert element at index - O(n)"""
        if index < 0:
            index = max(0, self._size + index)
        if index > self._size:
            index = self._size
        
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        
        # Shift elements right
        for i in range(self._size, index, -1):
            self._data[i] = self._data[i - 1]
        
        self._data[index] = value
        self._size += 1
    
    def remove(self, value):
        """Remove first occurrence of value - O(n)"""
        for i in range(self._size):
            if self._data[i] == value:
                self.pop(i)
                return
        raise ValueError(f"{value} not in list")
    
    def pop(self, index=-1):
        """Remove and return element at index - O(n)"""
        if self._size == 0:
            raise IndexError("Pop from empty list")
        
        if index < 0:
            index += self._size
        if not 0 <= index < self._size:
            raise IndexError("Index out of range")
        
        value = self._data[index]
        
        # Shift elements left
        for i in range(index, self._size - 1):
            self._data[i] = self._data[i + 1]
        
        self._size -= 1
        self._data[self._size] = None
        
        return value
    
    def _resize(self, new_capacity):
        """Resize internal array"""
        new_data = [None] * new_capacity
        for i in range(self._size):
            new_data[i] = self._data[i]
        self._data = new_data
        self._capacity = new_capacity
    
    def __iter__(self):
        """Make iterable"""
        for i in range(self._size):
            yield self._data[i]
    
    def __repr__(self):
        """String representation"""
        return f"CustomList([{', '.join(repr(x) for x in self)}])"


# ============================================================================
# 2. CUSTOM DICT (Hash Table Implementation)
# ============================================================================

class CustomDict:
    """
    Custom implementation of Python's dict using hash table with chaining
    
    Time Complexity:
    - Access: O(1) average, O(n) worst
    - Insert: O(1) average, O(n) worst
    - Delete: O(1) average, O(n) worst
    - Search: O(1) average, O(n) worst
    
    Space Complexity: O(n)
    """
    
    def __init__(self, initial_capacity=16):
        """Initialize hash table"""
        self._capacity = initial_capacity
        self._size = 0
        self._buckets = [CustomList() for _ in range(self._capacity)]
        self._load_factor_threshold = 0.75
    
    def _hash(self, key):
        """Hash function"""
        return hash(key) % self._capacity
    
    def __setitem__(self, key, value):
        """Set key-value pair - O(1) average"""
        # Check load factor and resize if needed
        if self._size / self._capacity > self._load_factor_threshold:
            self._resize(2 * self._capacity)
        
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self._size += 1
    
    def __getitem__(self, key):
        """Get value by key - O(1) average"""
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(key)
    
    def __delitem__(self, key):
        """Delete key-value pair - O(1) average"""
        bucket_index = self._hash(key)
        bucket = self._buckets[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self._size -= 1
                return
        
        raise KeyError(key)
    
    def get(self, key, default=None):
        """Get value with default"""
        try:
            return self[key]
        except KeyError:
            return default
    
    def keys(self):
        """Return all keys"""
        result = CustomList()
        for bucket in self._buckets:
            for k, v in bucket:
                result.append(k)
        return result
    
    def values(self):
        """Return all values"""
        result = CustomList()
        for bucket in self._buckets:
            for k, v in bucket:
                result.append(v)
        return result
    
    def items(self):
        """Return all key-value pairs"""
        result = CustomList()
        for bucket in self._buckets:
            for item in bucket:
                result.append(item)
        return result
    
    def __contains__(self, key):
        """Check if key exists"""
        try:
            self[key]
            return True
        except KeyError:
            return False
    
    def __len__(self):
        """Return number of items"""
        return self._size
    
    def _resize(self, new_capacity):
        """Resize hash table"""
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [CustomList() for _ in range(self._capacity)]
        self._size = 0
        
        # Rehash all items
        for bucket in old_buckets:
            for k, v in bucket:
                self[k] = v
    
    def __iter__(self):
        """Iterate over keys"""
        for bucket in self._buckets:
            for k, v in bucket:
                yield k
    
    def __repr__(self):
        """String representation"""
        items = ', '.join(f"{repr(k)}: {repr(v)}" for k, v in self.items())
        return f"CustomDict({{{items}}})"


# ============================================================================
# 3. CUSTOM SET (Hash Set Implementation)
# ============================================================================

class CustomSet:
    """
    Custom implementation of Python's set using hash table
    
    Time Complexity:
    - Add: O(1) average
    - Remove: O(1) average
    - Contains: O(1) average
    
    Space Complexity: O(n)
    """
    
    def __init__(self, iterable=None):
        """Initialize set"""
        self._dict = CustomDict()
        if iterable:
            for item in iterable:
                self.add(item)
    
    def add(self, item):
        """Add item to set"""
        self._dict[item] = True
    
    def remove(self, item):
        """Remove item from set"""
        del self._dict[item]
    
    def discard(self, item):
        """Remove item if exists"""
        try:
            self.remove(item)
        except KeyError:
            pass
    
    def __contains__(self, item):
        """Check if item in set"""
        return item in self._dict
    
    def __len__(self):
        """Return size"""
        return len(self._dict)
    
    def __iter__(self):
        """Iterate over items"""
        return iter(self._dict.keys())
    
    def __repr__(self):
        """String representation"""
        items = ', '.join(repr(x) for x in self)
        return f"CustomSet({{{items}}})"


# ============================================================================
# 4. CUSTOM QUEUE (FIFO - First In First Out)
# ============================================================================

class CustomQueue:
    """
    Custom Queue implementation using linked list
    
    Time Complexity:
    - Enqueue: O(1)
    - Dequeue: O(1)
    - Peek: O(1)
    
    Space Complexity: O(n)
    """
    
    class _Node:
        """Internal node class"""
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        """Initialize empty queue"""
        self._front = None
        self._rear = None
        self._size = 0
    
    def enqueue(self, item):
        """Add item to rear - O(1)"""
        new_node = self._Node(item)
        
        if self._rear is None:
            self._front = self._rear = new_node
        else:
            self._rear.next = new_node
            self._rear = new_node
        
        self._size += 1
    
    def dequeue(self):
        """Remove and return front item - O(1)"""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        
        item = self._front.data
        self._front = self._front.next
        
        if self._front is None:
            self._rear = None
        
        self._size -= 1
        return item
    
    def peek(self):
        """Return front item without removing"""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self._front.data
    
    def is_empty(self):
        """Check if queue is empty"""
        return self._size == 0
    
    def __len__(self):
        """Return size"""
        return self._size
    
    def __repr__(self):
        """String representation"""
        items = []
        current = self._front
        while current:
            items.append(repr(current.data))
            current = current.next
        return f"CustomQueue([{', '.join(items)}])"


# ============================================================================
# 5. CUSTOM STACK (LIFO - Last In First Out)
# ============================================================================

class CustomStack:
    """
    Custom Stack implementation using dynamic array
    
    Time Complexity:
    - Push: O(1) amortized
    - Pop: O(1)
    - Peek: O(1)
    
    Space Complexity: O(n)
    """
    
    def __init__(self):
        """Initialize empty stack"""
        self._items = CustomList()
    
    def push(self, item):
        """Push item onto stack - O(1)"""
        self._items.append(item)
    
    def pop(self):
        """Pop and return top item - O(1)"""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        """Return top item without removing"""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self._items) == 0
    
    def __len__(self):
        """Return size"""
        return len(self._items)
    
    def __repr__(self):
        """String representation"""
        return f"CustomStack({list(self._items)})"



# ============================================================================
# 6. LINKED LIST (Singly Linked List)
# ============================================================================

class LinkedList:
    """
    Singly Linked List implementation
    
    Time Complexity:
    - Insert at head: O(1)
    - Insert at tail: O(n) or O(1) with tail pointer
    - Delete: O(n)
    - Search: O(n)
    
    Space Complexity: O(n)
    """
    
    class Node:
        """Node class for linked list"""
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        """Initialize empty list"""
        self.head = None
        self._size = 0
    
    def insert_at_head(self, data):
        """Insert at beginning - O(1)"""
        new_node = self.Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1
    
    def insert_at_tail(self, data):
        """Insert at end - O(n)"""
        new_node = self.Node(data)
        
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        
        self._size += 1
    
    def delete(self, data):
        """Delete first occurrence - O(n)"""
        if not self.head:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self._size -= 1
                return True
            current = current.next
        
        return False
    
    def search(self, data):
        """Search for data - O(n)"""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def __len__(self):
        """Return size"""
        return self._size
    
    def __iter__(self):
        """Make iterable"""
        current = self.head
        while current:
            yield current.data
            current = current.next
    
    def __repr__(self):
        """String representation"""
        return f"LinkedList([{' -> '.join(repr(x) for x in self)}])"


# ============================================================================
# 7. BINARY SEARCH TREE
# ============================================================================

class BinarySearchTree:
    """
    Binary Search Tree implementation
    
    Time Complexity (balanced):
    - Insert: O(log n)
    - Delete: O(log n)
    - Search: O(log n)
    
    Time Complexity (worst case - skewed):
    - Insert: O(n)
    - Delete: O(n)
    - Search: O(n)
    
    Space Complexity: O(n)
    """
    
    class Node:
        """Node class for BST"""
        def __init__(self, data):
            self.data = data
            self.left = None
            self.right = None
    
    def __init__(self):
        """Initialize empty tree"""
        self.root = None
        self._size = 0
    
    def insert(self, data):
        """Insert data into tree"""
        if not self.root:
            self.root = self.Node(data)
            self._size += 1
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node, data):
        """Helper method for insertion"""
        if data < node.data:
            if node.left is None:
                node.left = self.Node(data)
                self._size += 1
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = self.Node(data)
                self._size += 1
            else:
                self._insert_recursive(node.right, data)
    
    def search(self, data):
        """Search for data in tree"""
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node, data):
        """Helper method for search"""
        if node is None:
            return False
        if data == node.data:
            return True
        elif data < node.data:
            return self._search_recursive(node.left, data)
        else:
            return self._search_recursive(node.right, data)
    
    def inorder_traversal(self):
        """Return inorder traversal (sorted)"""
        result = CustomList()
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)
    
    def __len__(self):
        """Return size"""
        return self._size
    
    def __contains__(self, data):
        """Check if data exists"""
        return self.search(data)


# ============================================================================
# 8. MIN HEAP (Priority Queue)
# ============================================================================

class MinHeap:
    """
    Min Heap implementation (Priority Queue)
    
    Time Complexity:
    - Insert: O(log n)
    - Extract Min: O(log n)
    - Get Min: O(1)
    
    Space Complexity: O(n)
    """
    
    def __init__(self):
        """Initialize empty heap"""
        self._heap = CustomList()
    
    def _parent(self, index):
        """Get parent index"""
        return (index - 1) // 2
    
    def _left_child(self, index):
        """Get left child index"""
        return 2 * index + 1
    
    def _right_child(self, index):
        """Get right child index"""
        return 2 * index + 2
    
    def _swap(self, i, j):
        """Swap two elements"""
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
    
    def insert(self, value):
        """Insert value into heap - O(log n)"""
        self._heap.append(value)
        self._heapify_up(len(self._heap) - 1)
    
    def _heapify_up(self, index):
        """Bubble up to maintain heap property"""
        parent = self._parent(index)
        if index > 0 and self._heap[index] < self._heap[parent]:
            self._swap(index, parent)
            self._heapify_up(parent)
    
    def extract_min(self):
        """Remove and return minimum - O(log n)"""
        if len(self._heap) == 0:
            raise IndexError("Extract from empty heap")
        
        min_val = self._heap[0]
        last_val = self._heap.pop()
        
        if len(self._heap) > 0:
            self._heap[0] = last_val
            self._heapify_down(0)
        
        return min_val
    
    def _heapify_down(self, index):
        """Bubble down to maintain heap property"""
        smallest = index
        left = self._left_child(index)
        right = self._right_child(index)
        
        if left < len(self._heap) and self._heap[left] < self._heap[smallest]:
            smallest = left
        
        if right < len(self._heap) and self._heap[right] < self._heap[smallest]:
            smallest = right
        
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)
    
    def get_min(self):
        """Return minimum without removing - O(1)"""
        if len(self._heap) == 0:
            raise IndexError("Peek from empty heap")
        return self._heap[0]
    
    def __len__(self):
        """Return size"""
        return len(self._heap)
    
    def is_empty(self):
        """Check if heap is empty"""
        return len(self._heap) == 0


# ============================================================================
# 9. GRAPH (Adjacency List)
# ============================================================================

class Graph:
    """
    Graph implementation using adjacency list
    
    Time Complexity:
    - Add Vertex: O(1)
    - Add Edge: O(1)
    - Remove Vertex: O(V + E)
    - Remove Edge: O(E)
    - BFS/DFS: O(V + E)
    
    Space Complexity: O(V + E)
    """
    
    def __init__(self, directed=False):
        """Initialize empty graph"""
        self._adj_list = CustomDict()
        self._directed = directed
    
    def add_vertex(self, vertex):
        """Add vertex to graph"""
        if vertex not in self._adj_list:
            self._adj_list[vertex] = CustomList()
    
    def add_edge(self, from_vertex, to_vertex, weight=1):
        """Add edge between vertices"""
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        
        self._adj_list[from_vertex].append((to_vertex, weight))
        
        if not self._directed:
            self._adj_list[to_vertex].append((from_vertex, weight))
    
    def get_neighbors(self, vertex):
        """Get neighbors of vertex"""
        return self._adj_list.get(vertex, CustomList())
    
    def bfs(self, start_vertex):
        """Breadth-First Search traversal"""
        if start_vertex not in self._adj_list:
            return CustomList()
        
        visited = CustomSet()
        queue = CustomQueue()
        result = CustomList()
        
        queue.enqueue(start_vertex)
        visited.add(start_vertex)
        
        while not queue.is_empty():
            vertex = queue.dequeue()
            result.append(vertex)
            
            for neighbor, _ in self.get_neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue(neighbor)
        
        return result
    
    def dfs(self, start_vertex):
        """Depth-First Search traversal"""
        if start_vertex not in self._adj_list:
            return CustomList()
        
        visited = CustomSet()
        result = CustomList()
        
        self._dfs_recursive(start_vertex, visited, result)
        
        return result
    
    def _dfs_recursive(self, vertex, visited, result):
        """Helper for DFS"""
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor, _ in self.get_neighbors(vertex):
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, result)
    
    def __repr__(self):
        """String representation"""
        edges = []
        for vertex in self._adj_list:
            for neighbor, weight in self._adj_list[vertex]:
                edges.append(f"{vertex} -> {neighbor} ({weight})")
        return f"Graph({', '.join(edges)})"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def convert_to_custom_list(python_list):
    """Convert Python list to CustomList"""
    custom = CustomList()
    for item in python_list:
        custom.append(item)
    return custom


def convert_to_custom_dict(python_dict):
    """Convert Python dict to CustomDict"""
    custom = CustomDict()
    for key, value in python_dict.items():
        custom[key] = value
    return custom


def convert_to_custom_set(python_set):
    """Convert Python set to CustomSet"""
    return CustomSet(python_set)


# ============================================================================
# PRODUCTION DATA STRUCTURES (Used in SkillVerse Application)
# ============================================================================

# ============================================================================
# 1. HASHMAP - For Caching Featured Services
# ============================================================================

class HashMap:
    """
    HashMap implementation for caching featured services
    
    Used in: ServiceManager._cache (managers.py)
    Purpose: Cache featured services to avoid repeated database queries
    
    Time Complexity:
    - get(key): O(1) average
    - set(key, value): O(1) average
    - delete(key): O(1) average
    - clear(): O(1)
    
    How it works:
    1. User visits homepage → DB query → 5 services → store in cache
    2. User visits AGAIN → cache hit → instant return (no DB query!)
    3. Admin approves service → cache.clear() → fresh data next time
    
    Internal Structure:
    - 16 buckets (array of linked lists)
    - Hash function: hash(key) % 16
    - Collision handling: Chaining (linked list in each bucket)
    """
    
    def __init__(self, capacity=16):
        """Initialize HashMap with 16 buckets"""
        self.capacity = capacity
        self.buckets = [[] for _ in range(capacity)]  # Array of lists
        self.size = 0
    
    def _hash(self, key):
        """
        Hash function to convert key to bucket index
        
        Example:
        key = 'featured_services_4'
        hash('featured_services_4') = 123456789
        bucket_index = 123456789 % 16 = 5
        → Store in bucket[5]
        """
        return hash(key) % self.capacity
    
    def set(self, key, value):
        """
        Store key-value pair in HashMap
        
        Example:
        cache.set('featured_services_4', [service1, service2, ...])
        
        Steps:
        1. Hash key → get bucket index
        2. Check if key exists in bucket → update
        3. If not exists → append new (key, value) pair
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
    
    def get(self, key, default=None):
        """
        Retrieve value by key
        
        Example:
        services = cache.get('featured_services_4')
        
        Steps:
        1. Hash key → get bucket index
        2. Search in bucket's linked list
        3. Return value if found, else default
        """
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        return default
    
    def __contains__(self, key):
        """Check if key exists (for 'in' operator)"""
        return self.get(key) is not None
    
    def delete(self, key):
        """Remove key-value pair"""
        bucket_index = self._hash(key)
        bucket = self.buckets[bucket_index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return True
        return False
    
    def clear(self):
        """
        Clear all cached data
        
        Used when: Admin approves new service → cache must refresh
        """
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
    
    def __len__(self):
        """Return number of items in cache"""
        return self.size
    
    def __repr__(self):
        """String representation"""
        items = []
        for bucket in self.buckets:
            items.extend(bucket)
        return f"HashMap({dict(items)})"


# ============================================================================
# 2. QUEUE - For FIFO Order Processing
# ============================================================================

class Queue:
    """
    Queue implementation for fair order processing (FIFO)
    
    Used in: OrderManager.processing_queue (managers.py)
    Purpose: Process orders in the order they arrive (first come, first served)
    
    Time Complexity:
    - enqueue(item): O(1)
    - dequeue(): O(1)
    - peek(): O(1)
    
    How it works:
    1. Customer A places order #101 → enqueue(101) → Queue: [101]
    2. Customer B places order #102 → enqueue(102) → Queue: [101, 102]
    3. Customer C places order #103 → enqueue(103) → Queue: [101, 102, 103]
    4. Provider processes → dequeue() → Order #101 (came first!)
    5. Provider processes → dequeue() → Order #102 (came second!)
    
    Internal Structure:
    - Linked list with front and rear pointers
    - Front: Where we dequeue (remove)
    - Rear: Where we enqueue (add)
    
    Visual:
    [FRONT] 101 → 102 → 103 [REAR]
            ↑              ↑
         dequeue        enqueue
    """
    
    class _Node:
        """Internal node for linked list"""
        def __init__(self, data):
            self.data = data
            self.next = None
    
    def __init__(self):
        """Initialize empty queue"""
        self.front = None
        self.rear = None
        self.size = 0
    
    def enqueue(self, item):
        """
        Add item to rear of queue
        
        Example:
        queue.enqueue(101)  # Order #101 joins the line
        
        Steps:
        1. Create new node with order ID
        2. If queue empty → front = rear = new node
        3. Else → rear.next = new node, rear = new node
        """
        new_node = self._Node(item)
        
        if self.rear is None:
            # Queue is empty
            self.front = self.rear = new_node
        else:
            # Add to rear
            self.rear.next = new_node
            self.rear = new_node
        
        self.size += 1
    
    def dequeue(self):
        """
        Remove and return item from front of queue
        
        Example:
        order_id = queue.dequeue()  # Get next order to process
        
        Steps:
        1. If queue empty → raise error
        2. Get data from front node
        3. Move front pointer to next node
        4. If queue becomes empty → rear = None
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        
        item = self.front.data
        self.front = self.front.next
        
        if self.front is None:
            # Queue is now empty
            self.rear = None
        
        self.size -= 1
        return item
    
    def peek(self):
        """View front item without removing"""
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.front.data
    
    def is_empty(self):
        """Check if queue is empty"""
        return self.size == 0
    
    def __len__(self):
        """Return queue size"""
        return self.size
    
    def __repr__(self):
        """String representation"""
        items = []
        current = self.front
        while current:
            items.append(str(current.data))
            current = current.next
        return f"Queue([{' → '.join(items)}])"


# ============================================================================
# 3. TRIE - For Search Autocomplete
# ============================================================================

class Trie:
    """
    Trie (Prefix Tree) implementation for search autocomplete
    
    Used in: SearchEngine._trie (managers.py)
    Purpose: Instant autocomplete suggestions as user types
    
    Time Complexity:
    - insert(word): O(k) where k = word length
    - search(prefix): O(k + m) where m = number of matches
    
    How it works:
    1. Build Trie from service titles and tags
    2. User types "lo" → Trie finds: ['Logo', 'Logo Design']
    3. User types "pro" → Trie finds: ['Professional Website']
    4. User types "xyz" → Trie finds: [] (no match)
    
    Internal Structure:
    Tree where each node represents a character:
    
    root
    ├─ l
    │  └─ o
    │     └─ g
    │        └─ o ✓ (word: "Logo")
    │           └─ (space)
    │              └─ d
    │                 └─ e
    │                    └─ s... ✓ (word: "Logo Design")
    ├─ p
    │  └─ r
    │     └─ o... ✓ (word: "Professional")
    
    When user types "lo":
    1. Walk: root → l → o (2 steps)
    2. Collect all words below this node
    3. Return: ['Logo', 'Logo Design']
    """
    
    class _TrieNode:
        """Internal node for Trie"""
        def __init__(self):
            self.children = {}  # char → TrieNode
            self.is_end_of_word = False
            self.word = None  # Store complete word at end node
    
    def __init__(self):
        """Initialize empty Trie"""
        self.root = self._TrieNode()
        self.word_count = 0
    
    def insert(self, word):
        """
        Insert word into Trie
        
        Example:
        trie.insert("Logo")
        trie.insert("Logo Design")
        
        Steps:
        1. Start at root
        2. For each character in word:
           - If child exists → move to child
           - If not → create new child node
        3. Mark last node as end of word
        """
        if not word:
            return
        
        node = self.root
        word_lower = word.lower()
        
        for char in word_lower:
            if char not in node.children:
                node.children[char] = self._TrieNode()
            node = node.children[char]
        
        node.is_end_of_word = True
        node.word = word  # Store original word (with capitals)
        self.word_count += 1
    
    def search_prefix(self, prefix, limit=5):
        """
        Find all words starting with prefix
        
        Example:
        trie.search_prefix("lo")  → ['Logo', 'Logo Design']
        trie.search_prefix("pro") → ['Professional Website']
        
        Steps:
        1. Walk down tree following prefix characters
        2. If prefix not found → return []
        3. If found → collect all words below that node
        4. Return up to 'limit' words
        """
        if not prefix:
            return []
        
        node = self.root
        prefix_lower = prefix.lower()
        
        # Walk down to prefix node
        for char in prefix_lower:
            if char not in node.children:
                return []  # Prefix not found
            node = node.children[char]
        
        # Collect all words below this node
        results = []
        self._collect_words(node, results, limit)
        return results
    
    def _collect_words(self, node, results, limit):
        """
        Recursively collect all words from node
        
        DFS (Depth-First Search) to find all words
        """
        if len(results) >= limit:
            return
        
        if node.is_end_of_word:
            results.append(node.word)
        
        for child in node.children.values():
            self._collect_words(child, results, limit)
            if len(results) >= limit:
                return
    
    def __len__(self):
        """Return number of words in Trie"""
        return self.word_count
    
    def __repr__(self):
        """String representation"""
        return f"Trie(words={self.word_count})"


# ============================================================================
# 4. MAXHEAP - For Top-Rated Services
# ============================================================================

class MaxHeap:
    """
    MaxHeap implementation for sorting top-rated services
    
    Used in: ServiceManager.get_featured_services() (managers.py)
    Purpose: Get top 4 highest-rated services for homepage
    
    Time Complexity:
    - insert(item): O(log n)
    - extract_max(): O(log n)
    - get_max(): O(1)
    
    How it works:
    1. Insert all services with their ratings
    2. Extract top 4 → automatically sorted by rating
    3. Homepage shows: ⭐5.0, ⭐4.8, ⭐4.7, ⭐4.5
    
    Internal Structure:
    Binary tree stored as array:
    
    Array: [5.0, 4.8, 4.7, 4.5, 4.2, 4.0]
    
    Tree:
           5.0
          /   \\
        4.8   4.7
       /  \\   /
     4.5 4.2 4.0
    
    Parent-child relationship:
    - Parent at index i
    - Left child at 2*i + 1
    - Right child at 2*i + 2
    
    Max Heap Property:
    - Parent ≥ Children (always!)
    """
    
    def __init__(self):
        """Initialize empty MaxHeap"""
        self.heap = []
    
    def _parent(self, index):
        """Get parent index"""
        return (index - 1) // 2
    
    def _left_child(self, index):
        """Get left child index"""
        return 2 * index + 1
    
    def _right_child(self, index):
        """Get right child index"""
        return 2 * index + 2
    
    def _swap(self, i, j):
        """Swap two elements"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
    
    def insert(self, item):
        """
        Insert item into MaxHeap
        
        Example:
        heap.insert((4.5, service1))  # (rating, service)
        heap.insert((5.0, service2))
        heap.insert((4.8, service3))
        
        Steps:
        1. Add item to end of array
        2. Bubble up: Compare with parent
        3. If item > parent → swap and continue
        4. Stop when item ≤ parent or reach root
        """
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)
    
    def _heapify_up(self, index):
        """
        Bubble up to maintain max heap property
        
        Example:
        Insert 5.0 into [4.8, 4.5, 4.2]
        
        Step 1: [4.8, 4.5, 4.2, 5.0]  ← Add to end
        Step 2: Compare 5.0 with parent 4.5 → 5.0 > 4.5 → SWAP
        Step 3: [4.8, 5.0, 4.2, 4.5]
        Step 4: Compare 5.0 with parent 4.8 → 5.0 > 4.8 → SWAP
        Step 5: [5.0, 4.8, 4.2, 4.5]  ← Done! Max at top
        """
        parent = self._parent(index)
        
        if index > 0 and self.heap[index] > self.heap[parent]:
            self._swap(index, parent)
            self._heapify_up(parent)
    
    def extract_max(self):
        """
        Remove and return maximum item
        
        Example:
        heap = [5.0, 4.8, 4.7, 4.5]
        max_item = heap.extract_max()  → 5.0
        heap = [4.8, 4.7, 4.5]  ← Automatically re-sorted
        
        Steps:
        1. Save max (root) item
        2. Move last item to root
        3. Bubble down: Compare with children
        4. Swap with larger child if needed
        5. Continue until heap property restored
        """
        if len(self.heap) == 0:
            raise IndexError("Extract from empty heap")
        
        max_item = self.heap[0]
        last_item = self.heap.pop()
        
        if len(self.heap) > 0:
            self.heap[0] = last_item
            self._heapify_down(0)
        
        return max_item
    
    def _heapify_down(self, index):
        """
        Bubble down to maintain max heap property
        
        Example:
        After removing max, last item moves to root:
        [4.2, 4.8, 4.7, 4.5]  ← 4.2 at root (wrong!)
        
        Step 1: Compare 4.2 with children (4.8, 4.7)
        Step 2: Larger child is 4.8 → SWAP
        Step 3: [4.8, 4.2, 4.7, 4.5]
        Step 4: Compare 4.2 with children (4.5, none)
        Step 5: 4.5 > 4.2 → SWAP
        Step 6: [4.8, 4.5, 4.7, 4.2]  ← Done! Max heap restored
        """
        largest = index
        left = self._left_child(index)
        right = self._right_child(index)
        
        # Find largest among node and children
        if left < len(self.heap) and self.heap[left] > self.heap[largest]:
            largest = left
        
        if right < len(self.heap) and self.heap[right] > self.heap[largest]:
            largest = right
        
        # If largest is not current node, swap and continue
        if largest != index:
            self._swap(index, largest)
            self._heapify_down(largest)
    
    def get_max(self):
        """View maximum without removing"""
        if len(self.heap) == 0:
            raise IndexError("Peek from empty heap")
        return self.heap[0]
    
    def get_top_n(self, n):
        """
        Get top N items (sorted by rating)
        
        Example:
        heap.get_top_n(4)  → Top 4 highest-rated services
        
        Used for: Homepage featured services
        """
        result = []
        temp_heap = self.heap.copy()  # Don't modify original
        
        for _ in range(min(n, len(temp_heap))):
            if temp_heap:
                # Extract max from temp heap
                max_item = temp_heap[0]
                result.append(max_item)
                
                # Remove max and re-heapify
                last_item = temp_heap.pop()
                if temp_heap:
                    temp_heap[0] = last_item
                    self._heapify_down_temp(temp_heap, 0)
        
        return result
    
    def _heapify_down_temp(self, heap, index):
        """Heapify down for temporary heap"""
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        
        if left < len(heap) and heap[left] > heap[largest]:
            largest = left
        
        if right < len(heap) and heap[right] > heap[largest]:
            largest = right
        
        if largest != index:
            heap[index], heap[largest] = heap[largest], heap[index]
            self._heapify_down_temp(heap, largest)
    
    def __len__(self):
        """Return heap size"""
        return len(self.heap)
    
    def is_empty(self):
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def __repr__(self):
        """String representation"""
        return f"MaxHeap({self.heap})"
