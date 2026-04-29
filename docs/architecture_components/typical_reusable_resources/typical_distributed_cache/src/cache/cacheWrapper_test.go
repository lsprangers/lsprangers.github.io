package cache

import (
	"sync"
	"testing"
)

func TestCacheWrapperBasic(t *testing.T) {
	cache := NewCacheWrapper(2)
	cache.Put("a", 1)
	cache.Put("b", 2)
	if v, ok := cache.Get("a"); !ok || v != 1 {
		t.Errorf("expected 1, got %v", v)
	}
	cache.Put("c", 3) // evicts "b"
	if _, ok := cache.Get("b"); ok {
		t.Error("expected b to be evicted")
	}
}

func TestCacheWrapperConcurrency(t *testing.T) {
	cache := NewCacheWrapper(10)
	wg := sync.WaitGroup{} // waits for a collection of goRoutines to finish
	for i := 0; i < 100; i++ {
		wg.Add(1)
		// new goRoutine
		go func(i int) {
			defer wg.Done() // Call wg.Done when the current goRoutine finishes, even if it panics and exits
			key := string(rune('a' + (i % 10)))
			cache.Put(key, i)
			cache.Get(key)
		}(i) //input to goRoutine
	}
	wg.Wait()
}
