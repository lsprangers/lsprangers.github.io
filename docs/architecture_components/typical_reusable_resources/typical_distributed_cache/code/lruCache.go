package lruCache

// LRUCache is a simple LRU cache implementation
type LRUCache struct {
	capacity int
	cache    map[string]*entry // make(map[KeyType]ValueType). String --> pointer[entry]
	head     *entry
	tail     *entry
}

type entry struct {
	key   string
	value interface{} // empty interface type. It specifies zero methods, which means it is satisfied by every type in the Go programming language
	prev  *entry
	next  *entry
}

// NewLRUCache creates a new LRUCache with the given capacity
func NewLRUCache(capacity int) *LRUCache {

	return &LRUCache{
		capacity: capacity,
		cache:    make(map[string]*entry),
	}
}

// Get retrieves a value from the cache and marks it as recently used
// A method with a receiver, func (c *LRUCache), the receiver variable c is automatically available inside the method as a pointer to the struct. Therefore c.cache is valid, because Go automaticaly dereferences the pointer when you use the dot operator. THat's why we don't have to go (*c).cache[key]
func (c *LRUCache) Get(key string) (interface{}, bool) {
	if e, ok := c.cache[key]; ok {
		// e is a pointer to an entry, entry is a linked list node type
		c.moveToFront(e)
		return e.value, true
	}
	return nil, false
}

// Put adds a value to the cache, evicting the least recently used if necessary
func (c *LRUCache) Put(key string, value interface{}) {
	// Update value in cache, move to front
	if e, ok := c.cache[key]; ok {
		e.value = value
		c.moveToFront(e)
		return
	}

	// else create the new entry and move it to front
	e := &entry{key: key, value: value}
	c.cache[key] = e
	c.addToFront(e)
	if len(c.cache) > c.capacity {
		c.evict()
	}
}

func (c *LRUCache) moveToFront(e *entry) {
	// If it's the head, return
	if c.head == e {
		return
	}

	// Remove pointers
	c.remove(e)
	c.addToFront(e)
}

func (c *LRUCache) addToFront(e *entry) {
	e.prev = nil
	e.next = c.head
	if c.head != nil {
		c.head.prev = e
	}
	c.head = e
	if c.tail == nil {
		c.tail = e
	}
}

func (c *LRUCache) remove(e *entry) {
	if e.prev != nil {
		e.prev.next = e.next
	} else {
		c.head = e.next
	}
	if e.next != nil {
		e.next.prev = e.prev
	} else {
		c.tail = e.prev
	}
}

func (c *LRUCache) evict() {
	if c.tail == nil {
		return
	}
	delete(c.cache, c.tail.key)
	c.remove(c.tail)
}
