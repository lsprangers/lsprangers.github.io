package cache

import (
	"testing"
)

func TestLRUCacheBasic(t *testing.T) {
	cache := NewLRUCache(2)
	cache.Put("a", 1)
	cache.Put("b", 2)
	if v, ok := cache.Get("a"); !ok || v != 1 {
		t.Errorf("expected 1, got %v", v)
	}
	cache.Put("c", 3) // evicts "b"
	if _, ok := cache.Get("b"); ok {
		t.Error("expected b to be evicted")
	}
	if v, ok := cache.Get("c"); !ok || v != 3 {
		t.Errorf("expected 3, got %v", v)
	}
}

func TestLRUCacheUpdate(t *testing.T) {
	cache := NewLRUCache(2)
	cache.Put("a", 1)
	cache.Put("a", 2)
	if v, ok := cache.Get("a"); !ok || v != 2 {
		t.Errorf("expected 2, got %v", v)
	}
}

func TestLRUCacheEvictionOrder(t *testing.T) {
	cache := NewLRUCache(2)
	cache.Put("a", 1)
	cache.Put("b", 2)
	cache.Get("a")
	cache.Put("c", 3) // evicts "b"
	if _, ok := cache.Get("b"); ok {
		t.Error("expected b to be evicted")
	}
	if v, ok := cache.Get("a"); !ok || v != 1 {
		t.Errorf("expected 1, got %v", v)
	}
}

func TestLRUCacheEmpty(t *testing.T) {
	cache := NewLRUCache(1)
	if _, ok := cache.Get("x"); ok {
		t.Error("expected cache miss for x")
	}
}
