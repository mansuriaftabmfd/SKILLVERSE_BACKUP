"""
Integration Examples: How to use custom data structures in SkillVerse
This file shows specific examples of where and how to integrate custom structures
"""

from custom_data_structures import (
    CustomList, CustomDict, CustomSet, CustomQueue, CustomStack,
    LinkedList, BinarySearchTree, MinHeap, Graph
)


# ============================================================================
# EXAMPLE 1: managers.py - ServiceManager
# ============================================================================

class ServiceManagerExample:
    """Example of using custom structures in ServiceManager"""
    
    def search_services(self, query, filters):
        """
        Search services with filters
        BEFORE: results = []
        AFTER: results = CustomList()
        """
        results = CustomList()  # ← Custom structure
        
        # Simulate database query
        all_services = self._get_all_services()
        
        for service in all_services:
            if self._matches_filters(service, filters):
                results.append(service)
        
        return results
    
    def _matches_filters(self, service, filters):
        """
        Check if service matches filters
        BEFORE: filters = {}
        AFTER: filters = CustomDict()
        """
        # filters is now CustomDict
        if 'category_id' in filters:
            if service['category_id'] != filters['category_id']:
                return False
        
        if 'min_price' in filters:
            if service['price'] < filters['min_price']:
                return False
        
        return True
    
    def _get_all_services(self):
        """Mock method - returns list of services"""
        return [
            {'id': 1, 'title': 'Service 1', 'category_id': 1, 'price': 100},
            {'id': 2, 'title': 'Service 2', 'category_id': 2, 'price': 200},
        ]


# ============================================================================
# EXAMPLE 2: routes.py - Statistics Dashboard
# ============================================================================

def index_route_example():
    """
    Example of using CustomDict for stats
    BEFORE: stats_data = {}
    AFTER: stats_data = CustomDict()
    """
    stats_data = CustomDict()  # ← Custom structure
    
    # Simulate database queries
    stats_data['total_users'] = 150
    stats_data['total_services'] = 75
    stats_data['total_orders'] = 200
    stats_data['satisfaction_rate'] = 95
    
    # Can still use like regular dict
    print(f"Total users: {stats_data['total_users']}")
    print(f"Keys: {list(stats_data.keys())}")
    
    return stats_data


# ============================================================================
# EXAMPLE 3: Order Status Validation
# ============================================================================

def validate_order_status_example(order_status):
    """
    Example of using CustomSet for validation
    BEFORE: valid_statuses = {'pending', 'in_progress', 'completed', 'cancelled'}
    AFTER: valid_statuses = CustomSet([...])
    """
    valid_statuses = CustomSet(['pending', 'in_progress', 'completed', 'cancelled'])
    
    if order_status in valid_statuses:
        print(f"✓ Status '{order_status}' is valid")
        return True
    else:
        print(f"✗ Status '{order_status}' is invalid")
        return False


# ============================================================================
# EXAMPLE 4: Chat Message Queue
# ============================================================================

class ChatManagerExample:
    """Example of using CustomQueue for chat messages"""
    
    def __init__(self):
        """
        BEFORE: self.message_queue = []
        AFTER: self.message_queue = CustomQueue()
        """
        self.message_queue = CustomQueue()  # ← FIFO queue
    
    def add_message(self, sender_id, content):
        """Add message to queue"""
        message = {
            'sender_id': sender_id,
            'content': content,
            'timestamp': 'now'
        }
        self.message_queue.enqueue(message)
        print(f"✓ Message queued: {content}")
    
    def process_messages(self):
        """Process messages in FIFO order"""
        processed = CustomList()
        
        while not self.message_queue.is_empty():
            message = self.message_queue.dequeue()
            print(f"Processing: {message['content']}")
            processed.append(message)
        
        return processed


# ============================================================================
# EXAMPLE 5: Undo Stack for Order Edits
# ============================================================================

class OrderEditorExample:
    """Example of using CustomStack for undo functionality"""
    
    def __init__(self):
        """
        BEFORE: self.undo_stack = []
        AFTER: self.undo_stack = CustomStack()
        """
        self.undo_stack = CustomStack()  # ← LIFO stack
        self.current_order = None
    
    def edit_order(self, new_data):
        """Edit order and save previous state"""
        # Save current state before editing
        if self.current_order:
            self.undo_stack.push(self.current_order.copy())
        
        # Apply edit
        self.current_order = new_data
        print(f"✓ Order edited: {new_data}")
    
    def undo(self):
        """Undo last edit"""
        if not self.undo_stack.is_empty():
            self.current_order = self.undo_stack.pop()
            print(f"✓ Undo successful: {self.current_order}")
            return True
        else:
            print("✗ Nothing to undo")
            return False


# ============================================================================
# EXAMPLE 6: Notification List
# ============================================================================

class NotificationManagerExample:
    """Example of using LinkedList for notifications"""
    
    def __init__(self):
        """
        BEFORE: self.notifications = []
        AFTER: self.notifications = LinkedList()
        """
        self.notifications = LinkedList()  # ← Linked list
    
    def add_notification(self, title, message):
        """Add notification at head (most recent first)"""
        notification = {
            'title': title,
            'message': message,
            'read': False
        }
        self.notifications.insert_at_head(notification)
        print(f"✓ Notification added: {title}")
    
    def get_all_notifications(self):
        """Get all notifications"""
        result = CustomList()
        for notif in self.notifications:
            result.append(notif)
        return result


# ============================================================================
# EXAMPLE 7: Price-Sorted Services (BST)
# ============================================================================

class ServicePricingExample:
    """Example of using BinarySearchTree for sorted prices"""
    
    def __init__(self):
        """
        Use BST to maintain sorted prices
        """
        self.price_tree = BinarySearchTree()
    
    def add_service(self, service_id, price):
        """Add service price to tree"""
        self.price_tree.insert((price, service_id))
        print(f"✓ Service {service_id} added with price ${price}")
    
    def get_sorted_prices(self):
        """Get all prices in sorted order"""
        sorted_items = self.price_tree.inorder_traversal()
        return sorted_items
    
    def find_service_by_price(self, price):
        """Check if service with price exists"""
        return price in self.price_tree


# ============================================================================
# EXAMPLE 8: Priority Order Processing (MinHeap)
# ============================================================================

class OrderProcessorExample:
    """Example of using MinHeap for priority processing"""
    
    def __init__(self):
        """
        Use MinHeap for priority queue
        Lower priority number = higher urgency
        """
        self.priority_queue = MinHeap()
    
    def add_order(self, order_id, priority):
        """
        Add order with priority
        Priority: 1 = Urgent, 5 = Normal, 10 = Low
        """
        self.priority_queue.insert((priority, order_id))
        print(f"✓ Order {order_id} added with priority {priority}")
    
    def process_next_order(self):
        """Process highest priority order"""
        if not self.priority_queue.is_empty():
            priority, order_id = self.priority_queue.extract_min()
            print(f"✓ Processing order {order_id} (priority: {priority})")
            return order_id
        else:
            print("✗ No orders to process")
            return None


# ============================================================================
# EXAMPLE 9: User Network (Graph)
# ============================================================================

class UserNetworkExample:
    """Example of using Graph for user connections"""
    
    def __init__(self):
        """
        Use Graph to track user relationships
        """
        self.network = Graph(directed=False)
    
    def add_connection(self, user1, user2):
        """Add connection between users (they worked together)"""
        self.network.add_edge(user1, user2)
        print(f"✓ Connected: {user1} ↔ {user2}")
    
    def find_connections(self, user):
        """Find all users connected to given user (BFS)"""
        connections = self.network.bfs(user)
        print(f"✓ {user}'s network: {list(connections)}")
        return connections
    
    def recommend_users(self, user):
        """Recommend users based on network (friends of friends)"""
        # Get direct connections
        direct = self.network.get_neighbors(user)
        
        # Get friends of friends
        recommendations = CustomSet()
        for friend, _ in direct:
            for friend_of_friend, _ in self.network.get_neighbors(friend):
                if friend_of_friend != user:
                    recommendations.add(friend_of_friend)
        
        return recommendations


# ============================================================================
# DEMO: Run all examples
# ============================================================================

def run_all_examples():
    """Run all integration examples"""
    print("=" * 70)
    print("CUSTOM DATA STRUCTURES - INTEGRATION EXAMPLES")
    print("=" * 70)
    
    # Example 1: ServiceManager
    print("\n1. ServiceManager - Search with CustomList")
    print("-" * 70)
    manager = ServiceManagerExample()
    filters = CustomDict()
    filters['category_id'] = 1
    results = manager.search_services("query", filters)
    print(f"Found {len(results)} services")
    
    # Example 2: Stats Dashboard
    print("\n2. Dashboard Stats - CustomDict")
    print("-" * 70)
    stats = index_route_example()
    
    # Example 3: Status Validation
    print("\n3. Order Status Validation - CustomSet")
    print("-" * 70)
    validate_order_status_example('pending')
    validate_order_status_example('invalid_status')
    
    # Example 4: Chat Queue
    print("\n4. Chat Messages - CustomQueue (FIFO)")
    print("-" * 70)
    chat = ChatManagerExample()
    chat.add_message(1, "Hello")
    chat.add_message(2, "Hi there")
    chat.add_message(1, "How are you?")
    chat.process_messages()
    
    # Example 5: Undo Stack
    print("\n5. Order Editor - CustomStack (LIFO)")
    print("-" * 70)
    editor = OrderEditorExample()
    editor.edit_order({'id': 1, 'status': 'pending'})
    editor.edit_order({'id': 1, 'status': 'in_progress'})
    editor.edit_order({'id': 1, 'status': 'completed'})
    editor.undo()
    editor.undo()
    
    # Example 6: Notifications
    print("\n6. Notifications - LinkedList")
    print("-" * 70)
    notif_mgr = NotificationManagerExample()
    notif_mgr.add_notification("New Order", "You have a new order")
    notif_mgr.add_notification("Payment", "Payment received")
    notifications = notif_mgr.get_all_notifications()
    print(f"Total notifications: {len(notifications)}")
    
    # Example 7: Price Sorting
    print("\n7. Service Pricing - BinarySearchTree")
    print("-" * 70)
    pricing = ServicePricingExample()
    pricing.add_service(1, 100)
    pricing.add_service(2, 50)
    pricing.add_service(3, 150)
    pricing.add_service(4, 75)
    sorted_prices = pricing.get_sorted_prices()
    print(f"Sorted prices: {list(sorted_prices)}")
    
    # Example 8: Priority Processing
    print("\n8. Order Processing - MinHeap (Priority Queue)")
    print("-" * 70)
    processor = OrderProcessorExample()
    processor.add_order(101, 5)  # Normal
    processor.add_order(102, 1)  # Urgent
    processor.add_order(103, 3)  # Medium
    processor.add_order(104, 10) # Low
    print("\nProcessing orders by priority:")
    for _ in range(4):
        processor.process_next_order()
    
    # Example 9: User Network
    print("\n9. User Network - Graph")
    print("-" * 70)
    network = UserNetworkExample()
    network.add_connection('Alice', 'Bob')
    network.add_connection('Bob', 'Charlie')
    network.add_connection('Alice', 'David')
    network.add_connection('Charlie', 'Eve')
    network.find_connections('Alice')
    recommendations = network.recommend_users('Alice')
    print(f"Recommended users for Alice: {list(recommendations)}")
    
    print("\n" + "=" * 70)
    print("✓ ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("=" * 70)
    print("\nYou can now integrate these patterns into your SkillVerse code!")


if __name__ == '__main__':
    run_all_examples()
