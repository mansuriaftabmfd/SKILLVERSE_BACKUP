"""
Test file for custom data structures
Run this to verify all implementations work correctly
"""

from custom_data_structures import (
    CustomList, CustomDict, CustomSet, CustomQueue, CustomStack,
    LinkedList, BinarySearchTree, MinHeap, Graph
)


def test_custom_list():
    """Test CustomList implementation"""
    print("\n=== Testing CustomList ===")
    
    lst = CustomList()
    lst.append(10)
    lst.append(20)
    lst.append(30)
    
    assert len(lst) == 3, "Length should be 3"
    assert lst[0] == 10, "First element should be 10"
    assert lst[-1] == 30, "Last element should be 30"
    
    lst.insert(1, 15)
    assert lst[1] == 15, "Inserted element should be at index 1"
    
    lst.remove(15)
    assert len(lst) == 3, "Length should be 3 after removal"
    
    popped = lst.pop()
    assert popped == 30, "Popped element should be 30"
    
    print("✓ CustomList: All tests passed!")
    print(f"  Final list: {lst}")


def test_custom_dict():
    """Test CustomDict implementation"""
    print("\n=== Testing CustomDict ===")
    
    d = CustomDict()
    d['name'] = 'John'
    d['age'] = 25
    d['city'] = 'New York'
    
    assert d['name'] == 'John', "Value should be 'John'"
    assert len(d) == 3, "Length should be 3"
    assert 'age' in d, "'age' should be in dict"
    assert 'email' not in d, "'email' should not be in dict"
    
    assert d.get('name') == 'John', "get() should return 'John'"
    assert d.get('email', 'N/A') == 'N/A', "get() with default should return 'N/A'"
    
    del d['city']
    assert len(d) == 2, "Length should be 2 after deletion"
    
    print("✓ CustomDict: All tests passed!")
    print(f"  Keys: {list(d.keys())}")
    print(f"  Values: {list(d.values())}")


def test_custom_set():
    """Test CustomSet implementation"""
    print("\n=== Testing CustomSet ===")
    
    s = CustomSet()
    s.add(10)
    s.add(20)
    s.add(30)
    s.add(20)  # Duplicate
    
    assert len(s) == 3, "Length should be 3 (no duplicates)"
    assert 20 in s, "20 should be in set"
    assert 40 not in s, "40 should not be in set"
    
    s.remove(20)
    assert 20 not in s, "20 should be removed"
    
    s.discard(100)  # Should not raise error
    
    print("✓ CustomSet: All tests passed!")
    print(f"  Set elements: {list(s)}")


def test_custom_queue():
    """Test CustomQueue implementation"""
    print("\n=== Testing CustomQueue ===")
    
    q = CustomQueue()
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    
    assert len(q) == 3, "Length should be 3"
    assert q.peek() == 10, "Front should be 10"
    
    assert q.dequeue() == 10, "Dequeued should be 10"
    assert q.dequeue() == 20, "Dequeued should be 20"
    assert len(q) == 1, "Length should be 1"
    
    print("✓ CustomQueue: All tests passed!")
    print(f"  Queue: {q}")


def test_custom_stack():
    """Test CustomStack implementation"""
    print("\n=== Testing CustomStack ===")
    
    stack = CustomStack()
    stack.push(10)
    stack.push(20)
    stack.push(30)
    
    assert len(stack) == 3, "Length should be 3"
    assert stack.peek() == 30, "Top should be 30"
    
    assert stack.pop() == 30, "Popped should be 30"
    assert stack.pop() == 20, "Popped should be 20"
    assert len(stack) == 1, "Length should be 1"
    
    print("✓ CustomStack: All tests passed!")
    print(f"  Stack: {stack}")


def test_linked_list():
    """Test LinkedList implementation"""
    print("\n=== Testing LinkedList ===")
    
    ll = LinkedList()
    ll.insert_at_head(10)
    ll.insert_at_head(5)
    ll.insert_at_tail(20)
    
    assert len(ll) == 3, "Length should be 3"
    assert ll.search(10), "10 should be in list"
    assert not ll.search(100), "100 should not be in list"
    
    ll.delete(10)
    assert len(ll) == 2, "Length should be 2 after deletion"
    
    print("✓ LinkedList: All tests passed!")
    print(f"  List: {ll}")


def test_binary_search_tree():
    """Test BinarySearchTree implementation"""
    print("\n=== Testing BinarySearchTree ===")
    
    bst = BinarySearchTree()
    bst.insert(50)
    bst.insert(30)
    bst.insert(70)
    bst.insert(20)
    bst.insert(40)
    bst.insert(60)
    bst.insert(80)
    
    assert len(bst) == 7, "Length should be 7"
    assert bst.search(40), "40 should be in tree"
    assert not bst.search(100), "100 should not be in tree"
    assert 60 in bst, "60 should be in tree"
    
    inorder = bst.inorder_traversal()
    expected = [20, 30, 40, 50, 60, 70, 80]
    assert list(inorder) == expected, "Inorder should be sorted"
    
    print("✓ BinarySearchTree: All tests passed!")
    print(f"  Inorder traversal: {list(inorder)}")


def test_min_heap():
    """Test MinHeap implementation"""
    print("\n=== Testing MinHeap ===")
    
    heap = MinHeap()
    heap.insert(50)
    heap.insert(30)
    heap.insert(70)
    heap.insert(20)
    heap.insert(40)
    
    assert len(heap) == 5, "Length should be 5"
    assert heap.get_min() == 20, "Min should be 20"
    
    assert heap.extract_min() == 20, "Extracted min should be 20"
    assert heap.extract_min() == 30, "Extracted min should be 30"
    assert len(heap) == 3, "Length should be 3"
    
    print("✓ MinHeap: All tests passed!")
    print(f"  Remaining min: {heap.get_min()}")


def test_graph():
    """Test Graph implementation"""
    print("\n=== Testing Graph ===")
    
    # Undirected graph
    graph = Graph(directed=False)
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('C', 'D')
    
    # BFS from A
    bfs_result = graph.bfs('A')
    assert 'A' in bfs_result, "A should be in BFS result"
    assert 'D' in bfs_result, "D should be in BFS result"
    
    # DFS from A
    dfs_result = graph.dfs('A')
    assert 'A' in dfs_result, "A should be in DFS result"
    assert len(dfs_result) == 4, "DFS should visit all 4 vertices"
    
    print("✓ Graph: All tests passed!")
    print(f"  BFS from A: {list(bfs_result)}")
    print(f"  DFS from A: {list(dfs_result)}")


def test_real_world_scenario():
    """Test real-world scenario: Order management"""
    print("\n=== Testing Real-World Scenario: Order Management ===")
    
    # Use CustomDict for order data
    order = CustomDict()
    order['id'] = 1
    order['buyer_name'] = 'John Doe'
    order['service_title'] = 'Web Development'
    order['price'] = 500
    order['status'] = 'pending'
    
    # Use CustomList for order history
    order_history = CustomList()
    order_history.append(order)
    
    # Use CustomSet for valid statuses
    valid_statuses = CustomSet(['pending', 'in_progress', 'completed', 'cancelled'])
    
    assert order['status'] in valid_statuses, "Status should be valid"
    
    # Use CustomQueue for message queue
    message_queue = CustomQueue()
    message_queue.enqueue({'from': 'buyer', 'text': 'Hello'})
    message_queue.enqueue({'from': 'seller', 'text': 'Hi there'})
    
    first_message = message_queue.dequeue()
    assert first_message['from'] == 'buyer', "First message should be from buyer"
    
    # Use MinHeap for priority orders
    priority_queue = MinHeap()
    priority_queue.insert((1, 'Urgent order'))
    priority_queue.insert((5, 'Normal order'))
    priority_queue.insert((3, 'Medium order'))
    
    priority, urgent_order = priority_queue.extract_min()
    assert priority == 1, "Highest priority should be 1"
    assert urgent_order == 'Urgent order', "Should get urgent order first"
    
    print("✓ Real-World Scenario: All tests passed!")
    print(f"  Order: {dict((k, order[k]) for k in order)}")
    print(f"  Order history length: {len(order_history)}")
    print(f"  Valid statuses: {list(valid_statuses)}")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("CUSTOM DATA STRUCTURES TEST SUITE")
    print("=" * 60)
    
    try:
        test_custom_list()
        test_custom_dict()
        test_custom_set()
        test_custom_queue()
        test_custom_stack()
        test_linked_list()
        test_binary_search_tree()
        test_min_heap()
        test_graph()
        test_real_world_scenario()
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED SUCCESSFULLY!")
        print("=" * 60)
        print("\nYour custom data structures are working perfectly!")
        print("You can now use them in your SkillVerse application.")
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == '__main__':
    run_all_tests()
