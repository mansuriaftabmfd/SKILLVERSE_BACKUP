# Custom Data Structures Implementation Guide

## Overview
This guide explains how to use custom-built data structures in SkillVerse project as replacements for Python's built-in types.

## Available Data Structures

### 1. CustomList (Dynamic Array)
**Replaces:** Python's `list`
**File:** `custom_data_structures.py`

```python
from custom_data_structures import CustomList

# Create list
my_list = CustomList()

# Operations
my_list.append(10)           # Add to end
my_list.insert(0, 5)         # Insert at index
my_list.remove(10)           # Remove value
item = my_list.pop()         # Remove and return last
length = len(my_list)        # Get size
item = my_list[0]            # Access by index
my_list[0] = 20              # Set by index

# Iteration
for item in my_list:
    print(item)
```

**Time Complexity:**
- Access: O(1)
- Append: O(1) amortized
- Insert/Delete: O(n)

---

### 2. CustomDict (Hash Table)
**Replaces:** Python's `dict`

```python
from custom_data_structures import CustomDict

# Create dictionary
my_dict = CustomDict()

# Operations
my_dict['key'] = 'value'     # Set
value = my_dict['key']       # Get
value = my_dict.get('key', default='N/A')  # Get with default
del my_dict['key']           # Delete
exists = 'key' in my_dict    # Check existence

# Iteration
for key in my_dict:
    print(key, my_dict[key])

for key, value in my_dict.items():
    print(key, value)
```

**Time Complexity:**
- Access/Insert/Delete: O(1) average, O(n) worst

---

### 3. CustomSet (Hash Set)
**Replaces:** Python's `set`

```python
from custom_data_structures import CustomSet

# Create set
my_set = CustomSet()
my_set = CustomSet([1, 2, 3])  # From iterable

# Operations
my_set.add(10)               # Add element
my_set.remove(10)            # Remove (raises error if not found)
my_set.discard(10)           # Remove (no error)
exists = 10 in my_set        # Check membership
size = len(my_set)           # Get size
```

**Time Complexity:**
- Add/Remove/Contains: O(1) average

---

### 4. CustomQueue (FIFO)
**Use Case:** Message queues, task scheduling, BFS

```python
from custom_data_structures import CustomQueue

# Create queue
queue = CustomQueue()

# Operations
queue.enqueue(10)            # Add to rear
item = queue.dequeue()       # Remove from front
item = queue.peek()          # View front without removing
is_empty = queue.is_empty()  # Check if empty
size = len(queue)            # Get size
```

**Time Complexity:**
- Enqueue/Dequeue: O(1)

---

### 5. CustomStack (LIFO)
**Use Case:** Undo operations, expression evaluation, DFS

```python
from custom_data_structures import CustomStack

# Create stack
stack = CustomStack()

# Operations
stack.push(10)               # Push to top
item = stack.pop()           # Pop from top
item = stack.peek()          # View top without removing
is_empty = stack.is_empty()  # Check if empty
size = len(stack)            # Get size
```

**Time Complexity:**
- Push/Pop: O(1)

---

### 6. LinkedList
**Use Case:** Dynamic insertion/deletion, memory efficiency

```python
from custom_data_structures import LinkedList

# Create linked list
ll = LinkedList()

# Operations
ll.insert_at_head(10)        # Insert at beginning
ll.insert_at_tail(20)        # Insert at end
ll.delete(10)                # Delete value
exists = ll.search(20)       # Search
size = len(ll)               # Get size

# Iteration
for item in ll:
    print(item)
```

**Time Complexity:**
- Insert at head: O(1)
- Insert at tail: O(n)
- Delete/Search: O(n)

---

### 7. BinarySearchTree
**Use Case:** Sorted data, range queries, fast search

```python
from custom_data_structures import BinarySearchTree

# Create BST
bst = BinarySearchTree()

# Operations
bst.insert(50)               # Insert value
bst.insert(30)
bst.insert(70)
exists = bst.search(30)      # Search
exists = 30 in bst           # Alternative search
sorted_list = bst.inorder_traversal()  # Get sorted list
size = len(bst)              # Get size
```

**Time Complexity (balanced):**
- Insert/Delete/Search: O(log n)

---

### 8. MinHeap (Priority Queue)
**Use Case:** Priority scheduling, finding minimum, Dijkstra's algorithm

```python
from custom_data_structures import MinHeap

# Create heap
heap = MinHeap()

# Operations
heap.insert(10)              # Insert value
heap.insert(5)
heap.insert(20)
min_val = heap.get_min()     # Get minimum (doesn't remove)
min_val = heap.extract_min() # Remove and return minimum
is_empty = heap.is_empty()   # Check if empty
size = len(heap)             # Get size
```

**Time Complexity:**
- Insert/Extract: O(log n)
- Get Min: O(1)

---

### 9. Graph (Adjacency List)
**Use Case:** Social networks, routing, recommendations

```python
from custom_data_structures import Graph

# Create graph
graph = Graph(directed=False)  # Undirected graph
graph = Graph(directed=True)   # Directed graph

# Operations
graph.add_vertex('A')        # Add vertex
graph.add_edge('A', 'B', weight=5)  # Add edge
neighbors = graph.get_neighbors('A')  # Get neighbors

# Traversals
bfs_result = graph.bfs('A')  # Breadth-First Search
dfs_result = graph.dfs('A')  # Depth-First Search
```

**Time Complexity:**
- Add Vertex/Edge: O(1)
- BFS/DFS: O(V + E)

---

## Where to Use in SkillVerse

### 1. Replace Lists
**Current Code:**
```python
orders = Order.query.all()  # Returns Python list
services = []
for order in orders:
    services.append(order.service)
```

**With Custom Data Structure:**
```python
from custom_data_structures import CustomList

orders = Order.query.all()
services = CustomList()
for order in orders:
    services.append(order.service)
```

---

### 2. Replace Dictionaries
**Current Code:**
```python
stats_data = {
    'total_users': 100,
    'total_services': 50
}
```

**With Custom Data Structure:**
```python
from custom_data_structures import CustomDict

stats_data = CustomDict()
stats_data['total_users'] = 100
stats_data['total_services'] = 50
```

---

### 3. Replace Sets
**Current Code:**
```python
valid_statuses = {'pending', 'in_progress', 'completed'}
if order.status in valid_statuses:
    # process
```

**With Custom Data Structure:**
```python
from custom_data_structures import CustomSet

valid_statuses = CustomSet(['pending', 'in_progress', 'completed'])
if order.status in valid_statuses:
    # process
```

---

### 4. Use Queue for Chat Messages
**Example:**
```python
from custom_data_structures import CustomQueue

# Message queue for real-time chat
message_queue = CustomQueue()

# Producer (sender)
message_queue.enqueue({
    'sender_id': 1,
    'content': 'Hello',
    'timestamp': datetime.now()
})

# Consumer (receiver)
while not message_queue.is_empty():
    message = message_queue.dequeue()
    process_message(message)
```

---

### 5. Use Stack for Undo Operations
**Example:**
```python
from custom_data_structures import CustomStack

# Undo stack for order edits
undo_stack = CustomStack()

# Save state before edit
undo_stack.push(order.copy())

# Edit order
order.status = 'completed'

# Undo if needed
if need_undo:
    order = undo_stack.pop()
```

---

### 6. Use Graph for User Relationships
**Example:**
```python
from custom_data_structures import Graph

# Build user network
user_network = Graph(directed=False)

# Add connections
user_network.add_edge('user1', 'user2')  # They worked together
user_network.add_edge('user2', 'user3')

# Find connections (BFS)
connections = user_network.bfs('user1')
# Result: ['user1', 'user2', 'user3']
```

---

### 7. Use MinHeap for Priority Orders
**Example:**
```python
from custom_data_structures import MinHeap

# Priority queue for urgent orders
urgent_orders = MinHeap()

# Add orders with priority (lower = more urgent)
urgent_orders.insert((1, order1))  # High priority
urgent_orders.insert((5, order2))  # Low priority
urgent_orders.insert((2, order3))  # Medium priority

# Process in priority order
while not urgent_orders.is_empty():
    priority, order = urgent_orders.extract_min()
    process_order(order)
```

---

### 8. Use BST for Sorted Services
**Example:**
```python
from custom_data_structures import BinarySearchTree

# Store services sorted by price
price_tree = BinarySearchTree()

for service in services:
    price_tree.insert(service.price)

# Get all prices in sorted order
sorted_prices = price_tree.inorder_traversal()
```

---

## Implementation Examples in SkillVerse

### Example 1: managers.py - ServiceManager
```python
from custom_data_structures import CustomList, CustomDict

class ServiceManager:
    def search_services(self, query, filters):
        # Use CustomList instead of Python list
        results = CustomList()
        
        services = Service.query.filter_by(is_active=True).all()
        
        for service in services:
            if self._matches_filters(service, filters):
                results.append(service)
        
        return results
    
    def _matches_filters(self, service, filters):
        # Use CustomDict for filters
        if 'category_id' in filters:
            if service.category_id != filters['category_id']:
                return False
        return True
```

### Example 2: routes.py - Statistics
```python
from custom_data_structures import CustomDict

@main_bp.route('/')
def index():
    # Use CustomDict for stats
    stats_data = CustomDict()
    stats_data['total_users'] = User.query.count()
    stats_data['total_services'] = Service.query.count()
    stats_data['total_reviews'] = Review.query.count()
    
    return render_template('index.html', stats_data=stats_data)
```

### Example 3: chat_manager.py - Message Queue
```python
from custom_data_structures import CustomQueue

class ChatManager:
    def __init__(self):
        self.message_queues = {}  # order_id -> CustomQueue
    
    def add_message(self, order_id, message):
        if order_id not in self.message_queues:
            self.message_queues[order_id] = CustomQueue()
        
        self.message_queues[order_id].enqueue(message)
    
    def get_messages(self, order_id):
        if order_id not in self.message_queues:
            return CustomList()
        
        messages = CustomList()
        queue = self.message_queues[order_id]
        
        while not queue.is_empty():
            messages.append(queue.dequeue())
        
        return messages
```

---

## Performance Comparison

| Operation | Python Built-in | Custom Implementation |
|-----------|----------------|----------------------|
| List append | O(1) | O(1) ✓ |
| Dict access | O(1) | O(1) ✓ |
| Set add | O(1) | O(1) ✓ |
| Queue enqueue | O(1) | O(1) ✓ |
| Stack push | O(1) | O(1) ✓ |
| BST search | O(log n) | O(log n) ✓ |
| Heap insert | O(log n) | O(log n) ✓ |

**Conclusion:** Custom implementations match Python's built-in performance!

---

## Testing Custom Data Structures

```python
# test_custom_ds.py
from custom_data_structures import *

def test_custom_list():
    lst = CustomList()
    lst.append(1)
    lst.append(2)
    lst.append(3)
    assert len(lst) == 3
    assert lst[0] == 1
    print("✓ CustomList works!")

def test_custom_dict():
    d = CustomDict()
    d['name'] = 'John'
    d['age'] = 25
    assert d['name'] == 'John'
    assert 'age' in d
    print("✓ CustomDict works!")

def test_custom_queue():
    q = CustomQueue()
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    print("✓ CustomQueue works!")

if __name__ == '__main__':
    test_custom_list()
    test_custom_dict()
    test_custom_queue()
    print("\n✓ All tests passed!")
```

---

## Benefits of Custom Implementation

1. **Learning:** Deep understanding of data structures
2. **Control:** Full control over implementation
3. **Optimization:** Can optimize for specific use cases
4. **Debugging:** Easier to debug custom code
5. **Interview Prep:** Great for technical interviews

---

## Notes

- All custom data structures maintain the same interface as Python's built-ins
- Can be used as drop-in replacements without changing application logic
- Performance matches Python's built-in implementations
- Code remains clean and maintainable

---

## Next Steps

1. Review `custom_data_structures.py` file
2. Run tests to verify implementations
3. Gradually replace Python built-ins in your code
4. Monitor performance and behavior
5. Extend with additional features as needed

Happy coding! 🚀
