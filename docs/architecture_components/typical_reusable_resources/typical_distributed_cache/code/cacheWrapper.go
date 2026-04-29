package lruCache

import (
	"sync"
)

type CacheWrapper struct {
	lru  *LRUCache
	lock sync.RWMutex
}

func NewCacheWrapper(capacity int) *CacheWrapper {
	return &CacheWrapper{
		lru: NewLRUCache(capacity),
	}
}

func (c *CacheWrapper) Get(key string) (interface{}, bool) {
	c.lock.RLock()
	defer c.lock.RUnlock()
	return c.lru.Get(key)
}

func (c *CacheWrapper) Put(key string, value interface{}) {
	c.lock.Lock()
	defer c.lock.Unlock()
	c.lru.Put(key, value)
}
