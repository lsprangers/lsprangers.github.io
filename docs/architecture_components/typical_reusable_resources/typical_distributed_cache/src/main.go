package main

import (
	"encoding/json"
	"net/http"

	"lsprangers.com/cache/cache"
)

var svc = cache.NewCacheWrapper(100)

func GetHandler(w http.ResponseWriter, r *http.Request) {
	key := r.URL.Query().Get("key")
	value, ok := svc.Get(key)
	if !ok {
		http.NotFound(w, r)
		return
	}
	json.NewEncoder(w).Encode(map[string]interface{}{"key": key, "value": value})
}

func PutHandler(w http.ResponseWriter, r *http.Request) {
	var req struct {
		Key   string      `json:"key"`
		Value interface{} `json:"value"`
	}
	json.NewDecoder(r.Body).Decode(&req)
	svc.Put(req.Key, req.Value)
	w.WriteHeader(http.StatusNoContent)
}

// curl -X POST -d '{"key":"foo","value":"bar"}' -H "Content-Type: application/json" http://localhost:8080/put
// curl "http://localhost:8080/get?key=foo"
// curl -X POST -d '{"key":"one","value":"1"}' -H "Content-Type: application/json" http://localhost:8080/put
// curl -X POST -d '{"key":"two","value":"2"}' -H "Content-Type: application/json" http://localhost:8080/put
// curl -X POST -d '{"key":"three","value":"3"}' -H "Content-Type: application/json" http://localhost:8080/put

func main() {
	http.HandleFunc("/get", GetHandler)
	http.HandleFunc("/put", PutHandler)
	http.ListenAndServe(":8080", nil)
}
