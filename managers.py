"""
Business Logic Managers for SkillVerse Application

This module demonstrates:
1. OOP Concepts: Classes, Encapsulation, Abstraction
2. Data Structures: Dictionary, Heap, Trie, Set, Queue
3. Algorithms: Search, Sorting, Filtering

These manager classes handle business logic separately from routes (MVC pattern)

SCRATCH DATA STRUCTURES USED:
1. HashMap - Caching featured services (O(1) lookup)
2. Queue - FIFO order processing (O(1) enqueue/dequeue)
3. Trie - Search autocomplete (O(k) prefix search)
4. MaxHeap - Top-rated services sorting (O(log n) operations)

Author: SkillVerse Team
Purpose: Centralized business logic with data structure demonstrations
"""

import heapq
import random
from collections import defaultdict, deque
from datetime import datetime, timedelta
from models import db, Service, User, Category, Review, Order, Favorite, Notification, Message
from sqlalchemy.orm import joinedload

from flask import current_app

# Import scratch data structures (Production implementations)
from custom_data_structures import HashMap, Queue, Trie, MaxHeap

class ServiceManager:
    """
    Service Manager Class - Handles all service-related operations
    
    OOP Concepts:
    - ENCAPSULATION: Internal caching mechanism
    - ABSTRACTION: Simple interface for complex operations
    - SINGLETON PATTERN: Single instance manages all services
    
    Data Structures Used:
    - HASHMAP: For caching - O(1) lookup time (Line ~45)
    - MAXHEAP: For efficient top-N selection (Line ~60)
    - TRIE: For autocomplete (initialized in SearchEngine)
    """
    
    def __init__(self):
        """
        Initialize ServiceManager with HashMap cache
        
        Data Structure: HASHMAP (Scratch Implementation)
        Location: Line ~45
        Purpose: Cache featured services to avoid repeated DB queries
        
        How it works:
        1. User visits homepage → DB query → store in cache
        2. User visits AGAIN → cache hit → instant return!
        3. Admin approves service → cache.clear() → fresh data
        
        Performance: O(1) lookup vs O(n) database query
        """
        self._cache = HashMap(capacity=16)  # 16 buckets for hash table
        self._cache_timeout = 300  # Cache timeout in seconds (5 minutes)

    def get_featured_services(self, limit=4):
        """
        Get top-rated featured services using MAXHEAP data structure
        
        Data Structure: MAXHEAP (Scratch Implementation)
        Location: Line ~60
        Purpose: Efficiently get top N highest-rated services
        
        Algorithm:
        1. Check HashMap cache first (O(1))
        2. If cache miss → Query database
        3. Insert all services into MaxHeap with ratings
        4. Extract top 4 services (automatically sorted)
        5. Store in HashMap cache for next time
        
        Time Complexity: O(n log n) for heap operations
        Space Complexity: O(n) for heap storage
        
        Example Flow:
        User visits homepage →
          Check cache['featured_services_4'] →
            Cache HIT? → Return instantly! ✅
            Cache MISS? → DB query → MaxHeap sort → Cache → Return
        
        Args:
            limit (int): Number of services to return (default 4)
            
        Returns:
            list: Top-rated Service objects
        """
        # Check HashMap cache first
        cache_key = f'featured_services_{limit}'
        cached_data = self._cache.get(cache_key)
        
        if cached_data is not None:
            cached_services, timestamp = cached_data
            # Check if cache is still valid (within timeout)
            if (datetime.now() - timestamp).seconds < self._cache_timeout:
                print(f"✅ CACHE HIT: Returning {limit} services from HashMap cache")
                return cached_services
        
        print(f"❌ CACHE MISS: Querying database and building MaxHeap")
        
        # Get all active AND approved services with eager loading
        services = Service.query.options(
            joinedload(Service.category),
            joinedload(Service.provider)
        ).filter_by(is_active=True, is_approved=True).all()
        
        # Use MaxHeap to get top N services by rating
        # MaxHeap automatically keeps highest ratings at top
        heap = MaxHeap()
        
        for service in services:
            rating = service.get_average_rating()
            review_count = service.get_review_count()
            # Insert tuple: (rating, review_count, service)
            # MaxHeap will sort by first element (rating)
            heap.insert((rating, review_count, service))
        
        # Extract top N services from MaxHeap
        featured = []
        for _ in range(min(limit, len(heap))):
            if not heap.is_empty():
                rating, review_count, service = heap.extract_max()
                featured.append(service)
                print(f"  → Service: {service.title} | Rating: {rating} | Reviews: {review_count}")
        
        # Store in HashMap cache with timestamp
        self._cache.set(cache_key, (featured, datetime.now()))
        print(f"✅ Cached {len(featured)} services in HashMap")
        
        return featured
    
    def search_services(self, query, filters=None):
        """
        Search services with advanced filtering
        
        Algorithm:
        1. Tokenize search query
        2. Search in title, description, and tags
        3. Apply filters (category, price range, etc.)
        4. Rank results by relevance
        
        Args:
            query (str): Search query
            filters (dict): Optional filters (category_id, min_price, max_price, etc.)
            
        Returns:
            list: Matching Service objects sorted by relevance
        """
        if not query and not filters:
            return []
        
        # Start with all active and approved services
        results = Service.query.filter_by(is_active=True, is_approved=True)
        
        # Apply text search if query provided
        if query:
            search_term = f'%{query.lower()}%'
            results = results.filter(
                db.or_(
                    Service.title.ilike(search_term),
                    Service.description.ilike(search_term),
                    Service.tags.ilike(search_term)
                )
            )
        
        # Apply filters if provided
        if filters:
            if 'category_id' in filters and filters['category_id']:
                results = results.filter_by(category_id=filters['category_id'])
            
            if 'min_price' in filters and filters['min_price']:
                results = results.filter(Service.price >= filters['min_price'])
            
            if 'max_price' in filters and filters['max_price']:
                results = results.filter(Service.price <= filters['max_price'])
        
        # Get all results
        services = results.all()
        
        # Rank by relevance (simple scoring algorithm)
        if query:
            scored_services = []
            query_lower = query.lower()
            
            for service in services:
                score = 0
                # Title match gets highest score
                if query_lower in service.title.lower():
                    score += 10
                # Tag match gets medium score
                if service.tags and query_lower in service.tags.lower():
                    score += 5
                # Description match gets lower score
                if query_lower in service.description.lower():
                    score += 2
                # Boost by rating
                score += service.get_average_rating()
                
                scored_services.append((score, service))
            
            # Sort by score (highest first)
            scored_services.sort(reverse=True, key=lambda x: x[0])
            return [service for score, service in scored_services]
        
        return services
    
    def get_recommendations(self, user, limit=6):
        """
        Get personalized service recommendations for user
        
        Algorithm:
        1. Get user's favorite categories
        2. Get user's order history
        3. Find similar services
        4. Rank by relevance
        
        Args:
            user (User): User object
            limit (int): Number of recommendations
            
        Returns:
            list: Recommended Service objects
        """
        if not user or not user.is_authenticated:
            # Return popular services for non-authenticated users
            return self.get_featured_services(limit)
        
        # Get categories from user's favorites and orders
        favorite_categories = set()
        
        # From favorites
        favorites = Favorite.query.filter_by(user_id=user.id).all()
        for fav in favorites:
            if fav.service.category_id:
                favorite_categories.add(fav.service.category_id)
        
        # From orders
        orders = Order.query.filter_by(buyer_id=user.id).all()
        for order in orders:
            if order.service.category_id:
                favorite_categories.add(order.service.category_id)
        
        # Get services from favorite categories
        if favorite_categories:
            recommendations = Service.query.filter(
                Service.category_id.in_(favorite_categories),
                Service.is_active == True,
                Service.is_approved == True
            ).limit(limit * 2).all()
            
            # Sort by rating and return top N
            recommendations.sort(
                key=lambda s: s.get_average_rating(),
                reverse=True
            )
            return recommendations[:limit]
        
        # Fallback to featured services
        return self.get_featured_services(limit)
    
    def get_all_tags(self):
        """
        Get all unique tags from services
        
        Data Structure: SET for unique values
        
        Returns:
            list: Sorted list of unique tags
        """
        # Use SET to store unique tags
        all_tags = set()
        
        services = Service.query.filter_by(is_active=True).all()
        for service in services:
            if service.tags:
                tags = service.get_tags_list()
                all_tags.update(tags)
        
        # Return sorted list
        return sorted(all_tags)
    
    def filter_by_category(self, category_id):
        """
        Get all services in a category
        
        Args:
            category_id (int): Category ID
            
        Returns:
            list: Service objects in category
        """
        return Service.query.filter_by(
            category_id=category_id,
            is_active=True
        ).all()
    
    def create_service(self, user_id, data):
        """
        Create a new service
        
        Args:
            user_id (int): Provider user ID
            data (dict): Service data
            
        Returns:
            Service: Created service object
        """
        # Handle default images if not provided
        image_url = data.get('image_url')
        if not image_url or image_url == 'default-service.jpg' or image_url.strip() == '':
            # List of high-quality default images from Unsplash
            default_images = [
                'https://images.unsplash.com/photo-1498050108023-c5249f4df085?w=500&q=80', # Coding
                'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?w=500&q=80', # Analysis
                'https://images.unsplash.com/photo-1558655146-d09347e0b7a9?w=500&q=80', # Marketing
                'https://images.unsplash.com/photo-1561070791-2526d30994b5?w=500&q=80', # Design
                'https://images.unsplash.com/photo-1553877607-3fa983197609?w=500&q=80', # Discussion
                'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=500&q=80', # Analytics
                'https://images.unsplash.com/photo-1552664730-d307ca884978?w=500&q=80'  # Team
            ]
            image_url = random.choice(default_images)
        
        # Check if the creator is admin — auto-approve admin-created services
        creator = User.query.get(user_id)
        auto_approve = creator and creator.is_admin()
        
        service = Service(
            user_id=user_id,
            title=data['title'],
            description=data['description'],
            price=data['price'],
            delivery_time=data.get('delivery_time', ''),
            category_id=data['category_id'],
            tags=data.get('tags', ''),
            image_url=image_url,
            is_approved=auto_approve
        )
        
        db.session.add(service)
        db.session.commit()
        
        # Clear cache
        self._cache.clear()
        
        # Notify all admins about the new service pending approval
        if not auto_approve:
            admins = User.query.filter_by(user_type='admin').all()
            for admin in admins:
                notification_manager.create_notification(
                    user_id=admin.id,
                    title='New Service Pending Approval 📋',
                    message=f'{creator.username} submitted "{data["title"]}" for review.',
                    link='/admin/services/pending'
                )
        
        return service

    def approve_service(self, service_id):
        """
        Approve a service (Admin only)
        
        IMPORTANT: Clear HashMap cache and rebuild Trie after approval
        
        Args:
            service_id (int): Service ID
            
        Returns:
            Service: Approved service object or None
        """
        service = Service.query.get(service_id)
        if not service:
            return None
        
        service.is_approved = True
        service.rejection_reason = None
        db.session.commit()
        
        # Clear HashMap cache so new service appears in featured list
        self._cache.clear()
        print(f"✅ HashMap cache cleared after approving service #{service_id}")
        
        # Rebuild Trie so new service appears in autocomplete
        search_engine.rebuild_trie()
        print(f"✅ Trie rebuilt after approving service #{service_id}")
        
        # Notify the provider
        notification_manager.create_notification(
            user_id=service.user_id,
            title='Service Approved! ✅',
            message=f'Your service "{service.title}" has been approved and is now live on SkillVerse.',
            link=f'/service/{service.id}'
        )
        
        return service

    def reject_service(self, service_id, reason=''):
        """
        Reject a service (Admin only)
        
        Args:
            service_id (int): Service ID
            reason (str): Rejection reason
            
        Returns:
            Service: Rejected service object or None
        """
        service = Service.query.get(service_id)
        if not service:
            return None
        
        service.is_approved = False
        service.rejection_reason = reason or 'Service does not meet community guidelines.'
        db.session.commit()
        
        # Clear cache
        self._cache.clear()
        
        # Notify the provider
        notification_manager.create_notification(
            user_id=service.user_id,
            title='Service Rejected ❌',
            message=f'Your service "{service.title}" was not approved. Reason: {service.rejection_reason}',
            link=f'/service/{service.id}'
        )
        
        return service

    def get_pending_services(self):
        """
        Get all services pending approval
        
        Returns:
            list: List of Service objects awaiting approval
        """
        return Service.query.filter_by(
            is_active=True, is_approved=False
        ).filter(
            Service.rejection_reason.is_(None)
        ).order_by(Service.created_at.desc()).all()

    def get_pending_count(self):
        """
        Get count of services pending approval
        
        Returns:
            int: Number of pending services
        """
        return Service.query.filter_by(
            is_active=True, is_approved=False
        ).filter(
            Service.rejection_reason.is_(None)
        ).count()


class UserManager:
    """
    User Manager Class - Handles user operations
    
    OOP Concepts:
    - ENCAPSULATION: User authentication logic
    - ABSTRACTION: Simple interface for user management
    """
    
    def authenticate(self, email, password):
        """
        Authenticate user with email and password
        
        Args:
            email (str): User email
            password (str): Plain text password
            
        Returns:
            User: User object if authenticated, None otherwise
        """
        if email:
            email = email.lower().strip()
            
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            return user
        
        return None
    
    def create_user(self, data):
        """
        Create new user with validation
        
        Args:
            data (dict): User data (username, email, password, user_type)
            
        Returns:
            tuple: (User object or None, error message or None)
        """
        # Normalize email
        if 'email' in data:
            data['email'] = data['email'].lower().strip()
            
        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return None, "Email already registered"
        
        # Check if username already exists
        if User.query.filter_by(username=data['username']).first():
            return None, "Username already taken"
        
        # Set default avatar if not provided
        # Use UI Avatars API for consistent, nice default avatars
        username = data['username']
        default_avatar = f"https://ui-avatars.com/api/?name={username}&background=random&color=fff"
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            user_type=data.get('user_type', 'client'),
            full_name=data.get('full_name', ''),
            avatar_url=default_avatar
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Send welcome notification (placeholder call)
        # In a real app, we would use NotificationManager here
        
        return user, None
    
    def get_user_stats(self, user_id):
        """
        Calculate user statistics
        
        Returns:
            dict: User statistics
        """
        user = User.query.get(user_id)
        if not user:
            return {}
        
        stats = {
            'total_services': user.services.filter_by(is_active=True).count(),
            'total_reviews': user.get_total_reviews(),
            'average_rating': user.get_average_rating(),
            'total_orders_as_seller': user.orders_as_seller.count(),
            'total_orders_as_buyer': user.orders_as_buyer.count(),
            'completed_projects': user.orders_as_seller.filter_by(status='completed').count(),
            'member_since': user.created_at.strftime('%B %Y')
        }
        
        return stats


class SearchEngine:
    """
    Advanced Search Engine with Autocomplete
    
    Data Structures:
    - TRIE: For efficient autocomplete (O(k) prefix search)
    - HASHMAP: For caching search results
    """
    
    def __init__(self):
        """
        Initialize search engine with Trie and HashMap
        
        Data Structure 1: TRIE (Scratch Implementation)
        Location: Line ~535
        Purpose: Instant autocomplete as user types
        
        Data Structure 2: HASHMAP (Scratch Implementation)
        Purpose: Cache autocomplete results
        
        How Trie works:
        1. Build Trie from all service titles and tags
        2. User types "lo" → Trie walks: root → l → o
        3. Collect all words below "lo" node
        4. Return: ['Logo', 'Logo Design']
        
        Performance: O(k) where k = prefix length
        """
        self._trie = Trie()  # Trie for autocomplete
        self.suggestions_cache = HashMap(capacity=16)  # HashMap for caching
        self._trie_built = False  # Flag to track if Trie is built
    
    def _build_trie(self):
        """
        Build Trie from all service titles and tags
        
        Called once when first autocomplete request comes
        
        Steps:
        1. Query all active services
        2. Insert each title into Trie
        3. Insert each tag into Trie
        4. Set _trie_built = True
        
        Example:
        Service 1: "Logo Design" with tags "logo, design, branding"
        Service 2: "Professional Website" with tags "web, development"
        
        Trie will contain:
        - Logo, Logo Design, logo, design, branding
        - Professional, Professional Website, web, development
        """
        if self._trie_built:
            return
        
        print("🔨 Building Trie from service titles and tags...")
        
        services = Service.query.filter_by(is_active=True, is_approved=True).all()
        word_count = 0
        
        for service in services:
            # Insert service title
            if service.title:
                self._trie.insert(service.title)
                word_count += 1
            
            # Insert tags
            if service.tags:
                tags = service.get_tags_list()
                for tag in tags:
                    if tag.strip():
                        self._trie.insert(tag.strip())
                        word_count += 1
        
        self._trie_built = True
        print(f"✅ Trie built with {word_count} words from {len(services)} services")
    
    def rebuild_trie(self):
        """
        Rebuild Trie (called when new service is added)
        
        Used when: Admin approves new service
        """
        self._trie = Trie()
        self._trie_built = False
        self.suggestions_cache.clear()
        self._build_trie()
    
    def get_autocomplete_suggestions(self, query, limit=5):
        """
        Get autocomplete suggestions using TRIE data structure
        
        Data Structure: TRIE (Scratch Implementation)
        Location: Line ~600
        Purpose: Instant prefix-based search
        
        Algorithm:
        1. Check HashMap cache first
        2. If cache miss → Build Trie (if not built)
        3. Search Trie with prefix
        4. Cache results in HashMap
        5. Return suggestions
        
        Time Complexity: O(k + m)
        - k = prefix length
        - m = number of matches
        
        Example Flow:
        User types "lo" →
          Check cache['lo'] →
            Cache HIT? → Return ['Logo', 'Logo Design'] ✅
            Cache MISS? →
              Trie.search_prefix("lo") →
                Walk: root → l → o (2 steps)
                Collect words below: ['Logo', 'Logo Design']
                Cache result → Return
        
        Args:
            query (str): Partial search query (prefix)
            limit (int): Maximum suggestions
            
        Returns:
            list: Suggestion strings
        """
        if not query or len(query) < 2:
            return []
        
        # Check HashMap cache first
        cache_key = query.lower()
        cached_result = self.suggestions_cache.get(cache_key)
        
        if cached_result is not None:
            print(f"✅ CACHE HIT: Autocomplete for '{query}' from HashMap")
            return cached_result
        
        print(f"❌ CACHE MISS: Searching Trie for '{query}'")
        
        # Build Trie if not built yet
        self._build_trie()
        
        # Search Trie for prefix matches
        suggestions = self._trie.search_prefix(query, limit=limit)
        
        print(f"  → Trie found {len(suggestions)} matches: {suggestions}")
        
        # Cache the result in HashMap
        self.suggestions_cache.set(cache_key, suggestions)
        
        return suggestions
    
    def search_by_tags(self, tags):
        """
        Search services by multiple tags
        
        Args:
            tags (list): List of tag strings
            
        Returns:
            list: Matching services
        """
        if not tags:
            return []
        
        # Find services that match any of the tags
        services = []
        for tag in tags:
            search_term = f'%{tag}%'
            matching = Service.query.filter(
                Service.is_active == True,
                Service.tags.ilike(search_term)
            ).all()
            services.extend(matching)
        
        # Remove duplicates using SET
        unique_services = list(set(services))
        
        return unique_services


class ReviewSystem:
    """
    Review Management System
    
    OOP Concepts:
    - VALIDATION: Review validation
    - BUSINESS LOGIC: Rating calculations
    """
    
    def add_review(self, service_id, user_id, rating, comment):
        """
        Add review with validation
        
        Args:
            service_id (int): Service ID
            user_id (int): Reviewer user ID
            rating (int): Rating (1-5)
            comment (str): Review comment
            
        Returns:
            tuple: (Review object or None, error message or None)
        """
        # Validate rating
        if not (1 <= rating <= 5):
            return None, "Rating must be between 1 and 5"
        
        # Check if user already reviewed this service
        existing = Review.query.filter_by(
            service_id=service_id,
            user_id=user_id
        ).first()
        
        if existing:
            return None, "You have already reviewed this service"
        
        # Create review
        review = Review(
            service_id=service_id,
            user_id=user_id,
            rating=rating,
            comment=comment
        )
        
        db.session.add(review)
        db.session.commit()
        
        return review, None
    
    def get_service_reviews(self, service_id, limit=None):
        """
        Get reviews for a service
        
        Args:
            service_id (int): Service ID
            limit (int): Optional limit
            
        Returns:
            list: Review objects
        """
        query = Review.query.filter_by(service_id=service_id)\
                           .order_by(Review.created_at.desc())
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def calculate_rating_distribution(self, service_id):
        """
        Calculate rating distribution for a service
        
        Returns:
            dict: Rating distribution (1-5 stars with counts)
        """
        reviews = Review.query.filter_by(service_id=service_id).all()
        
        # Initialize distribution dictionary
        distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        for review in reviews:
            distribution[review.rating] += 1
        
        return distribution


class OrderManager:
    """
    Order Management System
    
    Data Structure: QUEUE (Scratch Implementation) for FIFO order processing
    Location: Line ~715
    Purpose: Fair order processing - first come, first served
    
    OOP Concepts: STATE MANAGEMENT
    """
    
    def __init__(self):
        """
        Initialize with Queue for order processing
        
        Data Structure: QUEUE (Scratch Implementation)
        Location: Line ~715
        Purpose: Process orders in FIFO order (First In First Out)
        
        How it works:
        1. Customer A places order #101 → enqueue(101)
        2. Customer B places order #102 → enqueue(102)
        3. Customer C places order #103 → enqueue(103)
        4. Queue: [101 → 102 → 103]
        5. Provider processes → dequeue() → Order #101 (came first!)
        6. Provider processes → dequeue() → Order #102 (came second!)
        
        Internal Structure:
        Linked list with front and rear pointers:
        [FRONT] 101 → 102 → 103 [REAR]
                ↑              ↑
             dequeue        enqueue
        
        Performance: O(1) enqueue, O(1) dequeue
        """
        self.processing_queue = Queue()  # FIFO queue for fair processing
    
    def create_order(self, service_id, buyer_id, requirements='', scope='', budget_tier='Standard', deadline=None):
        """
        Create new order
        
        Args:
            service_id (int): Service ID
            buyer_id (int): Buyer user ID
            requirements (str): Order requirements
            scope (str): Detailed scope
            budget_tier (str): Budget tier
            deadline (datetime): Agreed deadline
            
        Returns:
            Order: Created order object
        """
        service = Service.query.get(service_id)
        if not service:
            return None
            
        # Pricing Logic based on Tier
        price = service.price
        if budget_tier == 'Basic':
            price = price * 0.80  # 20% Less
        elif budget_tier == 'Premium':
            price = price * 1.50  # 50% Extra
        # Standard: Base Price
            
        order = Order(
            service_id=service_id,
            buyer_id=buyer_id,
            seller_id=service.user_id,
            total_price=round(price), # Round to nearest integer for clean display
            requirements=requirements,
            scope=scope,
            budget_tier=budget_tier,
            deadline=deadline
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Add to Queue for FIFO processing
        self.processing_queue.enqueue(order.id)
        print(f"✅ Order #{order.id} added to Queue | Queue size: {len(self.processing_queue)}")
        
        # Send notification to seller about new order
        buyer = User.query.get(buyer_id)
        if buyer:
            notification = Notification(
                user_id=service.user_id,
                title='New Order! 🎉',
                message=f'{buyer.username} has purchased your service "{service.title}" ({budget_tier} package) for ₹{round(price)}.',
                link=f'/user/orders'
            )
            db.session.add(notification)
            db.session.commit()
        
        return order
    
    def accept_order(self, order_id):
        """
        Provider accepts order
        
        When seller accepts:
        - Order status changes to 'in_progress'
        - Money automatically added to seller's wallet
        """
        order = Order.query.get(order_id)
        if order and order.status == 'pending':
            order.update_status('in_progress')
            
            # Automatic payment to seller's wallet
            from payment_system import WalletManager
            wallet_mgr = WalletManager()
            
            # Add money to seller's wallet
            payment_amount = order.total_price
            wallet_mgr.add_money(order.seller_id, payment_amount, 
                               description=f"Payment for order #{order.id} - {order.service.title}")
            
            db.session.commit()
            return True
        return False

    def complete_order(self, order_id):
        """Provider marks order as complete"""
        order = Order.query.get(order_id)
        if order and order.status == 'in_progress':
            order.update_status('completed')
            db.session.commit()
            return True
        return False
    
    def reject_order(self, order_id, rejection_reason=''):
        """
        Provider rejects/declines an order
        
        Simple cancellation with automatic refund:
        - Order cancelled
        - Money automatically refunded to buyer's wallet
        - Buyer notified with reason
        
        Args:
            order_id (int): Order ID
            rejection_reason (str): Reason for rejection
            
        Returns:
            bool: True if successful
        """
        order = Order.query.get(order_id)
        if order and order.status == 'pending':
            # Update order status
            order.update_status('cancelled')
            order.rejection_reason = rejection_reason or 'Seller unavailable'
            order.can_review = False  # Disable reviews for rejected orders
            
            # Automatic refund to buyer's wallet (as CREDIT, not debit)
            from payment_system import WalletManager
            from models import User
            wallet_mgr = WalletManager()
            
            # Get buyer username for transaction record
            buyer = User.query.get(order.buyer_id)
            buyer_username = buyer.username if buyer else f'User #{order.buyer_id}'
            
            # Credit refund to buyer's wallet
            refund_amount = order.total_price
            wallet_mgr.credit_seller(
                user_id=order.buyer_id,
                amount=refund_amount,
                description=f"Refund for cancelled order #{order.id}",
                username=buyer_username
            )
            
            db.session.commit()
            
            return True
        return False

    
    def get_user_orders(self, user_id, as_buyer=True):
        """
        Get orders for a user
        
        Args:
            user_id (int): User ID
            as_buyer (bool): True for buyer orders, False for seller orders
            
        Returns:
            list: Order objects
        """
        if as_buyer:
            return Order.query.filter_by(buyer_id=user_id)\
                             .order_by(Order.created_at.desc()).all()
        else:
            return Order.query.filter_by(seller_id=user_id)\
                             .order_by(Order.created_at.desc()).all()
    
    def update_order_status(self, order_id, new_status):
        """
        Update order status
        
        Args:
            order_id (int): Order ID
            new_status (str): New status
            
        Returns:
            bool: True if successful
        """
        order = Order.query.get(order_id)
        if order:
            return order.update_status(new_status)
        return False


class CategoryManager:
    """
    Category Management System
    
    OOP Concepts:
    - CRUD operations for categories
    - Dynamic category management
    """
    
    def get_all_categories(self):
        """
        Get all categories with service counts
        
        Returns:
            list: Category objects
        """
        return Category.query.all()
    
    def create_category(self, name, description='', icon='', color=''):
        """
        Create new category (Admin function)
        
        Args:
            name (str): Category name
            description (str): Category description
            icon (str): Icon class name
            color (str): Color class
            
        Returns:
            Category: Created category object
        """
        # Check if category already exists
        existing = Category.query.filter_by(name=name).first()
        if existing:
            return None
        
        category = Category(
            name=name,
            description=description,
            icon=icon,
            color=color
        )
        
        db.session.add(category)
        db.session.commit()
        
        return category
    
    def get_category_stats(self):
        """
        Get statistics for all categories
        
        Returns:
            list: Category stats with service counts
        """
        categories = self.get_all_categories()
        stats = []
        
        for category in categories:
            stats.append({
                'id': category.id,
                'name': category.name,
                'service_count': category.get_service_count(),
                'icon': category.icon,
                'color': category.color
            })
        
        return stats


class NotificationManager:
    """
    Notification Management System
    
    Handles creation and retrieval of user notifications
    """
    
    def create_notification(self, user_id, title, message, link=None):
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            link=link
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    def get_unread_count(self, user_id):
        """Get number of unread notifications"""
        return Notification.query.filter_by(user_id=user_id, is_read=False).count()
    
    def mark_as_read(self, notification_id):
        """Mark notification as read"""
        notification = Notification.query.get(notification_id)
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False
    
    def get_user_notifications(self, user_id, limit=10):
        """Get latest notifications"""
        return Notification.query.filter_by(user_id=user_id)\
            .order_by(Notification.created_at.desc())\
            .limit(limit).all()

    def mark_all_read(self, user_id):
        """Mark all notifications as read for a user"""
        Notification.query.filter_by(user_id=user_id, is_read=False).update({'is_read': True})
        db.session.commit()
        return True

    def delete_notification(self, notification_id):
        """Delete a single notification"""
        notification = Notification.query.get(notification_id)
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False

    def clear_all(self, user_id):
        """Delete all notifications for a user"""
        Notification.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        return True



class ChatManager:
    """
    Chat Management System for Orders
    """
    def send_message(self, order_id, sender_id, content):
        """Send a message in an order chat"""
        from models import HiddenChat
        
        # Verify sender is part of order
        order = Order.query.get(order_id)
        if not order:
            return None, "Order not found"
            
        if sender_id not in [order.buyer_id, order.seller_id]:
            return None, "Unauthorized"
            
        message = Message(
            order_id=order_id,
            sender_id=sender_id,
            content=content
        )
        
        db.session.add(message)
        
        # Auto-unhide the chat for the receiver when a new message arrives
        receiver_id = order.buyer_id if sender_id == order.seller_id else order.seller_id
        hidden = HiddenChat.query.filter_by(user_id=receiver_id, order_id=order_id).first()
        if hidden:
            db.session.delete(hidden)
        
        db.session.commit()
        
        return message, None

    def get_messages(self, order_id, user_id):
        """Get messages for an order"""
        # Verify permissions
        order = Order.query.get(order_id)
        if not order:
            return []
            
        if user_id not in [order.buyer_id, order.seller_id] and not User.query.get(user_id).is_admin():
            return []
            
        return Message.query.filter_by(order_id=order_id).order_by(Message.created_at).all()

    def get_active_chats(self, user_id):
        """
        Get all active chats for a user (pending or in_progress only),
        excluding chats the user has hidden/deleted.
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of Order objects that represent active chats
        """
        from models import HiddenChat
        
        # Get IDs of chats hidden by this user
        hidden_order_ids = db.session.query(HiddenChat.order_id).filter(
            HiddenChat.user_id == user_id
        ).subquery()
        
        # Find orders where the user is buyer or seller AND status is active
        # AND the chat is not hidden by this user
        orders = Order.query.filter(
            db.or_(Order.buyer_id == user_id, Order.seller_id == user_id),
            Order.status.in_(['pending', 'in_progress']),
            ~Order.id.in_(hidden_order_ids)
        ).order_by(Order.updated_at.desc()).all()
        
        return orders

    def hide_chat(self, order_id, user_id):
        """
        Hide a chat from the user's chat list (soft delete).
        The chat will reappear if a new message is sent.
        
        Args:
            order_id (int): Order/Chat ID
            user_id (int): User ID
            
        Returns:
            bool: True if successful
        """
        from models import HiddenChat
        
        # Verify user is part of this order
        order = Order.query.get(order_id)
        if not order:
            return False
        if user_id not in [order.buyer_id, order.seller_id]:
            return False
        
        # Check if already hidden
        existing = HiddenChat.query.filter_by(user_id=user_id, order_id=order_id).first()
        if existing:
            return True  # Already hidden
        
        hidden = HiddenChat(user_id=user_id, order_id=order_id)
        db.session.add(hidden)
        db.session.commit()
        return True

    def clear_all_chats(self, user_id):
        """
        Hide all active chats for a user (clear all).
        
        Args:
            user_id (int): User ID
            
        Returns:
            bool: True if successful
        """
        from models import HiddenChat
        
        # Get all active chat order IDs for this user
        active_orders = Order.query.filter(
            db.or_(Order.buyer_id == user_id, Order.seller_id == user_id),
            Order.status.in_(['pending', 'in_progress'])
        ).all()
        
        for order in active_orders:
            existing = HiddenChat.query.filter_by(user_id=user_id, order_id=order.id).first()
            if not existing:
                hidden = HiddenChat(user_id=user_id, order_id=order.id)
                db.session.add(hidden)
        
        db.session.commit()
        return True


class AvailabilityManager:
    """
    Availability Management System
    
    Handles provider calendar slots and bookings.
    """
    
    def get_provider_slots(self, provider_id, start_date, end_date):
        """
        Get slots for a provider within a date range
        """
        from models import AvailabilitySlot, User, Booking
        
        # 1. Get SkillVerse Slots
        slots = AvailabilitySlot.query.filter(
            AvailabilitySlot.provider_id == provider_id,
            AvailabilitySlot.start_time >= start_date,
            AvailabilitySlot.start_time <= end_date
        ).order_by(AvailabilitySlot.start_time).all()
        
        # Self-healing: Ensure is_booked flag matches actual Booking table state
        # This fixes "Ghost Availability" where slot shows green but booking fails
        consistency_fix = False
        for slot in slots:
            if not slot.is_booked:
                active_booking = Booking.query.filter_by(slot_id=slot.id).first()
                if active_booking and active_booking.status not in ['cancelled', 'rejected']:
                    slot.is_booked = True
                    consistency_fix = True
        
        if consistency_fix:
            try:
                db.session.commit()
            except:
                db.session.rollback()
        
        return slots



    def create_slots(self, provider_id, start_time, end_time, is_recurring=False, weeks=12):
        """
        Create availability slot(s)
        If is_recurring=True, creates slots for the next 'weeks' weeks
        """
        from models import AvailabilitySlot
        
        # Validation: start < end
        if start_time >= end_time:
            return None, "End time must be after start time"
            
        created_count = 0
        error_count = 0
        
        # Determine number of iterations
        iterations = weeks if is_recurring else 1
        
        current_start = start_time
        current_end = end_time
        
        for i in range(iterations):
            # Check overlap for this specific instance
            overlap = AvailabilitySlot.query.filter(
                AvailabilitySlot.provider_id == provider_id,
                AvailabilitySlot.start_time < current_end,
                AvailabilitySlot.end_time > current_start
            ).first()
            
            if not overlap:
                slot = AvailabilitySlot(
                    provider_id=provider_id,
                    start_time=current_start,
                    end_time=current_end
                )
                db.session.add(slot)
                created_count += 1
            else:
                error_count += 1
            
            # Move to next week
            current_start += timedelta(weeks=1)
            current_end += timedelta(weeks=1)
            
        db.session.commit()
        
        if created_count == 0 and error_count > 0:
            return None, "All selected slots overlap with existing availability"
            
        return {"created": created_count, "skipped": error_count}, None

    def delete_slot(self, slot_id, provider_id):
        """Delete a slot if not booked"""
        from models import AvailabilitySlot
        
        slot = AvailabilitySlot.query.get(slot_id)
        if not slot:
            return False, "Slot not found"
            
        if slot.provider_id != provider_id:
            return False, "Unauthorized"
            
        if slot.is_booked:
            return False, "Cannot delete booked slot"
            
        db.session.delete(slot)
        db.session.commit()
        return True, None

    def book_slot(self, slot_id, client_id, service_id=None, notes='', order_id=None):
        """
        Book a slot
        Uses transaction to prevent double booking
        Includes self-healing for data inconsistencies
        """
        from models import AvailabilitySlot, Booking
        
        try:
            # Start transaction (implicit in SQLAlchemy commit)
            slot = AvailabilitySlot.query.with_for_update().get(slot_id)
            
            if not slot:
                return None, "Slot not found"
                
            from datetime import datetime, timezone
            if slot.start_time < datetime.now(timezone.utc).replace(tzinfo=None):
                return None, "Cannot book a time slot in the past"
            
            # SELF-HEALING: Check for existing bookings and clean up stale ones
            existing_booking = Booking.query.filter_by(slot_id=slot_id).first()
            if existing_booking:
                if existing_booking.status in ['cancelled', 'rejected']:
                    # Clean up cancelled/rejected booking and reset slot
                    db.session.delete(existing_booking)
                    slot.is_booked = False
                    db.session.flush()
                elif slot.is_booked:
                    # Genuinely booked - cannot book
                    return None, "Slot already booked"
                else:
                    # Inconsistency: booking exists but slot not marked booked
                    # This shouldn't happen, but if it does, the booking is active
                    return None, "Slot has an active booking"
            else:
                # No booking record exists - ensure slot is marked available
                if slot.is_booked:
                    # SELF-HEALING: Slot marked booked but no booking exists - fix it
                    slot.is_booked = False
                    db.session.flush()
                    
            # Now the slot should be available - proceed with booking
            slot.is_booked = True
            
            booking = Booking(
                slot_id=slot.id,
                client_id=client_id,
                service_id=service_id,
                order_id=order_id,
                notes=notes,
                status='pending'
            )
            
            db.session.add(booking)
            db.session.commit()
            return booking, None
            
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    def cancel_booking(self, booking_id, user_id):
        """Cancel a booking (client or provider)"""
        from models import Booking
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, "Booking not found"
            
        # Check permission
        if user_id != booking.client_id and user_id != booking.slot.provider_id:
            return False, "Unauthorized"
            
        if booking.status == 'cancelled':
            return False, "Already cancelled"
            
        booking.status = 'cancelled'
        booking.slot.is_booked = False
        
        db.session.commit()
        return True, None

    def approve_booking(self, booking_id, provider_id):
        """
        Approve a booking request
        
        When provider approves booking:
        - Booking status → 'confirmed'
        - Order remains 'pending' (seller must explicitly accept/reject)
        - Seller can now see Accept/Reject buttons on order page
        """
        from models import Booking, Order
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, "Booking not found"
            
        if booking.slot.provider_id != provider_id:
            return False, "Unauthorized"
            
        if booking.status == 'confirmed':
            return False, "Already confirmed"
            
        booking.status = 'confirmed'
        
        # Create Order if not exists (but keep it PENDING)
        if not booking.order_id:
            service = booking.service
            if service:
                from managers import order_manager
                order = order_manager.create_order(
                    service_id=service.id,
                    buyer_id=booking.client_id,
                    requirements=f"Booking for {booking.slot.start_time}",
                    scope="Consultation",
                    budget_tier="Standard"
                )
                if order:
                     booking.order_id = order.id
                     # Keep order PENDING - seller must explicitly accept/reject
        
        # If order already exists, keep it pending
        # Seller will see Accept/Reject buttons on order detail page
            
        db.session.commit()
        return True, None

    def reject_booking(self, booking_id, provider_id):
        """Reject a booking"""
        from models import Booking
        
        booking = Booking.query.get(booking_id)
        if not booking:
            return False, "Booking not found"
            
        if booking.slot.provider_id != provider_id:
            return False, "Unauthorized"
            
        booking.status = 'cancelled'
        booking.slot.is_booked = False
        
        db.session.commit()
        return True, None


# Create singleton instances
service_manager = ServiceManager()
user_manager = UserManager()
search_engine = SearchEngine()
review_system = ReviewSystem()
order_manager = OrderManager()
category_manager = CategoryManager()
notification_manager = NotificationManager()
chat_manager = ChatManager()
availability_manager = AvailabilityManager()
