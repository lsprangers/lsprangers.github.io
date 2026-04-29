package lruCache

import (
	"sync"
)

type CacheService struct {
	lru  *LRUCache
	lock sync.RWMutex
}

func NewCacheService(capacity int) *CacheService {
	return &CacheService{
		lru: NewLRUCache(capacity),
	}
}

func (c *CacheService) Get(key string) (interface{}, bool) {
	c.lock.RLock()
	defer c.lock.RUnlock()
	return c.lru.Get(key)
}

func (c *CacheService) Put(key string, value interface{}) {
	c.lock.Lock()
	defer c.lock.Unlock()
	c.lru.Put(key, value)
}
